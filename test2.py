import os
import math
import datetime
import time
import json
import re
import zlib
import csv
import ecdsa
import base64
import uuid
import random
import ast
import itertools
import requests
import string
import subprocess
import boto3
import botocore
import struct
from hashlib import md5
from uuid import uuid4
from random import choice
from fabric.api import hide
from filechunkio import FileChunkIO
from marvin_lib.cli import cli
from marvin_lib.inifile import Inifile
from io import BytesIO
from marvin_lib.task import wait_for_tasks
from testhelpers.common import utils_ssh as us
from testhelpers.base_class import BaseTest
from testhelpers.base_class import AllActions as AA
from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from testhelpers.environment_type import EnvironmentType as ets
from scalerim_api import IdentityManager
from scalerim_api.ttypes import SIM_IdentitiesUpdateArgs, SIM_QuotaLimits, SIM_QuotaEnforcementType_t
from scalerim_api.constants import SERVICE_URL as SCALERIM_SERVICE_URL
from scaler_python_utils.thrift.connection import ScalerThriftHttpConnection
from boto.s3.lifecycle import Lifecycle, Rule, Expiration
from sync_sharded_arakoon_client.cluster_client import ClusterClient as ArakoonClusterClient
from boto.s3.deletemarker import DeleteMarker
from scalerdb_api.values.ttypes import SDB_ReplicationSystemType
METERING_LOG = "/opt/ampli/var/metering/"
FLAME_CFG = "/opt/ampli/cfg/flame/flame.cfg"
BEGIN_MARKER = '-----BEGIN LICENSE-----'
END_MARKER = '-----END LICENSE-----'
SCHEME_VERSION_V1 = 'V1'
SIM_URL_ON_SCALER = 'localhost:9400'

auth = us.Authentication('hgstsupport', 'Hg$t5upq0rt!')

ENCRYPTION_DISABLED = 'ENCRYPT_NOTHING'
ENCRYPTION_ALL = 'ENCRYPT_EVERYTHING'
ENCRYTPION_CLIENT_SIDE = 'ENCRYPT_CLIENT_SELECTION'

timing_params = ["db_update_max_duration", "multipart_upload_initiate_max_duration",
                 "multipart_upload_complete_and_abort_max_duration", "multipart_upload_part_upload_max_duration",
                 "put_max_duration", "safety_margin"]
FLAME_REPORTS = "/opt/ampli/var/flame_reports/"
FILE_MANAGER = "/opt/ampli/apps/marvinbase/tools/filemanager.py"
REQUIRED_KEYS = ['environment']

DEFAULT_CONFIG = {
    "deviceId": "264f104e-dab2-4c54-92c6-c93199c34c90",
    "sequenceId": 0,
    "sourceAccessInfo": {
        "email": "Rhegal.Devtest@hgst.com",
        "accessKey": "",
        "secretKey": ""
    },
    "destinationSystemName": "BLR_Hallmark",
    "destinationAccessInfo": {
        "email": "Rhegal.Datapump@hgst.com",
        "accessKey": "",
        "secretKey": ""
    },
    "destinationS3IpPorts": [
        "1.1.1.1:1000",
        "2.2.2.2:2000",
        "3.3.3.3:3000"
    ],
    "destinationS3DNSSuffix": "s3.amazonaws.com",
    "shouldCheckDestinationSSLCert": False,
    "destinationSSLCertSHA1Fingerprint": "17810b5c4a36adb659127e0571bd1cfad93901ab",
    "status": "ENABLED",
    "queueObjectCountThreshold": "100000",
    "queueMaxSizeThreshold": "100000"
}

DEFAULT_CONFIG_AWS = {
    "deviceId": "264f104e-dab2-4c54-92c6-c93199c34c90",
    "sequenceId": 0,
    "sourceAccessInfo": {
        "email": "Rhegal.Devtest@hgst.com",
        "accessKey": "",
        "secretKey": ""
    },
    "destinationSystemName": "aws",
    "destinationAccessInfo": {
        "email": "Rhegal.Datapump@hgst.com",
        "accessKey": "",
        "secretKey": ""
    },
    "status": "ENABLED",
    "queueObjectCountThreshold": "100000",
    "queueMaxSizeThreshold": "100000",
    "systemType": SDB_ReplicationSystemType.AWS

}


class LocalUtils(BaseTest):

    @classmethod
    def setUpClass(cls):
        super(LocalUtils, cls).setUpClass()
        cls.scaler_guids, cls.scaler_nodes = zip(*[[scaler.guid, scaler.name]
                                                   for scaler in cls.et.get_target(ets.ALL_SCALER)])
        cls.column_guids = [column.guid for column in cls.et.columns.columns]
        cls.column_nodes = cls.backends = list()
        for column in cls.et.columns.columns:
            for node in column.nodes:
                cls.backends.append(cls.env.get_machine(node.name))
                cls.column_nodes.append([node.name, node.guid])
        cls.scalers = [m.machine for m in cls.et.get_target(ets.ALL_SCALER)]
        cls.scaler_mgmt = [m.machine for m in cls.et.get_target(ets.ALL_SCALER) if m.role=='SPXMGMT']

        cls.scalers[0].run_cmd('sudo /etc/init.d/iptables-persistent flush', use_sudo=True)
        cls.m = cli(verbose=4)

        cls.env_info = cls.m.environment.list()[0]
        cls.node_ops = MultiNodeOps(cls.env, cls.scalers, cls.scaler_mgmt, cls.et.hardware)
        cls.s3_ops = S3_Ops(cls.env_info, cls.scalers, cls.et.hardware)
        cls.s3_ops_backend = S3_Ops_Column(cls.env_info, cls.backends, cls.et.hardware)


    def setUp(self, site1_system_type='as', site2_system_type='as'):
        super(LocalUtils, self).setUp()
        self.site1_system_type = site1_system_type
        self.site2_system_type = site2_system_type
        self.buckets_to_clean = []
        self.buckets_to_clean_site1 = []
        self.buckets_to_clean_site2 = []
        self.versioning_enabled = False
        self.site2 = self.get_site2()
        if site2_system_type is 'aws':
            self.site2 = 'aws'
        elif site2_system_type is 'as':
            self.site2 = self.get_site2()
        else:
            self.site2 = None;

        if self.site2 is None:
            self.flame = FlameUtils(self.env, self.scalers)

        elif self.site2 == "aws":
            self.scalers_site1 = [scaler.machine for scaler in self.get_target(ets.ALL_SCALER)]
            self.scalers = self.get_target(ets.ALL_SCALER)
            self.m = cli(verbose=4)
            self.env_info = self.m.environment.list()[0]
            self.scaler_nodes_site1 = [scaler.name for scaler in self.scalers]
            self.keyrouter = ScalerKeyrouter(self.scalers_site1)



            self.s3_ops_site1 = S3_Ops(self.env_info, self.scalers_site1, self.et.hardware, sys_type=self.site1_system_type)
            self.s3_ops_site2 = S3_Ops(self.env_info, self.scalers_site1, self.et.hardware, sys_type=self.site2_system_type)

            self.boto_site1 = self.s3_ops_site1.get_s3_connection()
            self.boto_site2 = self.s3_ops_site2.get_s3_connection()
            self.boto3_site1 = self.s3_ops_site1.get_boto3_connection()
            self.boto3_site2 = self.s3_ops_site2.get_boto3_connection()

            self.src_api_key, self.src_sec_key = self.s3_ops_site1.get_credentials()
            self.dst_api_key, self.dst_sec_key = self.s3_ops_site2.get_credentials()

            self.versioning_enabled = True
            self.object_list = []
            self.buck_keys = []
            self.map_objects = {}
            self.src_bucket_name1 = None
            self.src_bucket_name2 = None
            self.src_bucket, self.src_bucket_name = self.s3_ops_site1.create_bucket(self.boto_site1)
            self.dst_bucket, self.dst_bucket_name = self.s3_ops_site2.create_bucket(self.boto_site2)
            self.buckets_to_clean_site1 = [self.src_bucket_name]
            self.buckets_to_clean_site2 = [self.dst_bucket_name]

            self.lg('Enabling versioing on source bucket %s' % self.src_bucket_name)
            self.src_bucket.configure_versioning(versioning=True)
            time.sleep(120)
            self.assertTrue(self.src_bucket.get_versioning_status()['Versioning'] == 'Enabled',
                            'Versioning not enabled for bucket %s' % self.src_bucket_name)

            self.lg('Enabling versioing on destination bucket %s' % self.dst_bucket_name)
            self.dst_bucket.configure_versioning(versioning=True)
            time.sleep(120)
            self.assertTrue(self.dst_bucket.get_versioning_status()['Versioning'] == 'Enabled',
                            'Versioning not enabled for bucket %s' % self.dst_bucket_name)

            self.src_api_key, self.src_sec_key = self.s3_ops_site1.get_credentials()
            self.flame_site1 = FlameUtils(self.env, self.scalers_site1)
        else:
            self.site2 = self.get_site2()
            self.scalers_site1 = [scaler.machine for scaler in self.get_target(ets.ALL_SCALER)]
            self.scalers_site2 = [scaler.machine for scaler in self.site2.get_target(ets.ALL_SCALER)]
            self.scalers1 = self.get_target(ets.ALL_SCALER)
            self.scalers2 = self.site2.get_target(ets.ALL_SCALER)
            self.router_node = [i.name for i in self.env.machines if i.name.endswith('router-system')][0]
            self.router_vm = self.env.get_machine(self.router_node)

            self.m = cli(verbose=4)
            self.env_info = self.m.environment.list()[0]

            self.scaler_nodes_site1 = [scaler.name for scaler in self.scalers1]
            self.scaler_nodes_site2 = [scaler.name for scaler in self.scalers2]

            self.s3_ops_site1 = S3_Ops(self.env_info, self.scalers_site1, self.et.hardware,
                                       sys_type=self.site1_system_type)
            self.s3_ops_site2 = S3_Ops(self.env_info, self.scalers_site2, self.et.hardware,
                                       sys_type=self.site2_system_type)

            self.boto_site1 = self.s3_ops_site1.get_s3_connection()
            self.boto_site2 = self.s3_ops_site2.get_s3_connection()
            self.boto3_site1 = self.s3_ops_site1.get_boto3_connection()
            self.boto3_site2 = self.s3_ops_site2.get_boto3_connection()

            self.site1_ips = []
            self.site2_ips = []

            site1_netguid = ""
            site2_netguid = ""

            for net in self.ha.get_retry('/model/network')["network"]:
                if net["networktype"] == "PUBLIC":
                    for r in net["route"]:
                        if r["destination_network"] != '0.0.0.0' and r["destination_network_guid"] is None:
                            site1_netguid = net["guid"]
                            break
            for net in self.site2.ha.get_retry('/model/network')["network"]:
                if net["networktype"] == "PUBLIC":
                    for r in net["route"]:
                        if r["destination_network"] != '0.0.0.0' and r["destination_network_guid"] is None:
                            site2_netguid = net["guid"]
                            break

            for m in self.scalers1:
                nets = self.ha.get_retry("/model/machine/{}".format(m.guid))["machine"]["nic"]
                for n in nets:
                    if n["network"] == site1_netguid:
                        self.site1_ips.append(n["address"])
            for m in self.scalers2:
                nets = self.site2.ha.get_retry("/model/machine/{}".format(m.guid))["machine"]["nic"]
                for n in nets:
                    if n["network"] == site2_netguid:
                        self.site2_ips.append(n["address"])

            self.src_api_key, self.src_sec_key = self.s3_ops_site1.get_credentials()
            self.dst_api_key, self.dst_sec_key = self.s3_ops_site2.get_credentials()

            self.versioning_enabled = True
            self.object_list = []
            self.buck_keys = []
            self.map_objects = {}
            self.src_bucket_name1 = None
            self.src_bucket_name2 = None
            self.src_bucket, self.src_bucket_name = self.s3_ops_site1.create_bucket(self.boto_site1)
            self.dst_bucket, self.dst_bucket_name = self.s3_ops_site2.create_bucket(self.boto_site2)
            self.buckets_to_clean_site1 = [self.src_bucket_name]
            self.buckets_to_clean_site2 = [self.dst_bucket_name]

            self.lg('Enabling versioing on source bucket %s' % self.src_bucket_name)
            self.src_bucket.configure_versioning(versioning=True)
            self.assertTrue(self.src_bucket.get_versioning_status()['Versioning'] == 'Enabled',
                            'Versioning not enabled for bucket %s' % self.src_bucket_name)

            self.lg('Enabling versioing on destination bucket %s' % self.dst_bucket_name)
            self.dst_bucket.configure_versioning(versioning=True)
            self.assertTrue(self.dst_bucket.get_versioning_status()['Versioning'] == 'Enabled',
                            'Versioning not enabled for bucket %s' % self.dst_bucket_name)

            self.src_api_key, self.src_sec_key = self.s3_ops_site1.get_credentials()

            self.flame_site1 = FlameUtils(self.env, self.scalers_site1)
            self.flame_site2 = FlameUtils(self.env, self.scalers_site2)

    def tearDown(self):
        super(LocalUtils, self).tearDown()
        if len(self.buckets_to_clean_site1) > 0 and self.versioning_enabled is True:
            for bucket in self.buckets_to_clean_site1:
                self.s3_ops_site1.delete_all_versions(self.boto_site1, bucket)
            run_id = self.flame_site1.run_flame(self.scalers_site1[0], 'scalerdb_background')
            self.flame_site1.wait_for_flame_job(self.scalers_site1[0], run_id)
            for bucket in self.buckets_to_clean_site1:
                self.s3_ops_site1.delete_bucket(self.boto_site1, bucket)

        if len(self.buckets_to_clean_site2) > 0 and self.versioning_enabled is True:
            for bucket in self.buckets_to_clean_site2:
                self.s3_ops_site2.delete_all_versions(self.boto_site2, bucket)
        if self.site2 is 'aws':
            self.lg('In aws teardown')
            self.lg('Buckets to clean is %s' % self.buckets_to_clean_site2)
            for bucket in self.buckets_to_clean_site2:
                self.s3_ops_site2.delete_all_versions(self.boto_site2, bucket)
                self.s3_ops_site2.delete_bucket(self.boto_site2, bucket)

        elif self.site2 is 'as':
            run_id = self.flame_site2.run_flame(self.scalers_site2[0], 'scalerdb_background')
            self.flame_site2.wait_for_flame_job(self.scalers_site2[0], run_id)
            for bucket in self.buckets_to_clean_site2:
                self.s3_ops_site2.delete_bucket(self.boto_site2, bucket)

        if len(self.buckets_to_clean) > 0 and self.versioning_enabled is True:
            for bucket in self.buckets_to_clean:
                self.s3_ops.delete_all_versions(self.boto_connection, bucket)
            run_id = self.flame.run_flame_marvin_task(self.scalers[0], self.m, FlameUtils.FLAME_GC_OLM)
            self.flame.wait_for_flame_job(self.scalers[0], run_id)
            for bucket in self.buckets_to_clean:
                self.s3_ops.delete_bucket(self.boto_connection, bucket)
        if len(self.buckets_to_clean) > 0 and self.versioning_enabled is not True:
                for bucket in self.buckets_to_clean:
                    self.s3_ops.delete_bucket(self.boto_connection, bucket)
        if hasattr(self, 'multi_buckets_to_clean') and len(self.multi_buckets_to_clean) > 0:
            for bucket_dict in self.multi_buckets_to_clean:
                for bucket_keys in bucket_dict['Bucket Keys']:
                    self.user1_conn.delete_object(bucket_dict['User Conn'], bucket_dict['Bucket Name'],
                                                  key=bucket_keys)
                self.account_conn.delete_bucket(bucket_dict['Account Conn'], bucket_dict['Bucket Name'])
            self.multi_buckets_to_clean = []
        if hasattr(self, "clean_job") and self.clean_job is True:
            run_ids = []
            info = self.scalers[0].run_cmd('/opt/ampli/bin/flame job list --format=json', use_sudo=True)
            out = info.splitlines()
            json_info = json.loads(out[-1])
            for item in json_info:
                if item["status"] in ['CREATED', 'RUNNING']:
                    run_ids.append(item['runId'])
            for ids in run_ids:
                self.flame.stop_flame_job(self.scalers[0], ids)
            self.clean_job = False
        if hasattr(self, "timing_param") and self.timing_param is True:
            self.flame.unset_timing_params()
            self.timing_param = False
        if hasattr(self, "cron_restore") and self.cron_restore is True:
            self.flame.restore_root_cron()
            self.flame.clean_local_reports()
            self.timing_param = False
        if hasattr(self, "connection_attempt") and self.connection_attempt is True:
            self.flame.unset_connection_attempts()
            self.connection_attempt = False
        if hasattr(self, "throttle") and self.throttle is not None:
            self.flame.unset_throttling_ms()
            self.throttle = None
        if hasattr(self, "cores"):
            self.flame.revert_max_core()
        if hasattr(self, "mona_down") and self.mona_down is True:
            self.flame.start_mona()
            self.mona_down = False
        self.assertTrue(self.node_ops.check_health_of_all_nodes(), 'Health Check failed In setup')


class FlameUtils:

    FLAME_CAPACITY = 'scalerdb_foreground'
    FLAME_GC_OLM = 'scalerdb_background'
    FLAME_COMPLETE = 'scalerdb'
    FLAME_OLM = 'olm_scalerdb'
    FLAME_GC = 'gc_scalerdb'
    FLAME_CAPACITY_OLD = 'capacity_scalerdb'

    def __init__(self, env, scalers):
        self.cfg_flame = []
        self.cfg_scalerd = []
        self.env = env
        self.scalers = scalers
        for node in self.scalers:
            self.cfg_flame.append(ScalerConfigParser(node, 'flame'))
            self.cfg_scalerd.append(ScalerConfigParser(node, 'scalerd'))

    @staticmethod
    def run_flame(node, workitem):
        print 'Running %s job in %s' % (workitem, node.name)
        running = False
        time_out = 300
        output = node.run_cmd('/opt/ampli/bin/flame job start %s' % workitem, use_sudo=True)
        result_clean = [x.strip() for x in output.split('\n') if x.strip()]
        run_id = result_clean[-1]
        job_info = FlameUtils.get_job_info(node, run_id)
        if job_info["status"] not in ["CREATED", "RUNNING", "FINISHED"]:
            assert running, 'Job %s is in %s state' % (run_id, job_info["status"])
        if job_info["status"] == "CREATED":
            print 'Job with run ID %s is in CREATED state' % run_id
            while not running and time_out > 0:
                job_info = FlameUtils.get_job_info(node, run_id)
                if job_info["status"] in ["RUNNING", "FINISHED"]:
                    print 'Job %s is in %s state' % (run_id, job_info["status"])
                    return run_id
                elif job_info["status"] in ["FAILED", "KILLED"]:
                    assert running, 'Job %s is in %s state' % (run_id, job_info["status"])
                time.sleep(30)
                time_out -= 30
        elif job_info["status"] in ["RUNNING", "FINISHED"]:
            print 'Job %s is in %s state' % (run_id, job_info["status"])
            return run_id

    @staticmethod
    def run_flame_marvin_task(node, marvin_cli, workitem):
        run_id = None
        running = False
        time_out = 300
        init_run_ids = []
        latest_run_ids = []
        info = node.run_cmd('/opt/ampli/bin/flame job list --format=json', use_sudo=True)
        out = info.splitlines()
        json_info = json.loads(out[-1])
        for item in json_info:
            init_run_ids.append(item['runId'])
        task = None
        if workitem == 'scalerdb_foreground':
            capacity_task = marvin_cli.taskschedule.run("flame_scalerdb_foreground")
            print "capacity_task guid %s" % capacity_task['guid']
            wait_for_tasks([capacity_task], stop_on_error=True)
            task = marvin_cli.task.get(capacity_task['guid'])
            print "capacity_task status %s" % task['status']

        elif workitem == 'scalerdb_background':
            gc_task = marvin_cli.taskschedule.run("flame_scalerdb_background")
            print "gc_task guid %s" % gc_task['guid']
            wait_for_tasks([gc_task], stop_on_error=True)
            task = marvin_cli.task.get(gc_task['guid'])
            print "gc_task status %s" % task['status']

        elif workitem == 'scalerdb_verify':
            verifier_task = marvin_cli.taskschedule.run("flame_scalerdb_verifier")
            print "verifier_task guid %s" % verifier_task['guid']
            wait_for_tasks([verifier_task], stop_on_error=True)
            task = marvin_cli.task.get(verifier_task['guid'])
            print "verifier_task status %s" % task['status']

        assert task['status'] == 'SUCCESS', 'Marvin task status is not SUCCESS, Current status is %s' % task['status']
        info = node.run_cmd('/opt/ampli/bin/flame job list --format=json', use_sudo=True)
        out = info.splitlines()
        json_info = json.loads(out[-1])
        for item in json_info:
            latest_run_ids.append(item['runId'])
        for i in latest_run_ids:
            if i not in init_run_ids:
                run_id = i
        print 'Init run ids %s' % init_run_ids
        print 'Latest run ids %s' % latest_run_ids
        assert run_id is not None, 'Run Id not found'
        job_info = FlameUtils.get_job_info(node, run_id)
        if job_info["status"] not in ["CREATED", "RUNNING", "FINISHED"]:
            assert running, 'Job %s is in %s state' % (run_id, job_info["status"])
        if job_info["status"] == "CREATED":
            print 'Job with run ID %s is in CREATED state' % run_id
            while not running and time_out > 0:
                job_info = FlameUtils.get_job_info(node, run_id)
                if job_info["status"] in ["RUNNING", "FINISHED"]:
                    print 'Job %s is in %s state' % (run_id, job_info["status"])
                    return run_id
                elif job_info["status"] in ["FAILED", "KILLED"]:
                    assert running, 'Job %s is in %s state' % (run_id, job_info["status"])
                time.sleep(30)
                time_out -= 30
        elif job_info["status"] in ["RUNNING", "FINISHED"]:
            print 'Job %s is in %s state' % (run_id, job_info["status"])
            return run_id

    @staticmethod
    def run_quota_checker(node, taskschedule, marvin_cli):
        if taskschedule == 'account_quota_checker':
            quota_checker_task = marvin_cli.taskschedule.run(taskschedule)
            print "task guid %s" % quota_checker_task['guid']
            wait_for_tasks([quota_checker_task], stop_on_error=True)
            task = marvin_cli.task.get(quota_checker_task['guid'])
            print "task status %s" % task['status']
        assert task['status'] == 'SUCCESS', 'Account quota checker status is not SUCCESS, Current status is %s' % task[
            'status']
        return quota_checker_task['date_modified']

    @staticmethod
    def run_object_verifier_checker(node, taskschedule, marvin_cli):
        if taskschedule == 'flame_object_verifier_report_check':
            object_verifier_checker_task = marvin_cli.taskschedule.run(taskschedule)
            print "task guid %s" % object_verifier_checker_task['guid']
            wait_for_tasks([object_verifier_checker_task], stop_on_error=True)
            task = marvin_cli.task.get(object_verifier_checker_task['guid'])
            print "task status %s" % task['status']
        assert task['status'] == 'SUCCESS', 'Flame verifier is not SUCCESS, Current status is %s' % task[
            'status']
        return object_verifier_checker_task['date_modified']

    @staticmethod
    def get_job_info(node, run_id):
        info = node.run_cmd('/opt/ampli/bin/flame job info %s --format=json' % run_id,
                            use_sudo=True)
        result_clean = [x.strip() for x in info.split('\n') if x.strip()]
        return json.loads(result_clean[-1])

    def wait_for_flame_job(self, node, run_id, time_out=1200):
        finished = False
        elapsed_time = 0
        while not finished and elapsed_time < time_out:
            job_info = self.get_job_info(node, run_id)
            if job_info["status"] == "FINISHED":
                print 'Start time of Job %s : %s' % (run_id, job_info['startTime'])
                print 'End time of Job %s : %s' % (run_id, job_info['endTime'])
                finished = True
                break
            elif job_info["status"] in ["FAILED", "KILLED"]:
                break
            time.sleep(30)
            elapsed_time += 30
        return finished

    @staticmethod
    def stop_flame_job(node, run_id):
        print 'Stopping job with id %s in %s' % (run_id, node.name)
        node.run_cmd('/opt/ampli/bin/flame job stop %s' % run_id,
                     use_sudo=True)

    @staticmethod
    def restart_flame_job(node, run_id):
        print 'Restarting job with id %s in %s' % (run_id, node.name)
        node.run_cmd('/opt/ampli/bin/flame job restart %s' % run_id,
                     use_sudo=True, warn_only=True)

    def set_throttling_ms(self, throttle):
        print 'Setting throttling in all scaler nodes'
        for config in self.cfg_flame:
            config.update_config("workitem.capacity_scalerdb", "throttling_ms", throttle)
            config.update_config("workitem.gc_scalerdb", "throttling_ms", throttle)
            config.update_config("workitem.scalerdb", "throttling_ms", throttle)
            config.update_config("workitem.olm_scalerdb", "throttling_ms", throttle)
            config.update_config("workitem.scalerdb_foreground", "throttling_ms", throttle)
            config.update_config("workitem.scalerdb_background", "throttling_ms", throttle)

    def unset_throttling_ms(self):
        print 'Unsetting throttling in all scaler nodes'
        for config in self.cfg_flame:
            config.update_config("workitem.capacity_scalerdb", "throttling_ms", 100)
            config.update_config("workitem.gc_scalerdb", "throttling_ms", 100)
            config.update_config("workitem.scalerdb", "throttling_ms", 100)
            config.update_config("workitem.olm_scalerdb", "throttling_ms", 100)
            config.update_config("workitem.scalerdb_foreground", "throttling_ms", 0)
            config.update_config("workitem.scalerdb_background", "throttling_ms", 100)

    def change_max_core(self):
        print 'Changing cores.max in all scaler nodes'
        for config in self.cfg_flame:
            config.update_config("workitem.scalerdb_foreground", "cores.max", 1)
            config.update_config("workitem.scalerdb_background", "cores.max", 1)

    def revert_max_core(self):
        print 'Changing cores.max in all scaler nodes'
        for config in self.cfg_flame:
            config.update_config("workitem.scalerdb_foreground", "cores.max", 9)
            config.update_config("workitem.scalerdb_background", "cores.max", 6)

    def set_batch_size(self, size):
        print 'Setting batch size in all scaler nodes'
        for config in self.cfg_flame:
            config.update_config("workitem.capacity_scalerdb", "batch_size", size)
            config.update_config("workitem.gc_scalerdb", "batch_size", size)
            config.update_config("workitem.scalerdb", "batch_size", size)
            config.update_config("workitem.olm_scalerdb", "batch_size", size)
            config.update_config("workitem.scalerdb_foreground", "batch_size", size)
            config.update_config("workitem.scalerdb_background", "batch_size", size)

    def unset_batch_size(self):
        print 'Unsetting batch size in all scaler nodes'
        for config in self.cfg_flame:
            config.update_config("workitem.capacity_scalerdb", "batch_size", 1000)
            config.update_config("workitem.gc_scalerdb", "batch_size", 1000)
            config.update_config("workitem.scalerdb", "batch_size", 1000)
            config.update_config("workitem.olm_scalerdb", "batch_size", 1000)
            config.update_config("workitem.scalerdb_foreground", "batch_size", 1000)
            config.update_config("workitem.scalerdb_background", "batch_size", 1000)

    def set_checkpoint_interval_secs(self, sec):
        print 'Setting checkpoint interval secs in all scaler nodes'
        for config in self.cfg_flame:
            config.update_config("workitem.capacity_scalerdb", "checkpoint_interval_secs", sec)
            config.update_config("workitem.gc_scalerdb", "checkpoint_interval_secs", sec)
            config.update_config("workitem.scalerdb", "checkpoint_interval_secs", sec)
            config.update_config("workitem.olm_scalerdb", "checkpoint_interval_secs", sec)
            config.update_config("workitem.scalerdb_foreground", "checkpoint_interval_secs", sec)
            config.update_config("workitem.scalerdb_background", "checkpoint_interval_secs", sec)

    def unset_checkpoint_interval_secs(self):
        print 'Unsetting checkpoint interval sec in all scaler nodes'
        for config in self.cfg_flame:
            config.update_config("workitem.capacity_scalerdb", "checkpoint_interval_secs", 600)
            config.update_config("workitem.gc_scalerdb", "checkpoint_interval_secs", 600)
            config.update_config("workitem.scalerdb", "checkpoint_interval_secs", 600)
            config.update_config("workitem.olm_scalerdb", "checkpoint_interval_secs", 600)
            config.update_config("workitem.scalerdb_foreground", "checkpoint_interval_secs", 600)
            config.update_config("workitem.scalerdb_background", "checkpoint_interval_secs", 600)

    def set_connection_attempts(self, attempts):
        for config in self.cfg_flame:
            config.update_config("jobmanager", "connection_attempts", attempts, add=True)

    def unset_connection_attempts(self):
        for config in self.cfg_flame:
            config.remove_config("jobmanager", "connection_attempts")

    def set_timing_param(self):
        print 'Setting timing_params in all scaler nodes'
        for flame, scalerd in itertools.izip(self.cfg_flame, self.cfg_scalerd):
            scalerd.update_config("core", "object_ops.gc.allow_modified_settings", "true", add=True)
            for param in timing_params:
                scalerd.update_config("core", "object_ops.gc." + param, 1, add=True)  # 1 second
                flame.update_config("operation.gc_operation", param, 1, add=True)  # 1 second
            scalerd.update_config("core", "object_ops.gc.clock_drift_percentage", 10, add=True)
            flame.update_config("operation.gc_operation", "clock_drift_percentage", 10, add=True)
            scalerd.restart_component()

    def unset_timing_params(self):
        print 'Unsetting timing_params in all scaler nodes'
        for flame, scalerd in itertools.izip(self.cfg_flame, self.cfg_scalerd):
            for param in timing_params:
                scalerd.remove_config("core", "object_ops.gc." + param)
            scalerd.remove_config("core", "object_ops.gc.allow_modified_settings")
            scalerd.remove_config("core", "object_ops.gc.clock_drift_percentage")

            for param in timing_params:
                flame.remove_config("operation.gc_operation", param)
            flame.remove_config("operation.gc_operation", "clock_drift_percentage")
            scalerd.restart_component()

    def gc_enable(self):
        print 'Enabling GC in all scaler nodes'
        for config in self.cfg_scalerd:
            config.update_config("gc", "queue_policy", "immediate")
            config.update_config("gc", "queue_size", "5000")
            config.restart_component()

    def gc_disable(self):
        print 'Disabling GC in all scaler nodes'
        for config in self.cfg_scalerd:
            config.update_config("gc", "queue_policy", "discard")
            config.update_config("gc", "queue_size", "0")
            config.restart_component()

    def get_versioing_status(self):
        print 'Getting Versioning in all scaler nodes'
        versioning_status = []
        for config in self.cfg_scalerd:
            versioning_status.append(config.get_config_option("s3", "compatibility_version"))
        return versioning_status

    def reduce_resolve_internal_ids_cache_age(self, age=5):
        print 'Reducing ib_md_store.resolve_internal_ids_cache.max_age to ' + str(age) + ' sec'
        for config in self.cfg_scalerd:
            config.update_config('ib_md_store', 'resolve_internal_ids_cache.max_age', str(age))
            config.restart_component()

    def stop_flame_component(self, component):
        for scaler in self.scalers:
            print 'Stopping %s in %s' % (component, scaler.name)
            scaler.run_cmd('/etc/init.d/marvinservices stop %s' % component,
                           use_sudo=True)

    def restart_flame_component(self, component):
        for scaler in self.scalers:
            print 'Restarting %s in %s' % (component, scaler.name)
            scaler.run_cmd('/etc/init.d/marvinservices restart %s' % component,
                           use_sudo=True)

    def stop_mona(self):
        for scaler in self.scalers:
            print 'Stopping mona in %s' % scaler.name
            scaler.run_cmd('service mona stop', use_sudo=True)

    def start_mona(self):
        for scaler in self.scalers:
            print 'Starting mona in %s' % scaler.name
            scaler.run_cmd('service mona start', use_sudo=True)

    def stop_non_flame_component(self, component):
        for scaler in self.scalers:
            print 'Stopping %s in %s' % (component, scaler.name)
            scaler.run_cmd('/etc/init.d/marvinservices stop %s' % component,
                           use_sudo=True)

    def wait_for_flame_component_status(self, component, timeout=180):
        status = 0
        for scaler in self.scalers:
            wait_counter = timeout / 10
            while wait_counter > 0:
                output = scaler.run_cmd('/etc/init.d/marvinservices status %s' % component,
                                        use_sudo=True, warn_only=True)
                if 'is running' in output:
                    status += 1
                    break
                else:
                    wait_counter -= 1
                    time.sleep(30)
        return True if status >= 2 else False

    def get_backend_uploader_dir(self):
        return self.cfg_flame[0].get_config_option('backend_uploader', 'sources_dir')

    def browse_reports_for_file(self, file_ext):
        file_exists = False
        count = 0
        report_local = []
        backend_dir = self.get_backend_uploader_dir()
        for node in self.scalers:
            print 'In %s' % node.name
            list_dir = node.run_cmd('ls %s' % backend_dir, use_sudo=True)
            list_reports = list_dir.split('\s+')
            for file in list_reports:
                if file_ext in file:
                    file_exists = True
                    count += 1
                    report_local.append(file)
        return file_exists, count, report_local

    def clean_local_reports(self):
        backend_dir = self.get_backend_uploader_dir()
        for node in self.scalers:
            print 'Cleaning report in %s' % node.name
            node.run_cmd('rm -rf %s*' % backend_dir, use_sudo=True)
        return True

    def get_encrypt_status(self, section, option):
        return self.cfg_scalerd[0].get_config_option(section, option)

    def get_local_report_status(self, file_name):
        time.sleep(30)
        local_present = True
        time_out = 300
        while local_present and time_out >= 0:
            file_exists_local, sec_local_count, sec_report_local = self.browse_reports_for_file(file_name)
            if sec_local_count == 0:
                local_present = False
                break
            else:
                time.sleep(30)
                time_out -= 30
        return local_present

    def restore_root_cron(self):
        for scaler_node in self.scalers:
            scaler_node.run_cmd("sudo crontab -u root -l |"
                                "egrep -v '^\\* \\* \\* \\* \\*.*log' |"
                                "sudo crontab -u root -",
                                use_sudo=True)
            scaler_node.run_cmd('rm -f /tmp/root_cron', use_sudo=True)
            '''
            scaler_node.run_cmd("sudo crontab -r", use_sudo=True)
            scaler_node.run_cmd("crontab -u root /tmp/root_cron_b", use_sudo=True)
            scaler_node.run_cmd('rm -f /tmp/root_cron', use_sudo=True)
            scaler_node.run_cmd('rm -f /tmp/root_cron_b', use_sudo=True)
            '''


    def call_csv_upload(self, run_only=False):
        if run_only:
            for scaler_node in self.scalers:
                scaler_node.run_cmd('crontab -u root /tmp/root_cron', use_sudo=True)
        else:
            new_cron_capacity_entry = self.scalers[0].run_cmd("crontab -u root -l | grep bucket_capacity_report "
                                                              "| sed 's|^[^/]\+|* * * * * |'",
                                                              use_sudo=True)
            new_cron_encryption_entry = self.scalers[0].run_cmd("crontab -u root -l | grep bucket_encryption_keys  "
                                                                "| sed 's|^[^/]\+|* * * * * |'",
                                                                use_sudo=True)
            new_cron_metering_entry = self.scalers[0].run_cmd("crontab -u root -l | grep upload_metering "
                                                              "| sed 's|^\*/15[^/]\+|* * * * * |'",
                                                              use_sudo=True)
            new_cron_pending_error_entry = self.scalers[0].run_cmd("crontab -u root -l | grep object_verifier_report"
                                                              "| sed 's|^[^/]\+|* * * * * |'",
                                                              use_sudo=True)
            for scaler_node in self.scalers:
                scaler_node.run_cmd('crontab -u root -l > /tmp/root_cron', use_sudo=True)
                #scaler_node.run_cmd('crontab -u root -l > /tmp/root_cron_b', use_sudo=True)
                scaler_node.get_file('/tmp/root_cron', 'root_cron')
                with open('root_cron', 'a') as fp:
                    fp.write('%s\n' % new_cron_capacity_entry)
                    fp.write('%s\n' % new_cron_encryption_entry)
                    fp.write('%s\n' % new_cron_metering_entry)
                    fp.write('%s\n' % new_cron_pending_error_entry)
                scaler_node.put_file('root_cron', '/tmp/root_cron', use_sudo=True)
                scaler_node.run_cmd('crontab -u root /tmp/root_cron', use_sudo=True)
        return True

    def get_arakoon_master(self, ara_node):
        cfg = self.scalers[0].run_cmd('ls /opt/ampli/cfg/arakoon/{0}/{0}_*.cfg'.format(ara_node))
        cfg_content = BytesIO(self.scalers[0].get_file_contents(cfg))
        arakoon_config = Inifile(cfg_content)

        cluster_id = arakoon_config.getvalue('global', 'cluster_id')
        arakoon_nodes = arakoon_config.getvalue('global', 'cluster').split(',')

        nodes_ip_port_list = list()

        for node in arakoon_nodes:
            ip = arakoon_config.getvalue(node, 'ip').split(',')
            client_port = arakoon_config.getvalue(node, 'client_port')
            nodes_ip_port_list.append((node, ip, client_port))

        arakoon_client = ArakoonClusterClient(cluster_id, nodes_ip_port_list)
        who_master = arakoon_client.find_master()
        print 'Master Node for %s is %s' % (ara_node, who_master)
        return who_master

    def stop_arakoon_application(self, ara_nodes, groupstop=False):
        if groupstop:
            for scaler in self.scalers:
                print 'Brining down all Arakoon nodes in %s' % scaler.name
                scaler.run_cmd('/etc/init.d/marvinservices groupstop arakoon',
                               use_sudo=True)
            return True
        else:
            stopped_ara_nodes = []
            for scaler in self.scalers:
                new_ara_nodes = list(set(ara_nodes) - set(stopped_ara_nodes))
                output = scaler.run_cmd('/etc/init.d/marvinservices status | grep arakoon',
                                        use_sudo=True)
                for component in new_ara_nodes:
                    if component in output:
                        print 'Stopping %s in %s' % (component, scaler.name)
                        scaler.run_cmd('/etc/init.d/marvinservices stop %s' % component,
                                       use_sudo=True)
                        stopped_ara_nodes.append(component)
                    else:
                        continue
            return True if len(stopped_ara_nodes) == len(ara_nodes) else False


class FlameEncryption:

    def __init__(self, m):
        self.marvin_cli = m

    @staticmethod
    def read_key(filename):
        with open(filename, 'r') as myfile:
            data = myfile.read()
        return data

    def get_license_key(self):
        deployment_id = self.marvin_cli.environment.list()[0]['deployment_id']
        string_to_sign = 'LIC-ENCR1-' + str(deployment_id)
        uuid.UUID(string_to_sign[-36:])
        ss = string_to_sign.upper()
        data = self.read_key('cfg/secret_es_master.key')
        signing_key = ecdsa.SigningKey.from_pem(data)
        signature = signing_key.sign_deterministic(ss)
        license = SCHEME_VERSION_V1 + '\n' + signature + ss
        lk = '%s\n%s%s' % (BEGIN_MARKER, base64.encodestring(license), END_MARKER)
        license_key = ss + lk
        assert len(license_key) > 0, 'License key is not generated'
        return license_key

    def set_marvin_public_lic_verification_key(self):
        initial_status = '-- not set --'
        public_license_key_status = self.marvin_cli.environment.list()[0]['license_verification_key']
        marvin_lic_verification_key = self.read_key('cfg/public_es_verification.key')
        if public_license_key_status == md5(initial_status).hexdigest():
            self.marvin_cli.environment.update(self.marvin_cli.environment.list()[0]['guid'],
                                   license_verification_key=marvin_lic_verification_key)
        public_license_key_status = self.marvin_cli.environment.list()[0]['license_verification_key']
        assert public_license_key_status != initial_status, 'Could not update public license key to Marvin'

    def enable_encryption_from_marvin(self, license_key):
        self.set_marvin_public_lic_verification_key()
        self.marvin_cli.environment.update(self.marvin_cli.environment.list()[0]['guid'],
                                           encryption={"mode": 'ENCRYPT_EVERYTHING',
                                                       "license_key": license_key})
        time.sleep(180)

    def disable_encryption_from_marvin(self, license_key):
        self.set_marvin_public_lic_verification_key()
        self.marvin_cli.environment.update(self.marvin_cli.environment.list()[0]['guid'],
                                           encryption={"mode": 'ENCRYPT_NOTHING',
                                                       "license_key": license_key})
        time.sleep(180)


class MultiNodeOps:

    def __init__(self, env, scalers, scalers_mgmt, hw):
        self.env = env
        self.scalers = scalers
        self.scalers_mgmt = scalers_mgmt
        self.hw = hw

    def get_active_master_node(self):
        alive_node = None
        for port in ['9795', '9796']:
            master_found = False
            for node in self.scalers_mgmt:
                print 'Checking active master in node %s' % node
                output = node.run_cmd('curl http://localhost:%s/api/v1 | grep Status' % port,
                                      use_sudo=True, warn_only=True)
                if 'ALIVE' in output:
                    alive_node = node
                    master_found = True
            if master_found:
                break
        print 'ALIVE Node is %s' % alive_node
        return alive_node

    def validate_active_master(self, time_out=300):
        elected = False
        elapsed_time = 0
        active_node = None
        while not elected and elapsed_time < time_out:
            for port in ['9795', '9796']:
                for node in self.scalers_mgmt:
                    print 'Checking re-election of active master in node %s' % node
                    output = node.run_cmd('curl http://localhost:%s/api/v1 | grep Status' % port, use_sudo=True,
                                          warn_only=True)
                    if 'ALIVE' in output:
                        elected = True
                        active_node = node
                        break
                    time.sleep(20)
                time.sleep(10)
                elapsed_time += 30
                if elected:
                    break
        print 'ALIVE Node is %s' % active_node
        return elected

    def get_all_non_running_services(self, node):
        flame_services = ['sparkmaster', 'sparkexecutor', 'mongodb', 'arakoon', 'zookeeper', 'marvintaskmgr',
                          'keyrouter', 'scalerd', 'identitybridge', 'scalermgmt', 'marvinweb', 'scalerdbmgr']
        wait_for_svc = []
        out = node.run_cmd('/etc/init.d/marvinservices status', use_sudo=True, warn_only=True)
        list_status_svc = out.splitlines()
        del list_status_svc[0]
        del list_status_svc[-1]

        list_status_non_running_svc = [svc for svc in list_status_svc if " is not running" in svc]
        list_non_running_svc = [svc[:-len(" is not running")] for svc in list_status_non_running_svc]
        for svc in flame_services:
            for services in list_non_running_svc:
                if svc in services:
                    wait_for_svc.append(services)

        return wait_for_svc

    def check_all_marvin_services(self, node, start_manual):
        print 'Checking marvin services in %s' % node
        list_svc = self.get_all_non_running_services(node)
        if len(list_svc) == 0:
            return True
        else:
            print 'List of services not running : %s' % list_svc
            for svc in list_svc:
                print 'Waiting for %s to come up in %s' % (svc, node)
                assert self.wait_assert_marvin_services_status(node, svc, start_manual),\
                    'Unable to start %s to come up in %s' % (svc, node)

            time.sleep(10)
            list_svc = self.get_all_non_running_services(node)
            return True if len(list_svc) == 0 else False

    def wait_for_mona(self, node, time_out=480):
        print 'Checking mona service in %s' % node
        mona_status = False
        while not mona_status and time_out > 0:
            output = node.run_cmd('service mona status', use_sudo=True, warn_only=True)
            if 'start/running' in output:
                mona_status = True
                break
            else:
                time_out -= 30
                time.sleep(30)
        return mona_status

    def wait_assert_marvin_services_status(self, node, services, start_manual, time_out=480):
        service_status = False
        print 'Checking for %s status in %s' % (services, node)
        while not service_status and time_out > 0:
            output = node.run_cmd('/etc/init.d/marvinservices status %s' % services, use_sudo=True, warn_only=True)
            if 'is running' in output:
                service_status = True
            else:
                time_out -= 30
                time.sleep(30)

        if start_manual and not service_status:
            print '%s not automatically started in %s, hence starting manually.' % (services, node)
            output_start = node.run_cmd('/etc/init.d/marvinservices start %s' % services, use_sudo=True)
            if 'is running' in output_start:
                service_status = True
            else:
                service_status = False
        return service_status

    def check_health_scaler(self, node, start_manual=False):
        print 'Checking health in %s' % node
        assert self.wait_for_mona(node), 'Mona is not running in node %s' % node
        time.sleep(10)
        return self.check_all_marvin_services(node, start_manual)

    def stop_zookeeper_nodes(self):
        for node in self.scalers:
            print 'Stopping ZK in %s' % node
            output = self.env.get_machine(node).run_cmd('/etc/init.d/marvinservices status | grep zookeeper',
                                                        use_sudo=True, warn_only=True)
            zk_node = output.split('\s+')[0]
            self.env.get_machine(node).run_cmd('/etc/init.d/marvinservices stop %s' % zk_node, use_sudo=True)
        return True

    @staticmethod
    def stop_active_spark_master(node):
        print 'Stoping active master in %s' % node.name
        node.run_cmd('/etc/init.d/marvinservices stop sparkmaster',
                     use_sudo=True)
        return True

    def stop_spark_driver_instance(self, run_id, pattern, kill=True):
        process_id = None
        init_node = None
        for node in self.scalers:
            print 'Checking driver instance in %s' % node
            spark_driver_output = node.run_cmd("ps -ef | grep %s" % run_id, use_sudo=False)
            spark_driver = spark_driver_output.splitlines()

            if len(spark_driver) > 1 and pattern in spark_driver[0]:
                driver_process = re.split('\s+', spark_driver[0])
                process_id = driver_process[1] + ' ' + driver_process[2]
                init_node = self.env.get_machine(node).name
                print 'Driver ID %s is running in %s' % (process_id, init_node)
                if kill:
                    print 'Killing driver ID %s' % process_id
                    self.env.get_machine(node).run_cmd("kill -9 %s" % process_id, use_sudo=True)
                break
        return process_id, init_node

    @staticmethod
    def wait_assert_application_status(node, timeout=180):
        print 'Checking marvin services in %s' % node.name
        wait_counter = timeout / 10
        while wait_counter > 0:
            output = node.run_cmd('/etc/init.d/marvinservices status', use_sudo=True, warn_only=True)
            if 'done' in output:
                return True
            else:
                wait_counter -= 1
                time.sleep(30)
        return False

    def get_zk_leader(self):
        follower = False
        leader = False
        hosts = []
        client_port = None

        for node in self.scalers_mgmt:
            zk_cfg = node.run_cmd('ls /opt/ampli/cfg/zookeeper/zookeeper/*.cfg', use_sudo=True)
            cmd_output = node.run_cmd('cat %s' % zk_cfg, use_sudo=True)
            output = cmd_output.splitlines()
            for line in output:
                if 'clientPort=' in line:
                    ports = line.split('=')
                    client_port = ports[1]
                elif 'clientPortAddress=' in line:
                    host_addr = line.split('=')
                    hosts.append(host_addr[1])

        for host in hosts:
            print 'Checking ZK in %s' % host
            output = self.scalers[0].run_cmd('echo mntr | nc %s %s | grep zk_server_state' % (host, client_port))
            if 'follower' in output:
                follower = True
                print 'ZK is follower in %s' % host
            if 'leader' in output:
                leader = True
                print 'ZK is leader in %s' % host

        return leader, follower

    def check_health_of_all_nodes(self, restart=False):
        for node in self.scalers:
            marvin_status = self.check_health_scaler(node)
            if not marvin_status:
                print 'Not all marvin services are up and running in node %s' % node
                return False

        time.sleep(10) # safe time to check for the ZK to elect new leader if required
        leader, follower = self.get_zk_leader()
        if len(self.scalers) >= 3:
            if not leader:
                print 'Zookeeper leader not found.'
                return False
            time.sleep(10) # safe time to check for the ZK to elect new spark master if required
        if not self.get_active_master_node():
            print 'Alive master not found.'
            if restart:
                for node in self.scalers:
                    print 'Restarting spark master in %s' % node.name
                    node.run_cmd('/etc/init.d/marvinservices restart sparkmaster', use_sudo=True)
                time.sleep(10)
                if not self.validate_active_master():
                    print 'Alive master not found after restarting spark master.'
                    return False
            else:
                return False
        return True

class S3_Ops_Column(object):

    def __init__(self, env_info, backends, hw, account_name='devtest', sys_type= "as"):
        self.part_count = 0
        self.backends = backends
        self.system_bucket = env_info["configuration"]["s3"]["system_bucket"]
        self.system_account = env_info['configuration']["s3"]["system_account"]
        self.hw = hw
        self.sys_type = sys_type
        if self.sys_type is 'aws':
            self.api_key = 'AKIAIYPS4E763ZI75HSA'
            self.sec_key = 'Hx30NDmvG6RzV0lUT7dhKk61F6pJL1//HAAt+uLD'
        else:
            self.api_key = 's3user'
            self.sec_key = 's3pass'

    def get_s3_column_connection(self, access_key=None, secret_key=None, host=None, port=None):
        if access_key is None:
            access_key = self.api_key
        if secret_key is None:
            secret_key = self.sec_key
        if self.sys_type is 'aws':
            boto_conn = S3Connection(access_key, secret_key)
        else:

            if host is None:
                ipaddr = self.backends[0].exposed_ports['s3_http'].public_ip
                host = '127.0.0.1' if ipaddr == 'localhost' else ipaddr
            if port is None:
                port = self.backends[0].exposed_ports['s3_http'].public_port

            boto_conn = S3Connection(access_key, secret_key, host=host, port=port, is_secure=False,
                                     calling_format=OrdinaryCallingFormat())
        return boto_conn

    def delete_object(self, boto_connection, bucket_name, key):
        if self.hw:
            python_script = ('\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             'response = conn.make_request("DELETE", bucket="{2}", key="{3}")\n'
                             'print response.msg.get("x-amz-request-id") if int(response.status) == 204 else None'
                             .format(self.api_key, self.sec_key, bucket_name, key))
            with hide('running'):
                fab_run = self.scalers[0].run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
            response = fab_run.stdout.splitlines()[-1]
            return response
        else:
            try:
                response = boto_connection.make_request('DELETE', bucket=bucket_name, key=key)
                return response.msg.get('x-amz-request-id'), response.status, response.reason
            except Exception as exc:
                print 'exception: {} {}'.format(type(exc), exc)

    def upload_single_object(self, boto_connection, bucket_name, key, data):
        scaler = random.choice(self.scalers)
        if self.hw:
            python_script = ('\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             'response = conn.make_request("PUT", bucket="{2}", key="{3}", data="{4}")\n'
                             'print response.msg.get("x-amz-request-id") if int(response.status) == 200 else None'
                             .format(self.api_key, self.sec_key, bucket_name, key, data))
            with hide('running'):
                fab_run = scaler.run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
            response = fab_run.stdout.splitlines()[-1]
            return response
        else:
            try:
                response = boto_connection.make_request('PUT', bucket=bucket_name, key=key, data=data)
                return response.msg.get('x-amz-request-id'), response.status, response.reason, response.msg.get('x-amz-version-id')
            except Exception as exc:
                print 'exception: {} {}'.format(type(exc), exc)

    def get_object_size(self, boto_connection, bucket_name, key):
        if self.hw:
            python_script = ('\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             'response = conn.make_request("DELETE", bucket="{2}", key="{3}")\n'
                             'print response.msg.get("x-amz-request-id") if int(response.status) == 204 else None'
                             .format(self.api_key, self.sec_key, bucket_name, key))
            with hide('running'):
                fab_run = self.scalers[0].run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
            response = fab_run.stdout.splitlines()[-1]
            return response
        else:
            try:
                bucket_key = boto_connection.get_bucket(bucket_name)
                object_key = bucket_key.lookup(key)
            except Exception as exc:
                print 'exception: {} {}'.format(type(exc), exc)
            if object_key is None:
                #object does not exist
                return None, None
            else:
                return object_key.size, object_key.etag

class S3_Ops(object):

    def __init__(self, env_info, scalers, hw, account_name='devtest',  sys_type= "as"):
        self.part_count = 0
        self.scalers = scalers
        self.system_bucket = env_info["configuration"]["s3"]["system_bucket"]
        self.system_account = env_info['configuration']["s3"]["system_account"]
        self.hw = hw
        self.sys_type = sys_type
        if self.sys_type is 'aws':
            self.api_key = 'AKIAIYPS4E763ZI75HSA'
            self.sec_key = 'Hx30NDmvG6RzV0lUT7dhKk61F6pJL1//HAAt+uLD'
        else:
            python_script = ('\n'
                             'import json\n'
                             'from sherpa import cli_wrapper as cli\n'
                             'account_id_opt = cli.clients.scalerim.identitiesGetByEmail("", ["{0}@hgst.com"])[0]\n'
                             'if not account_id_opt.identity:\n'
                             '    account_id = cli.clients.scalerim.accountCreate("", "{0}", "{0}@hgst.com")\n'
                             'else:\n'
                             '    account_id = account_id_opt.identity\n'
                             'if not account_id.apiKeys:\n'
                             '    cli.clients.scalerim.apiKeyGenerate("", account_id.canonicalId)\n'
                             'account_id_opt = cli.clients.scalerim.identitiesGetByEmail("", ["{0}@hgst.com"])[0]\n'
                             'account_apikey = cli.clients.scalerim.apiKeyGet("", account_id_opt.identity.apiKeys[0].accessKey)\n'
                             'accountkeys = dict()\n'
                             'accountkeys["s3key"] = account_apikey.accessKey\n'
                             'accountkeys["canonical_id"] = account_id.canonicalId\n'
                             'accountkeys["s3secret"] = account_apikey.secretKey\n'
                             'print "{{}}".format(json.dumps(accountkeys))\n'.format(account_name))
            with hide('running'):
                fab_run = self.scalers[0].run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
            fab_run_stdout_lastline = fab_run.stdout.splitlines()[-1]
            accountkeys = json.loads(fab_run_stdout_lastline)
            self.api_key = accountkeys['s3key']
            self.sec_key = accountkeys['s3secret']
            self.canonical_id = accountkeys['canonical_id']

    def get_s3_connection(self, access_key=None, secret_key=None, host=None, port=None):
        if access_key is None:
            access_key = self.api_key
        if secret_key is None:
            secret_key = self.sec_key
        if self.sys_type is 'aws':
            boto_conn = S3Connection(access_key, secret_key)
        else:
            if host is None:
                ipaddr = self.scalers[0].exposed_ports['s3_http'].public_ip
                host = '127.0.0.1' if ipaddr == 'localhost' else ipaddr
            if port is None:
                port = self.scalers[0].exposed_ports['s3_http'].public_port

            boto_conn = S3Connection(access_key, secret_key, host=host, port=port, is_secure=False,
                                     calling_format=OrdinaryCallingFormat())
        return boto_conn

    def get_boto3_connection(self, access_key=None, secret_key=None, region_name=None):
        if access_key is None:
            access_key = self.api_key
        if secret_key is None:
            secret_key = self.sec_key
        if region_name is None:
            region_name = 'us-east-1'
        if self.sys_type is 'aws':
            boto_conn = boto3.client(service_name='s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key,
                                     region_name=region_name)
        else:
            ipaddr = self.scalers[0].exposed_ports['s3_http'].public_ip
            host = '127.0.0.1' if ipaddr == 'localhost' else ipaddr
            port = self.scalers[0].exposed_ports['s3_http'].public_port
            boto_conn = boto3.client(service_name='s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key,
                                     endpoint_url='http://%s:%s' % (host, port),
                                     config=botocore.config.Config(region_name='us-west-2'))
        return boto_conn

    def set_bucket_replication(self, boto_conn, src_bucket, dst_bucket, status='Enabled'):
        response = boto_conn.put_bucket_replication(
            Bucket=src_bucket, ReplicationConfiguration={'Role': 's3-replication-role',
                                                         'Rules': [{'ID': (''.join([choice(string.hexdigits) for n in xrange(40)])).lower(),
                                                                    'Prefix': '', 'Status': status,
                                                                    'Destination': {
                                                                        'Bucket': 'arn:aws:s3:::%s' % dst_bucket,
                                                                        'StorageClass': 'STANDARD'}}]})
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200, 'Replication not enabled on %s, status is %s' \
                                                                      % (src_bucket,
                                                                         response['ResponseMetadata']['HTTPStatusCode'])

    def get_credentials(self):
        return self.api_key, self.sec_key

    def create_bucket(self, boto_connection, bucket_name=None):
        if bucket_name is None:
            bucket_name = 'bucket-%s' % uuid4()
        bucket = boto_connection.create_bucket(bucket_name)
        if self.sys_type is not 'aws':
            bucket.add_user_grant('FULL_CONTROL', self.canonical_id)
        return bucket, bucket_name

    def create_bucket_with_location(self, boto_connection, bucket_name=None, location=None):
        if bucket_name is None:
            bucket_name = 'bucket-%s' % uuid4()
        if location is None:
            location = 'Location.EU'
        bucket = boto_connection.create_bucket(bucket_name, location=location)
        if self.sys_type is not 'aws':
            bucket.add_user_grant('FULL_CONTROL', self.canonical_id)
        return bucket, bucket_name

    def add_user_grant_acl(self, connection, bucket_name, canonical_id, permission):
        """
        It sets the user permission for a given bucket
        :param connection: connection is used for s3 operation
        :param bucket_name: bucket_name is to retrieve the bucket from the connection
        :param canonical_id: canonical_id is to identity of the user
        :param permission: permission is to set the following values (FULL_CONTROL, READ and WRITE)
        """
        bucket = connection.lookup(bucket_name)
        assert bucket.name == bucket_name, "There is no bucket \'%s\' found" % bucket_name
        bucket.add_user_grant(permission, canonical_id)

    def put_bucket(self, boto_connection, bucket_name):
        if self.hw:
            python_script = ('\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             'response = conn.make_request("PUT", bucket="{2}")\n'
                             'print response.msg.get("x-amz-request-id") if int(response.status) == 200 else None'
                             .format(self.api_key, self.sec_key, bucket_name))
            with hide('running'):
                fab_run = self.scalers[0].run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
            response = fab_run.stdout.splitlines()[-1]
            return response
        else:
            try:
                response = boto_connection.make_request('PUT', bucket=bucket_name)
                return response.msg.get('x-amz-request-id'), response.status, response.reason
            except Exception as exc:
                print 'exception: {} {}'.format(type(exc), exc)

    def upload_single_object(self, boto_connection, bucket_name, key, data):
        scaler = random.choice(self.scalers)
        if self.hw:
            python_script = ('\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             'response = conn.make_request("PUT", bucket="{2}", key="{3}", data="{4}")\n'
                             'print response.msg.get("x-amz-request-id") if int(response.status) == 200 else None'
                             .format(self.api_key, self.sec_key, bucket_name, key, data))
            with hide('running'):
                fab_run = scaler.run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
            response = fab_run.stdout.splitlines()[-1]
            return response
        else:
            try:
                response = boto_connection.make_request('PUT', bucket=bucket_name, key=key, data=data)
                print "............",response.msg
                return response.msg.get('x-amz-request-id'), response.status, response.reason, response.msg.get('x-amz-version-id')
            except Exception as exc:
                print 'exception: {} {}'.format(type(exc), exc)

    def get_object(self, boto_connection, bucket_name, key):
        if self.hw:
            python_script = ('\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             'response = conn.make_request("GET", bucket="{2}", key="{3}")\n'
                             'print response.msg.get("x-amz-request-id") if int(response.status) == 200 else None'
                             .format(self.api_key, self.sec_key, bucket_name, key))
            with hide('running'):
                fab_run = self.scalers[0].run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
            response = fab_run.stdout.splitlines()[-1]
            return response
        else:
            try:
                response = boto_connection.make_request('GET', bucket=bucket_name, key=key)
                print "............",response.msg
                return response.msg.get('x-amz-request-id'), response.status, response.reason
            except Exception as exc:
                print 'exception: {} {}'.format(type(exc), exc)

    def delete_object(self, boto_connection, bucket_name, key):
        if self.hw:
            python_script = ('\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             'response = conn.make_request("DELETE", bucket="{2}", key="{3}")\n'
                             'print response.msg.get("x-amz-request-id") if int(response.status) == 204 else None'
                             .format(self.api_key, self.sec_key, bucket_name, key))
            with hide('running'):
                fab_run = self.scalers[0].run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
            response = fab_run.stdout.splitlines()[-1]
            return response
        else:
            try:
                response = boto_connection.make_request('DELETE', bucket=bucket_name, key=key)
                return response.msg.get('x-amz-request-id'), response.status, response.reason
            except Exception as exc:
                print 'exception: {} {}'.format(type(exc), exc)

    def get_bucket_info(self, boto_connection, bucket_name):
        if self.hw:
            python_script = ('\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             'response = conn.make_request("GET", bucket="{2}")\n'
                             'print response.msg.get("x-amz-request-id") if int(response.status) == 200 else None'
                             .format(self.api_key, self.sec_key, bucket_name))
            with hide('running'):
                fab_run = self.scalers[0].run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
            response = fab_run.stdout.splitlines()[-1]
            return response
        else:
            try:
                response = boto_connection.make_request('GET', bucket=bucket_name)
                return response.msg.get('x-amz-request-id'), response.status, response.reason
            except Exception as exc:
                print 'exception: {} {}'.format(type(exc), exc)

    def delete_bucket(self, boto_connection, bucket_name):
        if self.hw:
            python_script = ('\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             'bucket = conn.get_bucket("{2}")\n'
                             'bucket.delete_keys(bucket.get_all_keys())\n'
                             'conn.delete_bucket(bucket)'.format(self.api_key, self.sec_key, bucket_name))
            with hide('running'):
                self.scalers[0].run_cmd("/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
        else:
            bucket = boto_connection.get_bucket(bucket_name)
            bucket.delete_keys(bucket.get_all_keys())
            boto_connection.delete_bucket(bucket)

    def delete_all_versions(self, boto_connection, bucket_name):
        if self.hw:
            python_script = ('\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             'bucket = conn.get_bucket("{2}")\n'
                             'obj_version_id_upload = dict()\n'
                             'a = bucket.get_all_versions()\n'
                             'for id in a:\n'
                             '    obj_version_id_upload[id.version_id] = id.name\n'
                             'for key, value in obj_version_id_upload.iteritems():\n'
                             '    bucket.delete_key(value, version_id=key)\n'
                             'print bucket.get_all_keys()'.format(self.api_key, self.sec_key, bucket_name))
            with hide('running'):
                self.scalers[0].run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
        else:
            buck_obj = boto_connection.get_bucket(bucket_name)
            obj_version_id_upload = {}
            a = buck_obj.get_all_versions()
            for id in a:
                obj_version_id_upload[id.version_id] = id.name
            for key, value in obj_version_id_upload.iteritems():
                buck_obj.delete_key(value, version_id=key)

    def configure_versioning_bucket(self, boto_connection, bucket_name):
        if self.hw:
            python_script = ('\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             'bucket = conn.get_bucket("{2}")\n'
                             'bucket.configure_versioning(versioning=True)\n'
                             'print bucket.get_versioning_status()["Versioning"]'.format(self.api_key, self.sec_key, bucket_name))
            with hide('running'):
                fab_run = self.scalers[0].run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
            response = fab_run.stdout.splitlines()[-1]
            return response
        else:
            try:
                bucket = boto_connection.get_bucket(bucket_name)
                bucket.configure_versioning(versioning=True)
                return bucket.get_versioning_status()["Versioning"]
            except Exception as exc:
                print 'exception: {} {}'.format(type(exc), exc)

    def configure_lifecycle_bucket(self, boto_connection, bucket_name, lifecycle_rules):
        now = datetime.datetime.now()
        prev_days = datetime.timedelta(days=30)
        past_date = now - prev_days
        past_date = past_date.replace(hour=0, minute=0, second=0, microsecond=0)
        iso_format = past_date.isoformat()
        if self.hw:
            python_script = ('\n'
                             'from uuid import uuid4\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'from boto.s3.lifecycle import Lifecycle, Rule, Expiration\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             'bucket = conn.get_bucket("{2}")\n'
                             'lifecycle = Lifecycle()\n'
                             'for l in range({3}):\n'
                             '    if l == 0:\n'
                             '        expiration = Expiration(date="{4}")\n'
                             '        date_rule = Rule(id="rule%s" % l, prefix="obj", status="Enabled", expiration=expiration)\n'
                             '    else:\n'
                             '        expiration = Expiration(date="{4}")\n'
                             '        date_rule = Rule(id="rule%s" % l, prefix="%s" % uuid4(), status="Enabled", expiration=expiration)\n'
                             '    lifecycle.append(date_rule)\n'
                             'bucket.configure_lifecycle(lifecycle)\n'
                             'get_lifecycle = bucket.get_lifecycle_config()\n'
                             'print len(get_lifecycle)'.format(self.api_key, self.sec_key, bucket_name, lifecycle_rules, iso_format))
            with hide('running'):
                fab_run = self.scalers[0].run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
            response = fab_run.stdout.splitlines()[-1]
            return response
        else:
            lifecycle = Lifecycle()
            for l in range(lifecycle_rules):
                if l == 0:
                    date_rule = self.set_lifecycle_with_date('rule%s' % l, prefixes='obj', format=iso_format)
                else:
                    date_rule = self.set_lifecycle_with_date('rule%s' % l, prefixes='%s' % uuid4(), format=iso_format)
                lifecycle.append(date_rule)
            try:
                bucket = boto_connection.get_bucket(bucket_name)
                bucket.configure_lifecycle(lifecycle)
                return len(bucket.get_lifecycle_config())
            except Exception as exc:
                print 'exception: {} {}'.format(type(exc), exc)

    def set_lifecycle_with_date(self, id, prefixes, format):
        expiration = Expiration(date=format)
        date_rule = Rule(id=id, prefix=prefixes, status='Enabled', expiration=expiration)
        return date_rule

    @staticmethod
    def create_bigfile(fileName, fileSizeinBytes):
        with open(fileName, "wb") as bigfile:
            bigfile.seek(fileSizeinBytes - 1)
            bigfile.write("\0")
        return fileName

    def multipart_upload_file(self, bucket, source_path, source_size, chunk_size, abort):
        mp = bucket.initiate_multipart_upload(os.path.basename(source_path))

        chunk_count = int(math.ceil(source_size / float(chunk_size)))

        for i in range(chunk_count):
            offset = chunk_size * i
            bytes = min(chunk_size, source_size - offset)
            try:
                with FileChunkIO(source_path, 'r', offset=offset, bytes=bytes) as fp:
                    mp.upload_part_from_file(fp, part_num=i + 1)
                self.part_count += 1
                if abort and (i > chunk_count / 2):
                    # abort the upload
                    mp.cancel_upload()
                    return True, self.part_count
            except Exception:
                return False, 0

        # Finish the upload
        mp.complete_upload()
        return True, self.part_count

    def upload_multipart_object(self, bucket, file_path, file_size, chunk_size, abort=False):
        source_path = self.create_bigfile(file_path, file_size)
        source_size = os.stat(source_path).st_size
        status, part_count = self.multipart_upload_file(bucket, source_path, source_size, chunk_size, abort)
        return status, part_count

    def get_system_bucket_info(self):
        python_script = ('\n'
                         'import json\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'account_id_opt = cli.clients.scalerim.identitiesGetByEmail("", ["{0}"])[0]\n'
                         'account_apikey = cli.clients.scalerim.apiKeyGet("", account_id_opt.identity.apiKeys[0].accessKey)\n'
                         'accountkeys = dict()\n'
                         'accountkeys["s3key"] = account_apikey.accessKey\n'
                         'accountkeys["s3secret"] = account_apikey.secretKey\n'
                         'print "{{}}".format(json.dumps(accountkeys))\n'.format(self.system_account))
        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
        fab_run_stdout_lastline = fab_run.stdout.splitlines()[-1]
        sys_account = json.loads(fab_run_stdout_lastline)
        return sys_account['s3key'], sys_account['s3secret']

    def browse_system_bucket_for_file(self, file_ext=None, clean=False):
        access_key, secret_key = self.get_system_bucket_info()
        boto_conn = self.get_s3_connection(access_key=access_key, secret_key=secret_key)
        bucket = boto_conn.get_bucket(self.system_bucket)
        file_do_exist = False

        if clean:
            if self.hw:
                python_script = ('\n'
                                 'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                                 'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                                 'bucket = conn.get_bucket("{2}")\n'
                                 'bucket.delete_keys(bucket.get_all_keys())\n'
                                 'conn.delete_bucket(bucket)'.format(access_key, secret_key, self.system_bucket))
                with hide('running'):
                    self.scalers[0].run_cmd(
                        "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
                return file_do_exist, 0
            else:
                bucket.delete_keys([key.name for key in bucket.list()])
                return file_do_exist, 0
        out = []
        count = 0
        if self.hw:
            python_script = ('\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             'bucket = conn.get_bucket("{2}")\n'
                             'out = [key.name.encode("utf-8") for key in bucket.list()]\n'
                             'inc = [key.endswith("{3}") for key in out]\n'
                             'count = 0\n'
                             'file_do_exist = False\n'
                             'for value in inc:\n'
                             '    if value:\n'
                             '        file_do_exist = True\n'
                             '        count += 1\n'
                             'print file_do_exist\n'
                             'print count'.format(access_key, secret_key, self.system_bucket, file_ext))
            with hide('running'):
                fab_run = self.scalers[0].run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
            out = fab_run.stdout.splitlines()
            count = int(out[-1])
            file_do_exist = out[-2]
            return file_do_exist, count
        else:
            for key in bucket.list():
                out.append(key.name.encode('utf-8'))
            inc = [key.endswith(file_ext) for key in out]
            for value in inc:
                if value:
                    file_do_exist = True
                    count += 1
            return file_do_exist, count

    def get_csv_contents(self, report):
        access_key, secret_key = self.get_system_bucket_info()
        if self.hw:
            python_script = ('\n'
                             'import zlib, csv\n'
                             'from boto.s3.connection import S3Connection, OrdinaryCallingFormat\n'
                             'conn = S3Connection("{0}", "{1}", host="127.0.0.1", port=80, is_secure=False, calling_format=OrdinaryCallingFormat())\n'
                             's3systembucket = conn.get_bucket("{2}")\n'
                             'encryption_report = ""\n'
                             'report_prefix = "reports/{3}"\n'
                             'for encryption_report in s3systembucket.list(prefix=report_prefix):\n'
                             '    pass\n'
                             'mylist = []\n'
                             'if encryption_report:\n'
                             '    unzipped_data = zlib.decompress(encryption_report.get_contents_as_string(),15 + 32)\n'
                             '    csvfile = csv.DictReader(unzipped_data.splitlines())\n'
                             '    for rows in csvfile:\n\n'
                             '        mylist.append(rows)\n'
                             '    print mylist\n'
                             'else:\n'
                             '    print "encryption CSV not found in system bucket"\n'
                             .format(access_key, secret_key, self.system_bucket, report))
            with hide('running'):
                fab_run = self.scalers[0].run_cmd(
                    "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
            csvfile = ast.literal_eval(fab_run.stdout.splitlines()[-1])
            return csvfile
        else:
            system_s3 = self.get_s3_connection(access_key=access_key, secret_key=secret_key)
            s3systembucket = system_s3.get_bucket(self.system_bucket)
            encryption_report = ''
            report_prefix = 'reports/%s' % report
            for encryption_report in s3systembucket.list(prefix=report_prefix):
                pass
            if encryption_report:
                unzipped_data = zlib.decompress(encryption_report.get_contents_as_string(), 15 + 32)
                csvfile = csv.DictReader(unzipped_data.splitlines())
                return csvfile
            else:
                assert encryption_report, "encryption CSV not found in system bucket"


class ScalerKeyrouter(object):

    def __init__(self, scalers):
        self.scalers = scalers

    def get_bl_entries(self, bucket_name):
        python_script = ('\n'
                         'import json\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_BucketLifecycle\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N%s"), SDB_KeyOption("N%s"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'prefix = sdb_bucket_id.id\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("L"+prefix), SDB_KeyOption("L"+prefix),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_life_cycle = SDB_BucketLifecycle()\n'
                         'sdb_bucket_life_cycle.read(p)\n'
                         'def serialize_instance(obj):\n'
                         '  d = { "__classname__" : type(obj).__name__ }\n'
                         '  d.update(vars(obj))\n'
                         '  return d\n'
                         'print json.dumps(sdb_bucket_life_cycle, default=serialize_instance)' % (
                             bucket_name, bucket_name))
        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '%s'" % (python_script))
        bucket_bl_str = fab_run.stdout.splitlines()[-1]
        bucket_bl = json.loads(bucket_bl_str)
        return bucket_bl

    def get_raw_bucket_id(self, bucket_name):
        python_script = ('\n'
                         'import json\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_BucketLifecycle\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N%s"), SDB_KeyOption("N%s"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'print sdb_bucket_id.id' % (bucket_name, bucket_name))
        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '%s'" % (python_script))
        raw_bucket_id = fab_run.stdout.splitlines()[-1]
        return raw_bucket_id

    def get_bi_entries(self, bucket_name):
        python_script = ('\n'
                         'import json, cPickle as pickle\n'
                         'import json\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Bucket, SDB_BucketLifecycle\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N%s"), SDB_KeyOption("N%s"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'original_bucket = cli.clients.keyrouter.get("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, "I" + str(sdb_bucket_id.id))\n'
                         't1 = TTransport.TMemoryBuffer(original_bucket.value.blob)\n'
                         'p1 = TCompatibleCompactProtocol(t1)\n'
                         'sdb_bucket = SDB_Bucket()\n'
                         'sdb_bucket.read(p1)\n'
                         'pickle.dump(sdb_bucket, open(\"txt.pkl\", \"wb\"))\n'
                         'print original_bucket' % (bucket_name, bucket_name))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '%s'" % (python_script))

        bucket_bi_list = fab_run.stdout.splitlines()[-1]
        return bucket_bi_list

    def restore_bi_entries(self, bucket_name, row, raw_bkt_id):
        print row
        python_script = ('\n'
                         'import json\n'
                         'import binascii, base64, time\n'
                         'import json, cPickle as pickle\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'import scalerdb_api.common.ttypes as SC\n'
                         'import scalerdb_api.values.ttypes as SV\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Bucket, SDB_BucketLifecycle\n'
                         'from scaler_api.scalerdb import serialize\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'now = time.time()\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N%s"), SDB_KeyOption("N%s"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'secure_metadata_container = SV.SDB_SecureMetaDataContainer(\n'
                         '               secureMetaDataEncryptionKeyId=int(%s),\n'
                         '               secureMetaDataIV=base64.b64decode("%s"),\n'
                         '               secureMetaData=base64.b64decode("%s"))\n'
                         'restored_bucket = SV.SDB_Bucket(\n'
                         '               creationTime=now, modificationTime=now, owner="A" + binascii.unhexlify("%s"),\n'
                         '               name="%s",status=SV.SDB_BucketStatusEnum_t.ACTIVE, permissions=None,\n'
                         '               secureMetaDataContainer=secure_metadata_container, tag="%s",\n'
                         '               overlayColumnId=None,\n'
                         '               permissionList=[SV.SDB_Grant("A" + binascii.unhexlify("%s"),15)])\n'
                         'restored_value = SC.SDB_Value(sequenceId=0,version=2, type=SC.SDB_ValueTypeEnum_t.BUCKET, blob=serialize(restored_bucket))\n'
                         'original_bucket = cli.clients.keyrouter.put("test", SDB_SpaceEnum_t.BUCKET_SPACE, "I" + str(sdb_bucket_id.id), restored_value)\n'
                         'original_bucket = cli.clients.keyrouter.get("test", SDB_SpaceEnum_t.BUCKET_SPACE, "I" + str(sdb_bucket_id.id))\n'
                         'print original_bucket' % (
                             bucket_name, bucket_name, row['Secure Metadata Encryptionkey ID'],
                             row['Secure Metadata IV'],
                             row['Secure Metadata'], row['Bucket Owner'][2:],
                             row['Bucket Name'], row['Bucket ID'], row['Bucket Owner'][2:]))
        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '%s'" % (python_script))

        bucket_bi = fab_run.stdout.splitlines()[-1]
        return bucket_bi

    def put_bi_entries(self, bucket_name, original_bucket):
        python_script = ('\n'
                         'import json\n'
                         'import json, cPickle as pickle\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption, SDB_Value\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_BucketLifecycle\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N%s"), SDB_KeyOption("N%s"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'sdb_bkt_load = pickle.load(open(\"txt.pkl\", \"rb\"))\n'
                         'transport = TTransport.TMemoryBuffer()\n'
                         'protocol = TCompatibleCompactProtocol(transport)\n'
                         'sdb_bkt_load.write(protocol)\n'
                         'blob = transport.getvalue()\n'
                         'value = SDB_Value(sequenceId = 0, version=2, type=1, blob=blob)\n'
                         'original_bucket = cli.clients.keyrouter.put("flame", SDB_SpaceEnum_t.BUCKET_SPACE, "I" + str(sdb_bucket_id.id), value)\n'
                         'print original_bucket' % (bucket_name, bucket_name))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '%s'" % (python_script))

        bucket_bi = fab_run.stdout.splitlines()[-1]
        return bucket_bi

    def remove_bi_entries(self, bucket_name):
        python_script = ('\n'
                         'import json\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_BucketLifecycle\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N%s"), SDB_KeyOption("N%s"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'original_bucket = cli.clients.keyrouter.remove("flame", SDB_SpaceEnum_t.BUCKET_SPACE, "I" + str(sdb_bucket_id.id))\n'
                         'print original_bucket' % (bucket_name, bucket_name))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '%s'" % (python_script))

        bucket_bi = fab_run.stdout.splitlines()[-1]
        return bucket_bi

    def restore_bi_entries_versioning(self, bucket_name, row):
        print row, row['Versioning Status']
        python_script = ('\n'
                         'import json\n'
                         'import binascii, base64, time\n'
                         'import json, cPickle as pickle\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'import scalerdb_api.common.ttypes as SC\n'
                         'import scalerdb_api.values.ttypes as SV\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Bucket, SDB_BucketLifecycle\n'
                         'from scaler_api.scalerdb import serialize\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'now = time.time()\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N%s"), SDB_KeyOption("N%s"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'secure_metadata_container = SV.SDB_SecureMetaDataContainer(\n'
                         '               secureMetaDataEncryptionKeyId=int(%s),\n'
                         '               secureMetaDataIV=base64.b64decode("%s"),\n'
                         '               secureMetaData=base64.b64decode("%s"))\n'
                         'versioningStatus = {"disabled": 1, "enabled": 2, "suspended": 3}\n'
                         'restored_bucket = SV.SDB_Bucket(\n'
                         '               creationTime=now, modificationTime=now, owner="A" + binascii.unhexlify("%s"),\n'
                         '               name="%s",status=SV.SDB_BucketStatusEnum_t.ACTIVE, permissions=None,\n'
                         '               secureMetaDataContainer=secure_metadata_container, tag="%s",\n'
                         '               overlayColumnId=None,\n'
                         '               permissionList=[SV.SDB_Grant("A" + binascii.unhexlify("%s"),15)],\n'
                         '               versioningStatus=versioningStatus["%s"])\n'
                         'restored_value = SC.SDB_Value(sequenceId=0,version=2, type=SC.SDB_ValueTypeEnum_t.BUCKET, blob=serialize(restored_bucket))\n'
                         'original_bucket = cli.clients.keyrouter.put("test", SDB_SpaceEnum_t.BUCKET_SPACE, "I" + str(sdb_bucket_id.id), restored_value)\n'
                         'original_bucket = cli.clients.keyrouter.get("test", SDB_SpaceEnum_t.BUCKET_SPACE, "I" + str(sdb_bucket_id.id))\n'
                         'print original_bucket' % (
                             bucket_name, bucket_name, row['Secure Metadata Encryptionkey ID'],
                             row['Secure Metadata IV'],
                             row['Secure Metadata'], row['Bucket Owner'][2:],
                             row['Bucket Name'], row['Bucket ID'], row['Bucket Owner'][2:], row['Versioning Status']))
        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '%s'" % (python_script))
        print python_script

        bucket_bi = fab_run.stdout.splitlines()[-1]
        return bucket_bi

    def iterate_bucket_objects(self, bucket_name, vtype, during):
        python_script = ('\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'prefix = sdb_bucket_id.id + "{1}"\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, prefix, prefix, False, None, 1000)\n'
                         'mylist = [entry.key for entry in list_result.entries]\n'
                         'print mylist'.format(bucket_name, vtype))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
        entries_dict = ast.literal_eval(fab_run.stdout.splitlines()[-1])
        self.display_key_spaces(entries_dict, vtype, during)
        return entries_dict

    def iterate_versioning_bucket_objects(self, bucket_name, vtype, during):
        python_script = ('\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'prefix = sdb_bucket_id.id\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, prefix, prefix, False, None, 1000)\n'
                         'mylist = [entry.key for entry in list_result.entries]\n'
                         'print mylist'.format(bucket_name))
        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
        entries_dict = ast.literal_eval(fab_run.stdout.splitlines()[-1])
        self.display_key_spaces(entries_dict, vtype, during)
        return entries_dict

    def iterate_versioning_backend_bucket_objects(self, bucket_name, vtype, during, object_index=0):
        python_script = ('\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Object\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'prefix = sdb_bucket_id.id\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, prefix, prefix, False, None, 1000)\n'
                         't = TTransport.TMemoryBuffer(list_result.entries[{2}].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_object = SDB_Object()\n'
                         'sdb_object.read(p)\n'
                         'print sdb_object.singlePart.columnPath '.format(bucket_name, vtype, object_index))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
        entries_dict = fab_run.stdout.splitlines()[-1]
        return entries_dict

    def iterate_versioning_multipart_backend_bucket_objects(self, bucket_name, vtype, during, object_index, part_number):
        python_script = ('\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Object\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'prefix = sdb_bucket_id.id\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, prefix, prefix, False, None, 1000)\n'
                         't = TTransport.TMemoryBuffer(list_result.entries[{3}].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_object = SDB_Object()\n'
                         'sdb_object.read(p)\n'
                         'print sdb_object.singlePart.columnPath '.format(bucket_name, vtype, object_index,
                                                                          part_number))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
        entries_dict = fab_run.stdout.splitlines()[-1]
        return entries_dict

    def iterate_versioning_backend_bucket_objects_size(self, bucket_name, vtype, during, object_index=0):
        python_script = ('\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Object\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'prefix = sdb_bucket_id.id\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, prefix, prefix, False, None, 1000)\n'
                         't = TTransport.TMemoryBuffer(list_result.entries[{2}].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_object = SDB_Object()\n'
                         'sdb_object.read(p)\n'
                         'print sdb_object.singlePart.size'.format(bucket_name, vtype, object_index))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
        entries_dict = fab_run.stdout.splitlines()[-1]
        return entries_dict

    def remove_one_part_object(self, bucket_name, vtype, part_number=0):
        """
        Using keyrouter API, remove one the part in the multi part object, using part key
        :param bucket_name: bucket name
        :param vtype: version
        :param object_index: object part index number
        :return: string (which contains the key of the part object)
        """
        python_script = ('\n'
                         'import keyrouter_api.ttypes as kt\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Object\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'prefix = sdb_bucket_id.id\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, prefix, prefix, False, None, 1000)\n'
                         'original_bucket = cli.clients.keyrouter.remove("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, list_result.entries[{2}].key)\n'
                         .format(bucket_name, vtype, part_number))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))

    def modify_multi_part_object_size(self, bucket_name, file_name):
        """
        Using keyrouter API, modify the size of multi part object
        :param bucket_name: bucket name
        :param file_name: uploaded file name
        """
        python_script = ('\n'
                         'import keyrouter_api.ttypes as kt\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Object\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'from scaler_api import scalerdb as utils\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'obj_prefix = sdb_bucket_id.id\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, obj_prefix, obj_prefix, False, None, 1000)\n'
                         'prefix = list_result.entries[0].key\n'
                         'p_key=prefix.split("{1}")\n'
                         'prefix=p_key[0]+"{1}"\n'
                         'entries = cli.clients.keyrouter.listEntries2a("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, "", "", False, prefix, 10, None, False)\n'
                         'okey = entries.entries[0].key\n'
                         'oval = entries.entries[0].value\n'
                         'obj = utils.deserialize_blob_of_sdb_value(oval)\n'
                         'initial_size_of_obj = obj.multipartMetaData.size\n'
                         'obj.multipartMetaData.size = initial_size_of_obj+1\n'
                         'mobj_blob = utils.serialize(obj)\n'
                         'modified_obj_sdb_val = oval\n'
                         'modified_obj_sdb_val.blob = mobj_blob\n'
                         'cli.clients.keyrouter.put("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, okey, modified_obj_sdb_val)\n'
                         .format(bucket_name, file_name))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))

    def modify_multi_part_size_of_part_key(self, bucket_name, part_number):
        """
        Using keyrouter API, modify the size of part key
        :param bucket_name: bucket name
        :param part_number: part number
        """
        python_script = ('\n'
                         'import keyrouter_api.ttypes as kt\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Object\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'from scaler_api import scalerdb as utils\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'obj_prefix = sdb_bucket_id.id\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, obj_prefix, obj_prefix, False, None, 1000)\n'
                         'prefix = list_result.entries[{1}].key\n'
                         'entries = cli.clients.keyrouter.listEntries2a("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, "", "", False, prefix, 10, None, False)\n'
                         'okey = entries.entries[0].key\n'
                         'oval = entries.entries[0].value\n'
                         'obj = utils.deserialize_blob_of_sdb_value(oval)\n'
                         'initial_size_of_obj = obj.singlePart.size\n'
                         'obj.singlePart.size = initial_size_of_obj+1\n'
                         'mobj_blob = utils.serialize(obj)\n'
                         'modified_obj_sdb_val = oval\n'
                         'modified_obj_sdb_val.blob = mobj_blob\n'
                         'cli.clients.keyrouter.put("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, okey, modified_obj_sdb_val)\n'
                         .format(bucket_name, part_number))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))


    def modify_multi_part_etag_of_part_key(self, bucket_name, part_number=0):
        """
        Using keyrouter API, modify etag of the part key of multi part object
        :param bucket_name: bucket name
        :param part_number: object part index number
        """
        python_script = ('\n'
                         'import keyrouter_api.ttypes as kt\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Object\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'from scaler_api import scalerdb as utils\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'obj_prefix = sdb_bucket_id.id\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, obj_prefix, obj_prefix, False, None, 1000)\n'
                         'pkey = list_result.entries[{1}].key\n'
                         'value = cli.clients.keyrouter.get("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, pkey)\n'
                         'pobj = utils.deserialize_blob_of_sdb_value(value.value)\n'
                         'checksum = list(pobj.singlePart.checksum)\n'
                         'checksum[-2] = 1\n'
                         'checksum=bytearray(checksum)\n'
                         'pobj.singlePart.checksum=checksum\n'
                         'mval = value.value\n'
                         'modified_pblob = utils.serialize(pobj)\n'
                         'mval.blob = modified_pblob\n'
                         'cli.clients.keyrouter.put("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, pkey, mval)\n'
                         .format(bucket_name, part_number))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))

    def modify_multi_part_filp_the_last_byte_offset(self, bucket_name, part_number=0):
        """
        Using keyrouter API, modify dkey of one part key of multi part object
        :param bucket_name: bucket name
        :param part_number: object part index number
        """
        python_script = ('\n'
                         'import keyrouter_api.ttypes as kt\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Object\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'from scaler_api import scalerdb as utils\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'obj_prefix = sdb_bucket_id.id\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, obj_prefix, obj_prefix, False, None, 1000)\n'
                         'pkey = list_result.entries[{1}].key\n'
                         'pvalue = list_result.entries[{1}].value\n'
                         'temp=list(pkey)\n'
                         'temp[-4]=1\n'
                         'mkey = bytearray(temp)\n'
                         'cli.clients.keyrouter.put("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, mkey, pvalue)\n'
                         'cli.clients.keyrouter.remove("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, pkey)\n'
                         .format(bucket_name, part_number))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))


    def modify_multi_part_dbkey_type_of_part_key(self, bucket_name, part_number=0):
        """
        Using keyrouter API, perform bit filp in one part key of multi part object
        :param bucket_name: bucket name
        :param part_number: objectpart index number
        """
        python_script = ('\n'
                         'import keyrouter_api.ttypes as kt\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Object\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'from scaler_api import scalerdb as utils\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'obj_prefix = sdb_bucket_id.id\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, obj_prefix, obj_prefix, False, None, 1000)\n'
                         'pkey = list_result.entries[{1}].key\n'
                         'pvalue = list_result.entries[{1}].value\n'
                         'temp=list(pkey)\n'
                         'temp[-28]="v"\n'
                         'mkey = bytearray(temp)\n'
                         'cli.clients.keyrouter.put("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, mkey, pvalue)\n'
                         'cli.clients.keyrouter.remove("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, pkey)\n'
                         .format(bucket_name, part_number))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))

    def modify_multi_part_upload_id_of_part_key(self, bucket_name, part_number=0):
        """
        Using keyrouter API, perform bit filp in one part key of multi part object
        :param bucket_name: bucket name
        :param part_number: objectpart index number
        """
        python_script = ('\n'
                         'import keyrouter_api.ttypes as kt\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Object\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'from scaler_api import scalerdb as utils\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'obj_prefix = sdb_bucket_id.id\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, obj_prefix, obj_prefix, False, None, 1000)\n'
                         'pkey = list_result.entries[{1}].key\n'
                         'pvalue = list_result.entries[{1}].value\n'
                         'temp=list(pkey)\n'
                         'temp[-30]=1\n'
                         'mkey = bytearray(temp)\n'
                         'cli.clients.keyrouter.put("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, mkey, pvalue)\n'
                         'cli.clients.keyrouter.remove("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, pkey)\n'
                         .format(bucket_name, part_number))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))

    def modify_one_object_size_in_multi_version(self, bucket_name, part_number):
        """
        Using keyrouter API, modify the size of oop key for multi version
        :param bucket_name: bucket name
        :param part_number: part number
        """
        python_script = ('\n'
                         'import keyrouter_api.ttypes as kt\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Object\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'from scaler_api import scalerdb as utils\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'obj_prefix = sdb_bucket_id.id\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, obj_prefix, obj_prefix, False, None, 1000)\n'
                         'prefix = list_result.entries[0].key\n'
                         'entries = cli.clients.keyrouter.listEntries2a("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, "", "", False, prefix, 10, None, False)\n'
                         'okey = entries.entries[0].key\n'
                         'oval = entries.entries[0].value\n'
                         'obj = utils.deserialize_blob_of_sdb_value(oval)\n'
                         'initial_size_of_obj = obj.singlePart.size\n'
                         'obj.singlePart.size = initial_size_of_obj+1\n'
                         'mobj_blob = utils.serialize(obj)\n'
                         'modified_obj_sdb_val = oval\n'
                         'modified_obj_sdb_val.blob = mobj_blob\n'
                         'cli.clients.keyrouter.put("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, okey, modified_obj_sdb_val)\n'
                         'print prefix.encode("base64", "strict")\n'
                         .format(bucket_name, part_number))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
        entries_dict = fab_run.stdout.splitlines()[-1]
        return entries_dict


    def iterate_versioning_backend_bucket_objects_etag(self, bucket_name, vtype, during, object_index=0):
        python_script = ('\n'
                         'from sherpa import cli_wrapper as cli\n'
                         'from keyrouter_api.ttypes import SDB_SpaceEnum_t\n'
                         'from thrift.transport import TTransport\n'
                         'from scalerdb_api.common.ttypes import SDB_KeyOption\n'
                         'from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Object\n'
                         'from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol\n'
                         'list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("N{0}"), SDB_KeyOption("N{0}"),1)\n'
                         't = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_bucket_id = SDB_BucketId()\n'
                         'sdb_bucket_id.read(p)\n'
                         'prefix = sdb_bucket_id.id\n'
                         'list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, prefix, prefix, False, None, 1000)\n'
                         't = TTransport.TMemoryBuffer(list_result.entries[{2}].value.blob)\n'
                         'p = TCompatibleCompactProtocol(t)\n'
                         'sdb_object = SDB_Object()\n'
                         'sdb_object.read(p)\n'
                         'print sdb_object.singlePart.columnDataHandle'.format(bucket_name, vtype, object_index))

        with hide('running'):
            fab_run = self.scalers[0].run_cmd(
                "/opt/ampli/apps/sherpa/venv/bin/python -W ignore -c '{}'".format(python_script))
        entries_dict = fab_run.stdout.splitlines()[-1]
        return entries_dict



    @staticmethod
    def display_key_spaces(entries_dict, vtype, during):
        print(entries_dict)
        print('KEY SPACES - %s' % during)
        if vtype == 'O':
            for key in entries_dict:
                if key.endswith('M'):
                    print('O - O - M')
                elif key.endswith('K'):
                    print('O - O - K')
                elif key.endswith('W'):
                    print('O - O - W')
                elif key.endswith('v'):
                    print('O - O - v')
                elif key.endswith('d'):
                    print('O - O - d')
                elif key.endswith('b'):
                    print('O - O - b')
                elif key.endswith('t'):
                    print('O - O - t')
                elif key.endswith('Z'):
                    print('O - O - Z')
                elif key.endswith('p'):
                    print('O - O - p')
                elif key.endswith('n'):
                    print('O - O - n')
        elif vtype == 'P':
            for key in entries_dict:
                if 'W' in key:
                    print('O - P - W')
        elif vtype == 'T':
            for key in entries_dict:
                if key.endswith('M'):
                    print('O - T - M')
                elif key.endswith('K'):
                    print('O - T - K')
                elif key.endswith('W'):
                    print('O - T - W')


class ScalerIM:

    def __init__(self, scalers, hw):
        self.scalers = scalers
        self.hw = hw
        if hw:
            exposed_ssh_ip = scalers[0].interfaces['eth4'].address
            self.ssh_connection_string = '%s:22' % exposed_ssh_ip
        else:
            exposed_ports_ssh = scalers[0].exposed_ports['ssh']
            self.ssh_connection_string = '%s:%s' % (exposed_ports_ssh.public_ip, exposed_ports_ssh.public_port)

    def create_s3_account(self, account_name, email_id):
        with us.SSHTunnel(auth, self.ssh_connection_string, SIM_URL_ON_SCALER) as client_tunnel:
            forward_server = client_tunnel[1]
            scalerim = ScalerThriftHttpConnection('marvin_scaler_libs', IdentityManager.Client, 'localhost',
                                                  forward_server.server_address[1], service=SCALERIM_SERVICE_URL)
            account_id_opt = scalerim.client.identitiesGetByEmail('marvin_scaler_libs', [email_id])[0]
            if not account_id_opt.identity:
                account_id = scalerim.client.accountCreate('marvin_scaler_libs', displayName=account_name,
                                                           email=email_id)
            else:
                account_id = account_id_opt.identity
            if not account_id.apiKeys:
                scalerim.client.apiKeyGenerate('marvin_scaler_libs', account_id.canonicalId)
            account_id_opt = scalerim.client.identitiesGetByEmail('marvin_scaler_libs', [email_id])[0]
            account_apikey = scalerim.client.apiKeyGet("", account_id_opt.identity.apiKeys[0].accessKey)
            account_dict = {'canonical_id': account_id.canonicalId, 'accessKey': account_apikey.accessKey,
                            'secretKey': account_apikey.secretKey}
            scalerim.close()
        return account_dict

    def create_s3_user(self, user_name, email_id, canonical_id):
        with us.SSHTunnel(auth, self.ssh_connection_string, SIM_URL_ON_SCALER) as client_tunnel:
            forward_server = client_tunnel[1]
            scalerim = ScalerThriftHttpConnection('marvin_scaler_libs', IdentityManager.Client, 'localhost',
                                                  forward_server.server_address[1], service=SCALERIM_SERVICE_URL)
            identity = scalerim.client.userCreate('marvin_scaler_libs', displayName=user_name, email=email_id,
                                                  parentAccountCanonicalId=canonical_id)
            apiKeys = scalerim.client.apiKeyGenerate('marvin_scaler_libs', identity.canonicalId)
            user_dict = {'canonical_id': identity.canonicalId, 'accessKey': apiKeys.accessKey,
                         'secretKey': apiKeys.secretKey}
            scalerim.close()
        return user_dict

    def configure_quota_sim(self, canonical_id, hardlimit, lp, hp, quota_type):
        with us.SSHTunnel(auth, self.ssh_connection_string, SIM_URL_ON_SCALER) as client_tunnel:
            forward_server = client_tunnel[1]
            scalerim = ScalerThriftHttpConnection('marvin_scaler_libs', IdentityManager.Client, 'localhost',
                                                  forward_server.server_address[1], service=SCALERIM_SERVICE_URL)

            args = list()
            # quota = SIM_QuotaLimits(100, 85, 95, SIM_QuotaEnforcementType_t.HARD)
            quota = SIM_QuotaLimits(hardlimit, lp, hp, quota_type)
            arg = SIM_IdentitiesUpdateArgs(canonicalId=canonical_id, capacityQuotaLimits=quota)
            args.append(arg)
            identity = scalerim.client.identitiesUpdate("", args)
            scalerim.close()
        return identity

    def validate_quota_sim(self, canonical_id, hardlimit, lp, hp, quota_type):
        with us.SSHTunnel(auth, self.ssh_connection_string, SIM_URL_ON_SCALER) as client_tunnel:
            forward_server = client_tunnel[1]
            scalerim = ScalerThriftHttpConnection('marvin_scaler_libs', IdentityManager.Client, 'localhost',
                                                  forward_server.server_address[1], service=SCALERIM_SERVICE_URL)

            quota_list = list()
            id = canonical_id
            quota_list.append(id)
            GetBycanonicalID = scalerim.client.identitiesGetByCanonicalId("", quota_list)
            scalerim.close()
            assert GetBycanonicalID[
                       0].identity.capacityQuotaLimits.hardLimitBytes == hardlimit, 'Quota limit did not match: %s and %s' % (
            GetBycanonicalID[0].identity.capacityQuotaLimits.hardLimitBytes, hardlimit)
            assert GetBycanonicalID[
                       0].identity.capacityQuotaLimits.softLimitLowPercentage == lp, 'Quota low percentage limit did not match: %s and %s' % (
            GetBycanonicalID[0].identity.capacityQuotaLimits.softLimitLowPercentage, lp)

            assert GetBycanonicalID[
                       0].identity.capacityQuotaLimits.softLimitHighPercentage == hp, 'Quota high percentage limit did not match: %s and %s' % (
            GetBycanonicalID[0].identity.capacityQuotaLimits.softLimitHighPercentage, hp)


class ScalerPowerOps:

    def __init__(self, m, env):
        self.marvin_cli = m
        self.env = env

    def wait_for_machine_status(self, node, exp_status, timeout=300):
        status_done = False
        elapsed_time = 0
        time.sleep(60)
        while not status_done and elapsed_time < timeout:
            status = self.marvin_cli.machine.status(node)
            if exp_status in status:
                status_done = True
                break
            else:
                time.sleep(10)
                elapsed_time += 10
        return status_done

    def soft_shutdown_scaler(self, node):
        print 'Bring down node %s' % node
        machine = self.env.get_machine(node)

        if 'running' in machine.status:
            machine.run_cmd('service mona stop', use_sudo=True)
            machine.run_cmd('/etc/init.d/marvinservices stop', use_sudo=True)

            self.env.close_connections()
            self.env.run_actions('stop_machine', select_machines=[node])

            if 'poweroff' not in machine.status:
                return False
            else:
                return True

        elif 'poweroff' in machine.status:
            return True

    def soft_poweron_scaler(self, node):
        print 'Bring up node %s' % node
        machine = self.env.get_machine(node)

        self.env.close_connections()
        self.env.run_actions('start_machine', select_machines=[node],
                             start_machine_check=True)

        if 'running' not in machine.status:
            return False
        else:
            return True

    def soft_reboot_scaler(self, node):
        print 'Rebooting node %s' % node
        machine = self.env.get_machine(node)

        if 'running' in machine.status:
            machine.run_cmd('service mona stop', use_sudo=True)
            machine.run_cmd('/etc/init.d/marvinservices stop', use_sudo=True)

            self.env.close_connections()
            self.env.run_actions('stop_machine', 'start_machine', select_machines=[node],
                                 start_machine_check=True)

        if 'running' not in machine.status:
            return False
        else:
            return True

    def check_ssh_status_node(self, nodes):
        for node in nodes:
            print 'Checking SSH status in %s' % node
            try:
                machine = self.env.get_machine(node)
                machine.run_cmd('true')
            except Exception as e:
                assert 'Unable to communicate to VM %s. Reason : %s' % (node, e.message)


class ScalerConfigParser(object):

    def __init__(self, scaler, component):
        self.scaler = scaler
        self.component = component
        self.config_file = scaler.run_cmd('ls /opt/ampli/cfg/%s/*.cfg' % self.component)
        self.cfg_content = BytesIO(self.scaler.get_file_contents(self.config_file))
        self.ini = Inifile(self.cfg_content)

    def update_config(self, section, option, value, add=False):
        if add:
            self.ini.addparam(section, option, value)
            print 'Adding %s=%s under %s in %s' % (option, value, section, self.scaler.name)
        else:
            self.ini.setparam(section, option, value)
            print 'Updating %s=%s under %s in %s' % (option, value, section, self.scaler.name)
        self.ini.write()
        self.scaler.put_file(self.cfg_content, self.config_file, use_sudo=True)

    def remove_config(self, section, option):
        self.ini.removeparam(section, option)
        self.ini.write()
        print 'Removing %s under %s in %s' % (option, section, self.scaler.name)
        self.scaler.put_file(self.cfg_content, self.config_file, use_sudo=True)

    def get_config_option(self, section, option):
        print 'Getting %s under %s in %s' % (option, section, self.scaler.name)
        return self.ini.getvalue(section, option)

    def restart_component(self):
        print 'Restarting %s in %s' % (self.component, self.scaler.name)
        self.scaler.run_cmd('/etc/init.d/marvinservices restart %s' % self.component,
                            use_sudo=True)
        time.sleep(10)

    def start_application(self):
        self.scaler.run_cmd('/etc/init.d/marvinservices start %s' % self.component,
                            use_sudo=True)

    def stop_application(self, groupstop=False):
        action = 'stop'
        if groupstop:
            action = 'groupstop'
        self.scaler.run_cmd('/etc/init.d/marvinservices %s %s' % (action, self.component),
                            use_sudo=True)


class ObjectLifeCycle:

    def __init__(self):
        self.lifecycle = Lifecycle()
        self.prefixes = ['obj', 'file', '*', 'logs/']
        self.status = ['Enabled', 'Enabled', 'Enabled', 'Disabled']

    def set_lifecycle_with_days(self, bucket):
        for i in xrange(4):
            expiration = Expiration(days=i+1)
            rule = Rule(id=i, prefix=self.prefixes[i], status=self.status[i], expiration=expiration)
            self.lifecycle.append(rule)
        return bucket.configure_lifecycle(self.lifecycle)

    def set_lifecycle_with_date(self, policy_days, bucket, append_rule=False):
        now = datetime.datetime.now()
        prev_days = datetime.timedelta(days=policy_days)
        past_date = now - prev_days
        past_date = past_date.replace(hour=0, minute=0, second=0, microsecond=0)
        iso_format = past_date.isoformat()
        self.exp_date = past_date.strftime('%Y-%m-%d %H:%M:%S')
        expiration = Expiration(date=iso_format)
        for i in xrange(4):
            if append_rule:
                date_rule = Rule(id=i+4, prefix=self.prefixes[i], status=self.status[i], expiration=expiration)
            else:
                date_rule = Rule(id=i, prefix=self.prefixes[i], status=self.status[i], expiration=expiration)
            self.lifecycle.append(date_rule)
        return bucket.configure_lifecycle(self.lifecycle)

    @staticmethod
    def delete_lifecycle_rule(boto_connection, bucket_name):
        response = boto_connection.make_request('DELETE', bucket=bucket_name,
                                                query_args='lifecycle', headers=None)
        return response.status

    def validate_lifecycle_config(self, rule_length, bucket):
        get_lifecycle = bucket.get_lifecycle_config()
        assert len(get_lifecycle) == rule_length, "Get lifecycle config Failed"

        for i in xrange(rule_length):
            actual_lifecycle = get_lifecycle[i]
            assert int(actual_lifecycle.id) == i, 'ID %s mismatch' % i
            assert actual_lifecycle.prefix == self.prefixes[i], 'Prefix %s mismatch' % self.prefixes[i]
            assert actual_lifecycle.status == self.status[i], 'Status %s mismatch' % self.status[i]

    def validate_lifecycle_bl_keys(self, life_cycle, prefix, status):
        assert life_cycle["status"] == 1, 'Lifecycle Status  = %s' % life_cycle["status"]
        assert len(life_cycle["lifecycleRules"]) == len(prefix), \
            'Number of rules   = %s' % len(life_cycle["lifecycleRules"])
        for rule in life_cycle["lifecycleRules"]:
            assert rule["prefix"] == prefix[int(rule["id"])], 'Rule prefixes are not same'
            rule_status = 1 if status[int(rule["id"])] == 'Enabled' else 2
            assert rule["status"] == rule_status, 'Rule Status are not same'
            for action in rule["lifecycleActions"]:
                if action["lifecycleExpiration"]:
                    if action["lifecycleExpiration"]["date"]:
                        assert self.exp_date == self.process_timestamp(action["lifecycleExpiration"]["date"] * 1000), \
                            'Expiry date not for lifecycle do not match'
                    elif action["lifecycleExpiration"]["milliSeconds"]:
                        days = int(action["lifecycleExpiration"]["milliSeconds"] / (24 * 60 * 60 * 1000))
                        days_set = int(rule["id"]) + 1
                        assert days_set == days, 'Expiration days are not same'
        return True

    def process_timestamp(self, timestamp_micros):
        time_str = time.asctime(time.gmtime(timestamp_micros / 1000000.0))
        date_object = datetime.datetime.strptime(time_str, '%a %b %d %H:%M:%S %Y')
        return date_object.strftime('%Y-%m-%d %H:%M:%S')


class ScalerLogParser:

    def __init__(self, scaler, component):
        self.scaler = scaler
        self.component = component
        log_files = scaler.run_cmd('ls /opt/ampli/var/log/%s/*.log' % self.component)
        self.log_file = log_files.split('\n')[0]
        self.log_file = self.log_file.replace('\r', '')

    def read_scaler_log_file(self):
        local_log = '%s_scalerd.log' % self.scaler.name
        self.scaler.get_file(self.log_file, local_log)
        return local_log


class Metering:

    def __init__(self, env, marvin_cli, env_info, scalers, hw):
        self.marvin = marvin_cli
        self.user_count = 0
        self.local_meter_file = 'scalerd.meter'
        self.env = env
        self.hw = hw
        self.scalers = scalers
        self.env_info = env_info
        self.nodes = []
        self.header_fields = ['type', 'timestamp', 'bucketid', 'resourcetype', 'httpmethod', 'userid', 'result',
                              'bytes', 'sourceip', 'forwardedfor', 'accountid', 'apikey', 'forwardedproto', 'bucket',
                              'key', 'totaltime', 'requestid', 'operation', 'useragent', 'inputversionid',
                              'outputversionid']
        for node_id in range(len(self.scalers)):
            node_info = {}
            application_list = self.marvin.machine.list()[node_id]['application']
            for app_guid in application_list:
                if app_guid['applicationtype'] == 'scalerd':
                    scalerd_guid = app_guid['guid']
                    node_info['node_scalerd_guid'] = '%s%s/' % (METERING_LOG, scalerd_guid)
            node_info['node_guid'] = marvin_cli.machine.list()[node_id]['guid']
            node_id += 1
            node_info['name'] = 'scaler-%s' % node_id
            self.nodes.append(node_info)

    def clean_metering_reports(self):
        for scaler in self.nodes:
            print 'Cleaning metering files in %s under %s' % (scaler['name'], scaler['node_scalerd_guid'])
            cmd = 'ls %s | tail -n 1 | xargs find %s ! -name $1 | xargs rm' % (scaler['node_scalerd_guid'],
                                                                               scaler['node_scalerd_guid'])
            self.env.get_machine(scaler['name']).run_cmd(cmd, use_sudo=True, warn_only=True)

    def get_metering_files(self):
        local_dir = 'metering_files'
        if not os.path.isdir(local_dir):
            os.mkdir(local_dir)
        for scaler in self.nodes:
            print 'checking metering file in %s' % scaler['name']
            output = self.env.get_machine(scaler['name']).run_cmd('ls -t1 %s*.meter'
                                                                  % scaler['node_scalerd_guid'],
                                                                  use_sudo=True)
            list_files = output.split('\n')
            for meter_files in list_files:
                meter_files = meter_files.replace('\r','')
                dest_file = local_dir + '/' + meter_files.split('/')[-1]
                self.env.get_machine(scaler['name']).get_file(meter_files, dest_file)

    def read_metering_file_content(self):
        for meter_file in os.listdir('metering_files'):
            file_path = 'metering_files' + '/' + meter_file
            with open(file_path) as f:
                data = f.read()
            with open(self.local_meter_file, 'a') as lf:
                lf.write(data)

    def get_meter_file_content(self):
        self.get_metering_files()
        # Safe sleep time so that all operations are updated in the meter file
        time.sleep(20)
        self.read_metering_file_content()

    def validate_metering_file_headers(self):
        self.get_meter_file_content()
        # safe time for local file getting updated.
        time.sleep(10)
        with open(self.local_meter_file, 'r') as fd:
            for lines in fd:
                if 's3_request_layout' in lines:
                    lines = lines.strip()
                    fields = lines.split(':')
                    metering_fields = fields[1].split('|')
                    diff_list = list(set(self.header_fields) - set(metering_fields))
                    return cmp(self.header_fields, metering_fields), diff_list

    def refactor_metering_results(self, bucket_name):
        refactored_fields = []
        print 'Reading local meter file %s' % self.local_meter_file
        # Safe sleep time before we read the meter file copied locally.
        time.sleep(20)
        with open(self.local_meter_file, 'r') as fd:
            for lines in fd:
                if bucket_name in lines:
                    metering_fields = lines.split(';')
                    meter_dict = dict(zip(self.header_fields, metering_fields))
                    refactored_fields.append(meter_dict)
        return refactored_fields

    def get_gunzip_meter_files(self, node_name):
        time.sleep(20)
        for scaler in self.nodes:
            if scaler['name'] == node_name:
                print 'checking for metering gunzip file in %s' % scaler['name']
                output = self.env.get_machine(scaler['name']).run_cmd('ls -t1 %s' % scaler['node_scalerd_guid'],
                                                                      use_sudo=True)
                file_list = output.split('\n')
                gunzip_files = [file_name.replace('\r', '') for file_name in file_list if '.meter.gz' in file_name]
                return gunzip_files

    def do_create_users_bucket_s3ops(self, sim, no_of_users, no_of_buckets, metering='capacity'):
        account_conn = S3_Ops(self.env_info, self.scalers, self.hw)
        bucket_list = []
        multi_buckets_to_clean = []
        metering_stats = []

        accounts_created = {}
        for user in range(no_of_users):
            self.user_count += 1
            account_name = "MtUser_%s" % uuid4()
            account_mail_id = "%s@hgst.com" % account_name
            accounts = sim.create_s3_account(account_name, account_mail_id)
            accounts_created[account_name] = accounts

        for account in accounts_created.values():
            for bucket in range(no_of_buckets):
                bucket_dict = {}
                clean_bucket_dict = {}
                bucket_keys = []
                object_byte_count = 0
                add_keys = random.randint(1, 20)
                del_keys = random.randint(0, add_keys-1)

                user_name = "flmuser_%s" % uuid4()
                email_id = "%s@hgst.com" % user_name
                user1 = sim.create_s3_user(user_name, email_id, account['canonical_id'])
                user1_conn = S3_Ops(self.env_info, self.scalers, self.hw)

                user1_boto_conn = user1_conn.get_s3_connection(access_key=user1['accessKey'],
                                                               secret_key=user1['secretKey'])

                account_boto_connection = account_conn.get_s3_connection(access_key=account['accessKey'],
                                                                         secret_key=account['secretKey'])
                bucket_name = 'bucket-%s' % uuid4()
                response = account_conn.put_bucket(account_boto_connection, bucket_name)
                user1_conn.add_user_grant_acl(account_boto_connection, bucket_name, user1['canonical_id'],
                                              'FULL_CONTROL')
                bucket_ops = {'resourcetype': 'bucket', 'bucket': bucket_name, 'operation': 'REST.PUT.BUCKET',
                              'httpmethod': 'PUT', 'result': 'SUCCESS', 'type': 's3_request', 'bytes': '0',
                              'key': '', 'requestid': response[0]}
                metering_stats.append(bucket_ops)

                for i in range(add_keys):
                    response = user1_conn.upload_single_object(user1_boto_conn, bucket_name,
                                                               key='obj-%s' % i, data='x' * i)
                    object_byte_count += i
                    bucket_keys.append('obj-%s' % i)
                    object_ops = {'resourcetype': 'object', 'bucket': bucket_name, 'operation': 'REST.PUT.OBJECT',
                                  'httpmethod': 'PUT', 'result': 'SUCCESS', 'type': 's3_request', 'bytes': str(i),
                                  'key': 'obj-%s' % i, 'requestid': response[0]}
                    metering_stats.append(object_ops)

                for i in range(del_keys):
                    response = user1_conn.delete_object(user1_boto_conn, bucket_name, key='obj-%s' % i)
                    object_byte_count -= i
                    bucket_keys.remove('obj-%s' % i)
                    object_ops = {'resourcetype': 'object', 'bucket': bucket_name, 'operation': 'REST.DELETE.OBJECT',
                                  'httpmethod': 'DELETE', 'result': 'SUCCESS', 'type': 's3_request', 'bytes': '0',
                                  'key': 'obj-%s' % i, 'requestid': response[0]}
                    metering_stats.append(object_ops)

                object_count = add_keys - del_keys

                clean_bucket_dict['Bucket Name'] = bucket_name
                clean_bucket_dict['Bucket Keys'] = bucket_keys
                clean_bucket_dict['User Conn'] = user1_boto_conn
                clean_bucket_dict['Account Conn'] = account_boto_connection
                multi_buckets_to_clean.append(clean_bucket_dict)

                bucket_dict['Bucket Name'] = bucket_name
                bucket_dict['Object Count'] = str(object_count)
                bucket_dict['Object Byte Count'] = str(object_byte_count)
                bucket_dict['Bucket Owner'] = str(account['canonical_id'])
                bucket_dict['Bucket Keys'] = bucket_keys
                bucket_list.append(bucket_dict)

        if metering == 'capacity':
            return user1_conn, account_conn, bucket_list, multi_buckets_to_clean
        elif metering == 'call':
            return user1_conn, account_conn, bucket_list, metering_stats, multi_buckets_to_clean

    def compare_metering_stats(self, expected_stats, metering_stats):
        match = 0
        validated = True
        for stats in expected_stats:
            for fields in metering_stats:
                if fields['requestid'] == stats['requestid']:
                    if fields['resourcetype'] != stats['resourcetype']:
                        print 'Resource type did not match for %s. It should be %s while it is %s for %s'\
                              % (stats['resourcetype'], stats['resourcetype'], fields['resourcetype'],
                                 stats['requestid'])
                        validated = False
                    if fields['httpmethod'] != stats['httpmethod']:
                        print 'Httpmethod did not match for %s. It should be %s while it is %s for %s' \
                              % (stats['httpmethod'], stats['httpmethod'], fields['httpmethod'],
                                 stats['requestid'])
                        validated = False
                    if fields['key'] != stats['key']:
                        print 'key did not match for %s. It should be %s while it is %s for %s'\
                              % (stats['key'], stats['key'], fields['key'], stats['requestid'])
                        validated = False
                    if fields['operation'] != stats['operation']:
                        print 'Operation did not match for %s. It should be %s while it is %s for %s'\
                              % (stats['operation'], stats['operation'], fields['operation'],
                                 stats['requestid'])
                        validated = False
                    if fields['bucket'] != stats['bucket']:
                        print 'Bucket name did not match for %s. It should be %s while it is %s for %s'\
                              % (stats['bucket'], stats['bucket'], fields['bucket'], stats['requestid'])
                        validated = False
                    if fields['result'] != stats['result']:
                        print 'Result did not match for %s. It should be %s while it is %s for %s'\
                              % (stats['result'], stats['result'], fields['result'], stats['requestid'])
                        validated = False
                    if fields['type'] != stats['type']:
                        print 'Type did not match for %s. It should be %s while it is %s for %s'\
                              % (stats['type'], stats['type'], fields['type'], stats['requestid'])
                        validated = False
                    if fields['bytes'] != stats['bytes']:
                        print 'Bytes did not match for %s. It should be %s while it is %s for %s'\
                              % (stats['bytes'], stats['bytes'], fields['bytes'], stats['requestid'])
                        validated = False
                    match += 1
        return validated, match


class AsCli:

    def __init__(self, hostname, https_port):
        self.url = 'https://' + hostname + ':' + str(https_port)

    def call_api(self, http_method, url, data=None, headers=None, stream=None):
        try:
            http_method = http_method.lower()
            if http_method == 'post':
                response = requests.post(url, json=data, headers=headers, verify=False)
            elif http_method == 'put':
                response = requests.put(url, json=data, headers=headers, verify=False)
            elif http_method == 'get':
                if stream is True:
                    response = requests.get(url, params=data, headers=headers, verify=False, stream=True)
                else:
                    response = requests.get(url, params=data, headers=headers, verify=False)
            elif http_method == 'delete':
                response = requests.delete(url, json=data, headers=headers, verify=False)
            else:
                return 1
        except requests.exceptions.HTTPError as e:
            print "Failed to call %s", url
            raise
        except requests.exceptions.ConnectionError as e:
            print "Connection Error. Failed to call %s", url
            raise
        except:
            print "Unexpected Error"
            raise
        else:
            return response

    def call_rest_api(self, http_verb, resource, data=None, headers=None, expected_status=200):
        response = self.call_api(http_verb, self.url + resource, data=data, headers=headers)
        try:
            assert response.status_code == expected_status
        except AssertionError:
            print "Status is not as expected. Expected: " + str(expected_status) + " Actual: " + \
                  str(response.status_code)
            raise
        else:
            return response

    def login(self):
        response = self.call_rest_api('POST', '/login', data=dict(username='admin', password='Administrat0r$'))
        auth_token = response.json()['payload']['token']
        return auth_token

    def get_device_id(self, headers):
        try:
            sysinfo_resp = self.call_rest_api('GET', '/api/replication/systeminfo', headers=headers, expected_status=200)
            return sysinfo_resp.json()["payload"]["deviceId"]
        except Exception as e:
            print "Failed to find device id with error %s" % e
        return None


class Replication:

    def __init__(self, logger, keyrouter=None):
        self.lg = logger
        self.keyrouter = keyrouter

    def convert_from_raw_bucket_id(self, bucket_id):
        """Convert a raw bucket id to a bucket id number

        :param bucket_id: raw bucket id
        :type bucket_id: string
        :returns: the bucket id number
        :rtype: int
        """
        (a, b, c) = struct.unpack('<LQL', bucket_id)
        assert b == 0x8000400000
        return c << 32 | a

    def validate_object_metadata(self, boto3_site1, boto3_site2, src_bucket, dst_bucket, src_bucket1=None,
                                 src_bucket2=None, minimal=False):
        """
        Validate whether the size, etag, and versions of the replicated objects match as that of the
        objects in source bucket
        """
        self.src_bucket = src_bucket
        self.dst_bucket = dst_bucket
        self.src_bucket1 = src_bucket1
        self.src_bucket2 = src_bucket2
        self.src_bucket_key_version = self.src_bucket.get_all_versions()
        self.dst_bucket_key_version = self.dst_bucket.get_all_versions()
        self.src_bucket_key1 = []
        self.src_bucket_key2 = []
        self.src_bucket1_key_versions = []
        self.src_bucket2_key_versions = []
        src_obj_list = list()
        dst_obj_list = list()
        match = 0
        for key in self.src_bucket_key_version:
            my_key = boto3_site1.head_object(Bucket=self.src_bucket.name, Key=key.name, VersionId=key.version_id)
            src_obj = {'name': key.name, 's3versionId': key.version_id,
                       'etag': self.src_bucket.get_key(key.name, version_id=key.version_id).etag,
                       'size': self.src_bucket.get_key(key.name, version_id=key.version_id).size,
                       'date': self.src_bucket.get_key(key.name, version_id=key.version_id).date}
            src_obj_list.append(src_obj)

        if self.src_bucket1 is not None:
            self.src_bucket1_key_versions = self.src_bucket1.get_all_versions()
            for key in self.src_bucket1_key_versions:
                my_key = boto3_site1.head_object(Bucket=self.src_bucket1.name, Key=key.name, VersionId=key.version_id)
                src_obj = {'name': key.name, 's3versionId': key.version_id,
                           'etag': self.src_bucket1.get_key(key.name, version_id=key.version_id).etag,
                           'size': self.src_bucket1.get_key(key.name, version_id=key.version_id).size,
                           'date': self.src_bucket1.get_key(key.name, version_id=key.version_id).date}
                src_obj_list.append(src_obj)

        if self.src_bucket2 is not None:
            self.src_bucket2_key_versions = self.src_bucket2.get_all_versions()
            for key in self.src_bucket2_key_versions:
                my_key = boto3_site1.head_object(Bucket=self.src_bucket2.name, Key=key.name, VersionId=key.version_id)
                src_obj = {'name': key.name, 's3versionId': key.version_id,
                           'etag': self.src_bucket2.get_key(key.name, version_id=key.version_id).etag,
                           'size': self.src_bucket2.get_key(key.name, version_id=key.version_id).size,
                           'date': self.src_bucket2.get_key(key.name, version_id=key.version_id).date}
                src_obj_list.append(src_obj)

        for key in self.dst_bucket_key_version:
            my_key = boto3_site2.head_object(Bucket=self.dst_bucket.name, Key=key.name, VersionId=key.version_id)
            dst_obj = {'name': key.name, 's3versionId': key.version_id,
                       'etag': self.dst_bucket.get_key(key.name, version_id=key.version_id).etag,
                       'size': self.dst_bucket.get_key(key.name, version_id=key.version_id).size,
                       'date': self.dst_bucket.get_key(key.name, version_id=key.version_id).date}
            dst_obj_list.append(dst_obj)

        self.lg('\n')
        self.lg(src_obj_list)
        self.lg(dst_obj_list)
        for dst_obj in dst_obj_list:
            for src_obj in src_obj_list:
                if dst_obj['s3versionId'] == src_obj['s3versionId']:
                    assert dst_obj['name'] == src_obj['name'], \
                        'Objects key did not match: %s and %s' % (src_obj['name'], dst_obj['name'])
                    assert dst_obj['size'] == src_obj['size'],\
                        'Objects size did not match: %s and %s' % (src_obj['size'], dst_obj['size'])
                    assert dst_obj['etag'] == src_obj['etag'],\
                        'Objects etag did not match: %s and %s' % (src_obj['etag'], dst_obj['etag'])
                    match += 1
        if not minimal:
            assert match == (len(self.src_bucket_key_version) + len(self.src_bucket1_key_versions) + len(self.src_bucket2_key_versions)),\
                'All objects did not match'

    def validate_object_metadata_aws(self, boto3_site1, boto3_site2, src_bucket, dst_bucket, src_bucket1=None,
                                     src_bucket2=None, minimal=False):
        """
        Validate whether the size, etag, and versions of the replicated objects match as that of the
        objects in source bucket
        """
        self.src_bucket = src_bucket
        self.dst_bucket = dst_bucket
        self.src_bucket1 = src_bucket1
        self.src_bucket2 = src_bucket2
        self.src_bucket_key_version = self.src_bucket.get_all_versions()
        self.dst_bucket_key_version = self.dst_bucket.get_all_versions()
        self.src_bucket_key1 = []
        self.src_bucket_key2 = []
        self.src_bucket1_key_versions = []
        self.src_bucket2_key_versions = []
        src_obj_list = list()
        dst_obj_list = list()
        match = 0
        for key in self.src_bucket_key_version:
            my_key = boto3_site1.head_object(Bucket=self.src_bucket.name, Key=key.name, VersionId=key.version_id)
            raw_bucket_id = self.keyrouter.get_raw_bucket_id(self.src_bucket.name)
            bucket_id = self.convert_from_raw_bucket_id(raw_bucket_id)
            src_obj = {'name': key.name, 's3versionId': key.version_id,
                       'etag': self.src_bucket.get_key(key.name, version_id=key.version_id).etag,
                       'size': self.src_bucket.get_key(key.name, version_id=key.version_id).size,
                       'date': self.src_bucket.get_key(key.name, version_id=key.version_id).date,
                       'last-modified': my_key['ResponseMetadata']['HTTPHeaders']['last-modified'],
                       'bucket_id': str(bucket_id),
                       'bucket_name': self.src_bucket.name}
            src_obj_list.append(src_obj)

        if self.src_bucket1 is not None:
            self.src_bucket1_key_versions = self.src_bucket1.get_all_versions()
            for key in self.src_bucket1_key_versions:
                my_key = boto3_site1.head_object(Bucket=self.src_bucket1.name, Key=key.name, VersionId=key.version_id)
                raw_bucket_id = self.keyrouter.get_raw_bucket_id(self.src_bucket1.name)
                bucket_id = self.convert_from_raw_bucket_id(raw_bucket_id)
                src_obj = {'name': key.name, 's3versionId': key.version_id,
                           'etag': self.src_bucket1.get_key(key.name, version_id=key.version_id).etag,
                           'size': self.src_bucket1.get_key(key.name, version_id=key.version_id).size,
                           'date': self.src_bucket1.get_key(key.name, version_id=key.version_id).date,
                           'last-modified': my_key['ResponseMetadata']['HTTPHeaders']['last-modified'],
                           'bucket_id': str(bucket_id),
                           'bucket_name': self.src_bucket1.name
                           }
                src_obj_list.append(src_obj)

        if self.src_bucket2 is not None:
            self.src_bucket2_key_versions = self.src_bucket2.get_all_versions()
            for key in self.src_bucket2_key_versions:
                my_key = boto3_site1.head_object(Bucket=self.src_bucket2.name, Key=key.name, VersionId=key.version_id)
                raw_bucket_id = self.keyrouter.get_raw_bucket_id(self.src_bucket2.name)
                bucket_id = self.convert_from_raw_bucket_id(raw_bucket_id)
                src_obj = {'name': key.name, 's3versionId': key.version_id,
                           'etag': self.src_bucket2.get_key(key.name, version_id=key.version_id).etag,
                           'size': self.src_bucket2.get_key(key.name, version_id=key.version_id).size,
                           'date': self.src_bucket2.get_key(key.name, version_id=key.version_id).date,
                           'last-modified': my_key['ResponseMetadata']['HTTPHeaders']['last-modified'],
                           'bucket_id': str(bucket_id),
                           'bucket_name': self.src_bucket2.name
                           }
                src_obj_list.append(src_obj)

        for key in self.dst_bucket_key_version:
            my_key = boto3_site2.head_object(Bucket=self.dst_bucket.name, Key=key.name, VersionId=key.version_id)
            response = boto3_site2.get_object_tagging(Bucket=self.dst_bucket.name, Key=key.name,
                                                      VersionId=key.version_id)
            dst_obj = {'name': key.name, 's3versionId': key.version_id,
                       'etag': self.dst_bucket.get_key(key.name, version_id=key.version_id).etag,
                       'size': self.dst_bucket.get_key(key.name, version_id=key.version_id).size,
                       'date': self.dst_bucket.get_key(key.name, version_id=key.version_id).date}

            for tag in response['TagSet']:
                dst_obj[tag['Key']] = tag['Value']
            dst_obj_list.append(dst_obj)

        self.lg('\n')
        self.lg(src_obj_list)
        self.lg(dst_obj_list)

        for dst_obj in dst_obj_list:
            for src_obj in src_obj_list:
                if src_obj['s3versionId'] == dst_obj["com.wdc.activescale.versionid"]:
                    assert dst_obj['name'] == src_obj['name'], \
                        'Objects key did not match: %s and %s' % (src_obj['name'], dst_obj['name'])
                    assert dst_obj['size'] == src_obj['size'], \
                        'Objects size did not match: %s and %s' % (src_obj['size'], dst_obj['size'])
                    assert dst_obj['etag'] == src_obj['etag'], \
                        'Objects etag did not match: %s and %s' % (src_obj['etag'], dst_obj['etag'])
                    assert dst_obj["com.wdc.activescale.versionid"] == src_obj['s3versionId'], \
                        'Objects versionids did not match: %s and %s' % (
                        src_obj['s3versionId'], dst_obj["com.wdc.activescale.versionid"])
                    src_obj_time = src_obj['last-modified']
                    dst_obj_time = dst_obj["com.wdc.activescale.sourcetimestamp"]
                    src_obj_convert_time = datetime.datetime.strptime(src_obj_time, '%a, %d %b %Y %H:%M:%S %Z')
                    dst_obj_convert_time = datetime.datetime.strptime(dst_obj_time, '%a %b %d %H:%M:%S %Z %Y')
                    assert dst_obj_convert_time == src_obj_convert_time, \
                        'Objects timestamps did not match: %s and %s' % (src_obj_convert_time, dst_obj_convert_time)
                    assert dst_obj["com.wdc.activescale.bucketname"] == src_obj['bucket_name'], \
                        'Objects bucketname did not match: %s and %s' % (
                        src_obj['bucket_name'], dst_obj["com.wdc.activescale.bucketname"])
                    assert dst_obj["com.wdc.activescale.bucketid"] == src_obj['bucket_id'], \
                        'Objects bucketid did not match: %s and %s' % (
                        src_obj['bucket_id'], dst_obj["com.wdc.activescale.bucketid"])

                    match += 1

        if not minimal:
            assert match >= (len(self.src_bucket_key_version) + len(self.src_bucket1_key_versions) + len(
                self.src_bucket2_key_versions)), \
                'All objects did not match'

    def validate_object_metadata_aws_delete_marker(self, boto3_site1, boto3_site2, src_bucket, dst_bucket,
                                                   src_bucket1=None,
                                                   src_bucket2=None, minimal=False):
        """
        Validate whether the size, etag, and versions of the replicated objects match as that of the
        objects in source bucket
         """
        self.src_bucket = src_bucket
        self.dst_bucket = dst_bucket
        self.src_bucket1 = src_bucket1
        self.src_bucket2 = src_bucket2
        self.src_bucket_key_version = self.src_bucket.get_all_versions()
        self.dst_bucket_key_version = self.dst_bucket.get_all_versions()
        self.src_bucket_key1 = []
        self.src_bucket_key2 = []
        self.src_bucket1_key_versions = []
        self.src_bucket2_key_versions = []
        src_obj_list = list()
        dst_obj_list = list()
        match = 0

        for key in self.src_bucket_key_version:
            if isinstance(key, DeleteMarker):
                raw_bucket_id = self.keyrouter.get_raw_bucket_id(self.src_bucket.name)
                bucket_id = self.convert_from_raw_bucket_id(raw_bucket_id)
                src_obj = {'name': key.name, 's3versionId': key.version_id,
                           'size': 0,
                           'bucket_id': str(bucket_id),
                           'key': key,
                           'bucket_name': self.src_bucket.name}
            else:
                my_key = boto3_site1.head_object(Bucket=self.src_bucket.name, Key=key.name, VersionId=key.version_id)
                src_obj = {'name': key.name, 's3versionId': key.version_id,
                           'etag': self.src_bucket.get_key(key.name, version_id=key.version_id).etag,
                           'size': self.src_bucket.get_key(key.name, version_id=key.version_id).size,
                           'date': self.src_bucket.get_key(key.name, version_id=key.version_id).date,
                           'last-modified': my_key['ResponseMetadata']['HTTPHeaders']['last-modified'],
                           'bucket_id': str(bucket_id),
                           'key': key,
                           'bucket_name': self.src_bucket.name}
            src_obj_list.append(src_obj)

        for key in self.dst_bucket_key_version:
            my_key = boto3_site2.head_object(Bucket=self.dst_bucket.name, Key=key.name, VersionId=key.version_id)
            response = boto3_site2.get_object_tagging(Bucket=self.dst_bucket.name, Key=key.name,
                                                      VersionId=key.version_id)
            dst_obj = {'name': key.name, 's3versionId': key.version_id,
                       'etag': self.dst_bucket.get_key(key.name, version_id=key.version_id).etag,
                       'size': self.dst_bucket.get_key(key.name, version_id=key.version_id).size,
                       'date': self.dst_bucket.get_key(key.name, version_id=key.version_id).date}
            for tag in response['TagSet']:
                dst_obj[tag['Key']] = tag['Value']
            dst_obj_list.append(dst_obj)

        self.lg('\n')
        self.lg(src_obj_list)
        self.lg(dst_obj_list)

        for dst_obj in dst_obj_list:
            for src_obj in src_obj_list:
                if src_obj['s3versionId'] == dst_obj["com.wdc.activescale.versionid"]:
                    assert dst_obj['name'] == src_obj['name'], \
                        'Objects key did not match: %s and %s' % (src_obj['name'], dst_obj['name'])
                    assert dst_obj['size'] == src_obj['size'], \
                        'Objects size did not match: %s and %s' % (src_obj['size'], dst_obj['size'])
                    assert dst_obj["com.wdc.activescale.versionid"] == src_obj['s3versionId'], \
                        'Objects versionids did not match: %s and %s' % (
                                src_obj['s3versionId'], dst_obj["com.wdc.activescale.versionid"])
                    assert dst_obj["com.wdc.activescale.bucketname"] == src_obj['bucket_name'], \
                        'Objects bucketname did not match: %s and %s' % (
                                src_obj['bucket_name'], dst_obj["com.wdc.activescale.bucketname"])
                    assert dst_obj["com.wdc.activescale.bucketid"] == src_obj['bucket_id'], \
                        'Objects bucketid did not match: %s and %s' % (
                                src_obj['bucket_id'], dst_obj["com.wdc.activescale.bucketid"])
                    if isinstance(src_obj['key'], DeleteMarker):
                        assert dst_obj["com.wdc.activescale.requesttype"] == 'delete-marker', \
                            'Delete marker tag is not set'
                    match += 1

        if not minimal:
            assert match == (len(self.src_bucket_key_version)), 'All objects did not match'

class ValidateKeys(object):

    def __init__(self, keyrouter):
        self.keyrouter_ops = keyrouter


    def validate_keys_multipart_object_upload(self, bucket_name, part_count,
                                              job=False, timing_param=False):
        during = 'After' if job else 'Before'
        t_keys = 0 if timing_param else 1
        t_w_keys = 0 if timing_param else part_count + 1

        message = 'Multi-part upload successful'
        message += ' - temp keys deleted.' if timing_param else message
        status = True
        entries_dict = self.keyrouter_ops.iterate_bucket_objects(bucket_name, 'O',
                                                          '%s Running Flame Job : Multi-part upload completed, '
                                                          'timimg set %s' % (during, timing_param))

        if sum(key.endswith('M') for key in entries_dict) != 1:
            message = "Number of keys in O-vtype [%s] with suffix 'M' is not correct, " \
                      "should be %s " % (entries_dict, 1)
            status = False

        entries_dict = self.keyrouter_ops.iterate_bucket_objects(bucket_name, 'P',
                                                          '%s Running Flame Job : Multi-part upload completed, '
                                                          'timimg set %s' % (during, timing_param))

        if len(entries_dict) != part_count:
            message = "Number of parts in P-vtype [%s] is not correct, " \
                      "should be %s " % (entries_dict, part_count)
            status = False

        entries_dict = self.keyrouter_ops.iterate_bucket_objects(bucket_name, 'T',
                                                          '%s Running Flame Job : Multi-part upload completed, '
                                                          'timimg set %s' % (during, timing_param))

        if sum(key.endswith('K') for key in entries_dict) != t_keys:
            message = "Number of keys in T-vtype [%s] with suffix 'K' is not" \
                      " correct, should be %s " % (entries_dict, t_keys)
            status = False

        if sum(key.endswith('M') for key in entries_dict) != t_keys:
            message = "Number of keys in T-vtype [%s] with suffix 'M' is not" \
                      " correct, should be %s " % (entries_dict, t_keys)
            status = False

        if sum(key.endswith('W') for key in entries_dict) != t_w_keys:
            message = "Number of keys in T-vtype [%s] with suffix 'W' is not" \
                      " correct, should be %s " % (entries_dict, t_w_keys)
            status = False

        return message, status

    def validate_keys_mark_for_deletion(self, bucket_name, timing_param=False):
        key = 0 if timing_param else 1

        message = 'Multi-part delete successful'
        message += ' - all keys cleaned.' if timing_param else message
        status = True

        entries_dict = self.keyrouter_ops.iterate_bucket_objects(bucket_name, 'O',
                                                          'After deleting object and running Flame Job - Timing set %s'
                                                          % timing_param)

        if sum(key.endswith('K') for key in entries_dict) != key:
            message = "Number of keys [%s] with suffix 'K' is not" \
                      " correct, should be %s " % (entries_dict, key)
            status = False

        entries_dict = self.keyrouter_ops.iterate_bucket_objects(bucket_name, 'T',
                                                          'After deleting object and running Flame Job - Timing set %s'
                                                          % timing_param)

        if sum(key.endswith('K') for key in entries_dict) != key:
            message = "Number of keys [%s] with suffix 'K' is not" \
                      " correct, should be %s " % (entries_dict, key)
            status = False

        if sum(key.endswith('M') for key in entries_dict) != key:
            message = "Number of keys [%s] with suffix 'K' is not" \
                      " correct, should be %s " % (entries_dict, key)
            status = False

        return message, status

    def validate_keys_object_overwrite(self, bucket_name, part_count,
                                       overwrite=0, job=False, timing_param=False):
        duration = 'After' if job else 'Before'
        total_parts = part_count

        t_w_key = 0 if job else part_count + 1 + overwrite
        t_k_key = 0 if timing_param else 1 + overwrite
        t_m_key = 0 if timing_param else 1 + overwrite
        o_m_key = 2 if overwrite == 1 else 1
        if job:
            o_m_key = 1

        message = 'Multi-part overwrite successful'
        message += ' - all keys cleaned.' if timing_param else message
        status = True

        entries_dict = self.keyrouter_ops.iterate_bucket_objects(bucket_name, 'O',
                                                          '%s Flame Job - overwrite object, timing set %s'
                                                          % (duration, timing_param))

        if sum(key.endswith('M') for key in entries_dict) != o_m_key:
            message = "Number of keys in [%s] with suffix 'M' is not" \
                      " correct, should be %s " % (entries_dict, o_m_key)
            status = False

        entries_dict = self.keyrouter_ops.iterate_bucket_objects(bucket_name, 'P',
                                                          '%s Flame Job - overwrite object, timing set %s'
                                                          % (duration, timing_param))

        if len(entries_dict) != total_parts:
            message = "Number of parts in [%s] is not" \
                      "correct, should be %s " % (entries_dict, total_parts)
            status = False

        entries_dict = self.keyrouter_ops.iterate_bucket_objects(bucket_name, 'T',
                                                          '%s Flame Job - overwrite object, timing set %s'
                                                          % (duration, timing_param))

        if sum(key.endswith('K') for key in entries_dict) != t_k_key:
            message = "Number of keys in [%s] with suffix 'K' is not" \
                      " correct, should be %s " % (entries_dict, t_k_key)
            status = False

        if sum(key.endswith('M') for key in entries_dict) != t_m_key:
            message = "Number of keys in [%s] with suffix 'M' is not" \
                      " correct, should be %s " % (entries_dict, t_m_key)
            status = False

        if sum(key.endswith('W') for key in entries_dict) != t_w_key:
            message = "Number of keys in [%s] with suffix 'W' is not" \
                      " correct, should be %s " % (entries_dict, t_w_key)
            status = False

        return message, status

    def validate_keys_object_abort(self, bucket_name, part_count,
                                   job=False, timing_param=False):
        duration = 'After' if job else 'Before'
        t_w_key = 0 if timing_param else part_count + 1
        t_k_key = 0 if timing_param else 1
        t_m_key = 0 if timing_param else 1

        message = 'Multi-part abort successful'
        message += ' - all keys cleaned.' if timing_param else message
        status = True

        entries_dict = self.keyrouter_ops.iterate_bucket_objects(bucket_name, 'T',
                                                          '%s Flame Job - aborted object, timing set %s'
                                                          % (duration, timing_param))

        if sum(key.endswith('K') for key in entries_dict) != t_k_key:
            message = "Number of keys in [%s] with suffix 'K' is not" \
                      " correct, should be %s " % (entries_dict, t_k_key)
            status = False

        if sum(key.endswith('M') for key in entries_dict) != t_m_key:
            message = "Number of keys in [%s] with suffix 'M' is not" \
                      " correct, should be %s " % (entries_dict, t_m_key)
            status = False

        if sum(key.endswith('W') for key in entries_dict) != t_w_key:
            message = "Number of keys in [%s] with suffix 'W' is not" \
                      " correct, should be %s " % (entries_dict, t_w_key)
            status = False

        return message, status

    def validate_keys_object_upload(self, bucket_name, part_count,
                                    job=False, timing_param=False,
                                    single_object_count=1, multipart_object_count=1,
                                    delete_multipart=False, delete_singlepart=False,
                                    old_keys=0):
        during = 'After' if job else 'Before'
        t_keys = 0 if timing_param else multipart_object_count + old_keys
        t_w_keys = 0 if job else part_count + multipart_object_count

        message = 'Object upload successful'
        message += ' - temp keys deleted.' if timing_param else message
        status = True
        entries_dict = self.keyrouter_ops.iterate_bucket_objects(bucket_name, 'O',
                                                          '%s Running Flame Job, '
                                                          'timimg set %s' % (during, timing_param))

        if sum(key.endswith('W') for key in entries_dict) != single_object_count:
            message = "Number of keys in O-vtype [%s] with suffix 'W' is not correct, " \
                      "should be %s " % (entries_dict, single_object_count)
            status = False

        if sum(key.endswith('M') for key in entries_dict) != multipart_object_count:
            message = "Number of keys in O-vtype [%s] with suffix 'M' is not correct, " \
                      "should be %s " % (entries_dict, multipart_object_count)
            status = False

        if delete_multipart:
            if sum(key.endswith('K') for key in entries_dict) != multipart_object_count:
                message = "Number of keys in O-vtype [%s] with suffix 'K' is not correct, " \
                          "should be %s " % (entries_dict, 1)
                status = False

        if delete_singlepart:
            if sum(key.endswith('K') for key in entries_dict) != single_object_count:
                message = "Number of keys in O-vtype [%s] with suffix 'K' is not correct, " \
                          "should be %s " % (entries_dict, 1)
                status = False

        entries_dict = self.keyrouter_ops.iterate_bucket_objects(bucket_name, 'P',
                                                          '%s Running Flame Job, '
                                                          'timimg set %s' % (during, timing_param))

        if len(entries_dict) != part_count:
            message = "Number of parts in P-vtype [%s] is not correct, " \
                      "should be %s " % (entries_dict, part_count)
            status = False

        entries_dict = self.keyrouter_ops.iterate_bucket_objects(bucket_name, 'T',
                                                          '%s Running Flame Job, '
                                                          'timimg set %s' % (during, timing_param))

        if sum(key.endswith('K') for key in entries_dict) != t_keys:
            message = "Number of keys in T-vtype [%s] with suffix 'K' is not" \
                      " correct, should be %s " % (entries_dict, t_keys)
            status = False

        if sum(key.endswith('M') for key in entries_dict) != t_keys:
            message = "Number of keys in T-vtype [%s] with suffix 'M' is not" \
                      " correct, should be %s " % (entries_dict, t_keys)
            status = False

        if sum(key.endswith('W') for key in entries_dict) != t_w_keys:
            message = "Number of keys in T-vtype [%s] with suffix 'W' is not" \
                      " correct, should be %s " % (entries_dict, t_w_keys)
            status = False

        return message, status

class FlameConstants(object):
    FLAME_CAPACITY = 'scalerdb_foreground'
    FLAME_GC_OLM = 'scalerdb_background'
    FLAME_COMPLETE = 'scalerdb'
    FLAME_OLM = 'olm_scalerdb'
    FLAME_GC = 'gc_scalerdb'
    FLAME_CAPACITY_OLD = 'capacity_scalerdb'