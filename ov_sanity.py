__author__ = 'Mani'
from tests.common.utils_new import LocalUtils, Metering, ScalerKeyrouter, FlameUtils, ScalerConfigParser
from uuid import uuid4
import time
import unittest

ACCESS_KEY = 'iwglsgvoxxn3v3vkffhv7a9b8e8838ec'
SECRET_KEY = '3eni46tq4kokcyagfiz74ebhnnf4stk7fqgewz7kc7mroakvdurbx35vgfsmkdus'
VERIFIER_OBJECT_OK = "ok"
VERIFIER_OBJECT_LINK_BROKEN = "link_broken"
VERIFIER_OBJECT_SIZE_MISMATCH = "size_mismatch"
VERIFIER_OBJECT_ETAG_MISMATCH = "etag_mismatch"
VERIFIER_OBJECT_LINK_UNAVAILABLE = "link_unavailable"
VERIFIER_OK_CSV_FILE_NAME = "object_verifier_report_ok.csv"
VERIFIER_OK_CSV_GZ_FILE_NAME = "object_verifier_report_ok.csv.gz"
VERIFIER_CRITICAL_CSV_FILE_NAME = "object_verifier_report_critical_pending.csv"
VERIFIER_CRITICAL_CSV_GZ_FILE_NAME = "object_verifier_report_critical_pending.csv.gz"
VERIFIER_MISSING_PART = "missing_part"
VERIFIER_SIZE_MISMATCH = "mp_obj_size_inconsistent"
VERIFIER_OBJECT_MP_ETAG_MISMATCH = "mp_obj_etag_inconsistent"
VERIFIER_OBJECT_MP_DBKEY_MISMATCH = "mp_obj_part_dbkey_inconsistent"
VERIFIER_OBJECT_MP_OFFSET_MISMATCH = "mp_byte_offset_inconsistent"
VERIFIER_OBJECT_MP_UPLOADID_MISMATCH = "mp_obj_uploadid_inconsistent"

class TestFlameObjectVerifier(LocalUtils):

    def setUp(self):
        super(TestFlameObjectVerifier, self).setUp()
        self.flame = FlameUtils(self.env, self.scalers)
        self.cfg_flame = []
        self.lg('Modifying job_duration_days for verifier')
        for node in self.scalers:
            self.cfg_flame.append(ScalerConfigParser(node, 'flame'))
        for config in self.cfg_flame:
            config.update_config("workitem.scalerdb_verify", "job_duration_days", 0)
        self.flame.gc_disable()
        self.meter = Metering(self.env, self.m, self.env_info, self.scalers, self.et.hardware)
        self.keyrouter = ScalerKeyrouter(self.scalers)
        self.user_conn = self.s3_ops.get_s3_connection()
        self.bucket_name = 'bucket-%s' % uuid4()
        self.boto_backend = self.s3_ops_backend.get_s3_column_connection()
        self.multipart_file = 'multipart_object'
        self.multipart_file_size = 1073741824
        self.chunk_size = 102428800

    def tearDown(self):
        super(TestFlameObjectVerifier, self).tearDown()
        self.flame.gc_enable()
        if hasattr(self, "_buckets_to_clean"):
            try:
                for bucket in self._buckets_to_clean:
                    buck_obj = self.user_conn.get_bucket(bucket)
                    obj_version_id_upload = {}
                    a = buck_obj.get_all_versions()
                    for id in a:
                        obj_version_id_upload[id.version_id] = id.name
                    for key, value in obj_version_id_upload.iteritems():
                        buck_obj.delete_key(value, version_id=key)

                for bucket in self._buckets_to_clean:
                    self.s3_ops.delete_bucket(self.user_conn, bucket)
            except:
                print "exception"

    def validate_size_etag(self, bucket_name, object_index, backend_buckname, backend_obj):
        entries_dict_size = self.keyrouter.iterate_versioning_backend_bucket_objects_size(bucket_name, 'O',
                                                                                'before flame job', object_index)
        self.lg('Object size is %s' % entries_dict_size)
        self.lg('Backend buck name is %s' % backend_buckname)
        self.lg('backend obj is %s' % backend_obj)
        size, etag = self.s3_ops_backend.get_object_size(self.boto_backend, backend_buckname, backend_obj)
        print "entries_dict_size:", entries_dict_size
        print "size:", size
        print "backend etag", etag

        if size is None and etag is None:
            if entries_dict_size != 0:
                self.lg("object does not exist in backend")
                return False
        if int(entries_dict_size) != int(size):
           self.lg("Object exist in backend but size mismatches entries_dict_size:%s size:%s" %(entries_dict_size, size))
           return False
        self.lg("Object exist with valid size and etag")
        return True

    def validate_ok_report(self):
        self.lg('Check for ok report in the csv file')
        th_file_exists_bucket, th_count_bucket = \
        self.s3_ops.browse_system_bucket_for_file(file_ext="object_verifier_report_ok.csv.gz", clean=False)
        print "th_file_exists_bucket" , th_file_exists_bucket
        print "th_count_bucket", th_count_bucket
        self.assertTrue(th_count_bucket == self.init_count_bucket + 1,
                            'New report not uploaded to system bucket after verifier job')

    def validate_backend_object(self, bucket_name, object_index, versionId='null', errorType='', part_number=0,
                                kill_marker=False):
        self.lg("validating bucket_name: %s object:obj-%s versionId:%s" % (bucket_name, object_index, versionId))

        if part_number != 0:
            entries_dict = self.keyrouter.iterate_versioning_multipart_backend_bucket_objects(bucket_name, 'O',
                                                                                              'before flame job',
                                                                                              object_index, part_number)
        else:
            entries_dict = self.keyrouter.iterate_versioning_backend_bucket_objects(bucket_name, 'O',
                                                                                    'before flame job', object_index)
        self.lg('Entries_dict is %s' % entries_dict)
        entries_list = entries_dict.split('/')
        self.backend_buckname = entries_list[1]
        self.backend_obj = entries_list[2]
        self.lg('Backend buck name is %s' % self.backend_buckname)
        self.lg('backend obj is %s' % self.backend_obj)

        valid_obj = True

        self.lg('Validate size and etag')
        if not kill_marker:
            if not self.validate_size_etag(bucket_name, object_index, self.backend_buckname, self.backend_obj):
                valid_obj = False
        else:
            valid_obj = False
        if not valid_obj:
            self.validate_csv(bucket_name=bucket_name, object_index=object_index, errorType=errorType,
                              part_number=part_number)

    def validate_csv(self, bucket_name, object_index, errorType='', part_number=0, validate_full_key=False, full_key=None):
        object_found = False
        self.lg('Check for broken object in the csv file')
        th_file_exists_bucket, th_count_bucket = \
            self.s3_ops.browse_system_bucket_for_file(file_ext=VERIFIER_CRITICAL_CSV_GZ_FILE_NAME, clean=False)
        print "th_file_exists_bucket", th_file_exists_bucket
        print "th_count_bucket", th_count_bucket
        self.assertTrue(th_count_bucket == self.init_count_bucket + 1,
                        'New report not uploaded to system bucket after verifier job')

        csvfile = self.s3_ops.get_csv_contents('object_verifier')
        for metering_stats in csvfile:
            print "csvfile.....", metering_stats
            if metering_stats['Bucket Name'] == bucket_name:
                obj_name = 'obj-%s' % object_index
                print metering_stats['Object Name'], obj_name
                if metering_stats['Object Name'] == obj_name and metering_stats['Part Number'] == str(part_number) and \
                        metering_stats['Error'] == errorType:
                    object_found = True
                if validate_full_key:
                    if metering_stats['Full Key'] in full_key:
                        full_key_validation = True
                    else:
                        full_key_validation = False
                    self.assertTrue(full_key_validation, "Multiple version mismatch of OOP key")

        self.assertTrue(object_found, "Object  not found in csv")

    def test_001_single_object_version_enable_link_broken(self):


        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Enabling versioing on bucket %s' % self.bucket_name)
        self.bucket.configure_versioning(versioning=True)
        time.sleep(60)
        self.assertTrue(self.bucket.get_versioning_status()['Versioning'] == 'Enabled',
                        'Versioning not enabled for bucket %s' % self.bucket_name)
        responseid, status, reason, versionId = self.s3_ops.upload_single_object(self.user_conn, self.bucket_name,
                                                                     key='obj-0', data='x' * 101)
        self.assertTrue(status == 200, reason)

        self.validate_backend_object(self.bucket_name, 0, versionId)
        self.s3_ops_backend.delete_object(self.boto_backend, self.backend_buckname, self.backend_obj)
        self.assertTrue(status == 200, reason)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status('object_verifier_report_pending.csv'),
                         'Reports still present in local scalers')
        self.validate_backend_object(self.bucket_name, 0, versionId, VERIFIER_OBJECT_LINK_BROKEN)

    def test_002_single_object_version_enable_size_mismatch(self):


        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Enabling versioing on bucket %s' % self.bucket_name)
        self.bucket.configure_versioning(versioning=True)
        time.sleep(60)
        self.assertTrue(self.bucket.get_versioning_status()['Versioning'] == 'Enabled',
                        'Versioning not enabled for bucket %s' % self.bucket_name)
        responseid, status, reason, versionId = self.s3_ops.upload_single_object(self.user_conn, self.bucket_name,
                                                                     key='obj-0', data='x' * 150)
        self.assertTrue(status == 200, reason)

        self.validate_backend_object(self.bucket_name, 0, versionId)

        self.lg("overriding object obj-0 backend bucket:%s backend object:%s" %(self.backend_buckname, self.backend_obj))
        responseid, status, reason, versionId = self.s3_ops.upload_single_object(self.boto_backend, self.backend_buckname ,
                                                                     key=self.backend_obj, data='x' * 101)
        self.assertTrue(status == 200, reason)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status('object_verifier_report_pending.csv'),
                         'Reports still present in local scalers')
        self.validate_backend_object(self.bucket_name, 0, versionId, VERIFIER_OBJECT_SIZE_MISMATCH)


    def test_003_single_object_version_enable_etag_mismatch(self):


        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Enabling versioing on bucket %s' % self.bucket_name)
        self.bucket.configure_versioning(versioning=True)
        time.sleep(60)
        self.assertTrue(self.bucket.get_versioning_status()['Versioning'] == 'Enabled',
                        'Versioning not enabled for bucket %s' % self.bucket_name)
        responseid, status, reason, versionId = self.s3_ops.upload_single_object(self.user_conn, self.bucket_name,
                                                                     key='obj-0', data='x' * 150)
        self.assertTrue(status == 200, reason)

        self.validate_backend_object(self.bucket_name, 0, versionId)

        self.lg("overriding object obj-0 backend bucket:%s backend object:%s" %(self.backend_buckname, self.backend_obj))
        responseid, status, reason, versionId = self.s3_ops.upload_single_object(self.boto_backend, self.backend_buckname ,
                                                                     key=self.backend_obj, data='a' * 150)
        self.assertTrue(status == 200, reason)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status('object_verifier_report_pending.csv'),
                         'Reports still present in local scalers')
        self.validate_backend_object(self.bucket_name, 0, versionId, VERIFIER_OBJECT_ETAG_MISMATCH)

    def test_004_zero_size_single_object_version_enable(self):


        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Enabling versioing on bucket %s' % self.bucket_name)
        self.bucket.configure_versioning(versioning=True)
        time.sleep(60)
        self.assertTrue(self.bucket.get_versioning_status()['Versioning'] == 'Enabled',
                        'Versioning not enabled for bucket %s' % self.bucket_name)
        responseid, status, reason, versionId = self.s3_ops.upload_single_object(self.user_conn, self.bucket_name,
                                                                     key='obj-0', data='x' * 0)
        self.assertTrue(status == 200, reason)
        entries_dict_size = self.keyrouter.iterate_versioning_backend_bucket_objects_size(self.bucket_name, 'O',
                                                                                'before flame job', 0)
        self.assertEqual(entries_dict_size, str(0))
        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status('object_verifier_report_ok.csv'),
                         'Reports still present in local scalers')
        self.validate_ok_report()

    def test_005_multiple_object_version_enable_link_broken(self):
        self.flame.clean_local_reports()
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)
        self.lg("1. Clean up all existing bucket capacity reports")
        self.flame.clean_local_reports()

        file_exists_bucket, init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                          clean=True)
        self.assertTrue(init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Enabling versioing on bucket %s' % self.bucket_name)
        self.bucket.configure_versioning(versioning=True)
        time.sleep(60)
        self.assertTrue(self.bucket.get_versioning_status()['Versioning'] == 'Enabled',
                        'Versioning not enabled for bucket %s' % self.bucket_name)

        self.assertTrue(self.bucket.get_versioning_status()['Versioning'] == 'Enabled',
                        'Versioning not enabled for bucket %s' % self.bucket_name)

        object_list = list()
        for i in range(3):
            responseid, status, reason, versionId = self.s3_ops.upload_single_object(self.user_conn, self.bucket_name,
                                                                     key='obj-%s' % i, data='x' * 101)
            self.assertTrue(status == 200, reason)
            key = dict()
            key['bucket_name'] = self.bucket_name
            key['object_index'] = i
            key['version_id'] = versionId
            key['part_number'] = 0
            object_list.append(key)

        for i in range(2):
            obj = object_list[i]
            self.lg("deleting backend link of object:obj-%s, bucket:%s, version:%s"%(obj['object_index'], obj['bucket_name'], obj['version_id']))
            self.validate_backend_object(obj['bucket_name'], obj['object_index'], obj['version_id'])
            self.s3_ops_backend.delete_object(self.boto_backend, self.backend_buckname, self.backend_obj)
            self.assertTrue(status == 200, reason)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))

        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status('object_verifier_report_pending.csv'),
                         'Reports still present in local scalers')
        for obj in object_list:
            self.validate_backend_object(obj['bucket_name'], obj['object_index'], obj['version_id'], VERIFIER_OBJECT_LINK_BROKEN)

    def test_006_multiple_object_version_enable_link_broken_size_mismatch_zero_size(self):
        self.flame.clean_local_reports()
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)
        self.lg("1. Clean up all existing bucket capacity reports")
        self.flame.clean_local_reports()

        file_exists_bucket, init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                          clean=True)
        self.assertTrue(init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Enabling versioing on bucket %s' % self.bucket_name)
        self.bucket.configure_versioning(versioning=True)
        time.sleep(60)
        self.assertTrue(self.bucket.get_versioning_status()['Versioning'] == 'Enabled',
                        'Versioning not enabled for bucket %s' % self.bucket_name)

        self.assertTrue(self.bucket.get_versioning_status()['Versioning'] == 'Enabled',
                        'Versioning not enabled for bucket %s' % self.bucket_name)

        object_list = list()
        for i in range(5):
            responseid, status, reason, versionId = self.s3_ops.upload_single_object(self.user_conn, self.bucket_name,
                                                                                     key='obj-%s' % i, data='x' * 101)
            self.assertTrue(status == 200, reason)
            key = dict()
            key['bucket_name'] = self.bucket_name
            key['object_index'] = i
            key['version_id'] = versionId
            key['part_number'] = 0
            object_list.append(key)

        for i in range(2):
            obj = object_list[i]
            self.lg("deleting backend link of object:obj-%s, bucket:%s, version:%s" % (
                obj['object_index'], obj['bucket_name'], obj['version_id']))
            self.validate_backend_object(obj['bucket_name'], obj['object_index'], obj['version_id'])
            self.s3_ops_backend.delete_object(self.boto_backend, self.backend_buckname, self.backend_obj)
            self.assertTrue(status == 200, reason)

        self.lg(
            "overriding object obj-2 backend bucket:%s backend object:%s" % (self.backend_buckname, self.backend_obj))

        obj1 = object_list[2]

        self.validate_backend_object(obj1['bucket_name'], obj1['object_index'], obj1['version_id'])

        responseid, status, reason, versionId = self.s3_ops.upload_single_object(self.boto_backend,
                                                                                 self.backend_buckname,
                                                                                 key=self.backend_obj, data='x' * 200)
        self.assertTrue(status == 200, reason)

        responseid, status, reason, versionId = self.s3_ops.upload_single_object(self.user_conn, self.bucket_name,
                                                                                 key='obj-6', data='x' * 0)
        self.assertTrue(status == 200, reason)
        entries_dict_size = self.keyrouter.iterate_versioning_backend_bucket_objects_size(self.bucket_name, 'O',
                                                                                          'before flame job', 5)
        self.assertEqual(entries_dict_size, str(0))
        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status('object_verifier_report_pending.csv'),
                         'Reports still present in local scalers')

        for i in range(2):
            obj = object_list[i]
            self.validate_backend_object(obj['bucket_name'], obj['object_index'], obj['version_id'],
                                         VERIFIER_OBJECT_LINK_BROKEN)

        self.validate_backend_object(obj1['bucket_name'], obj1['object_index'], obj1['version_id'],
                                     VERIFIER_OBJECT_SIZE_MISMATCH)

    def test_007_multi_part_version_enable_link_broken(self):
        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Enabling versioing on bucket %s' % self.bucket_name)
        self.bucket.configure_versioning(versioning=True)
        time.sleep(60)
        self.assertTrue(self.bucket.get_versioning_status()['Versioning'] == 'Enabled',
                        'Versioning not enabled for bucket %s' % self.bucket_name)
        self.lg('Upload a multipart object onto source bucket in site1.')
        self.file_size = 1073741824
        self.chunk_size = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.validate_backend_object(self.bucket_name, 1, errorType='', part_number=4)

        self.s3_ops_backend.delete_object(self.boto_backend, self.backend_buckname, self.backend_obj)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status('object_verifier_report_pending.csv'),
                         'Reports still present in local scalers')
        self.validate_backend_object(self.bucket_name, 1, errorType=VERIFIER_OBJECT_LINK_BROKEN, part_number=4)

    def test_008_multi_part_version_enable_multiple_link_broken(self):
        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Enabling versioing on bucket %s' % self.bucket_name)
        self.bucket.configure_versioning(versioning=True)
        time.sleep(60)
        self.assertTrue(self.bucket.get_versioning_status()['Versioning'] == 'Enabled',
                        'Versioning not enabled for bucket %s' % self.bucket_name)
        self.lg('Upload a multipart object onto source bucket in site1.')
        self.file_size = 1073741824
        self.chunk_size = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.validate_backend_object(self.bucket_name, 1, errorType='', part_number=5)
        self.s3_ops_backend.delete_object(self.boto_backend, self.backend_buckname, self.backend_obj)

        self.validate_backend_object(self.bucket_name, 1, errorType='', part_number=7)
        self.s3_ops_backend.delete_object(self.boto_backend, self.backend_buckname, self.backend_obj)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status('object_verifier_report_pending.csv'),
                         'Reports still present in local scalers')
        self.validate_backend_object(self.bucket_name, 1, errorType=VERIFIER_OBJECT_LINK_BROKEN, part_number=5)
        self.validate_backend_object(self.bucket_name, 1, errorType=VERIFIER_OBJECT_LINK_BROKEN, part_number=7)

    def test_009_multi_part_version_enable_version_kill_marker_link_broken(self):
        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")

        self._buckets_to_clean = []
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Enabling versioing on bucket %s' % self.bucket_name)
        self.bucket.configure_versioning(versioning=True)
        time.sleep(60)
        self.assertTrue(self.bucket.get_versioning_status()['Versioning'] == 'Enabled',
                        'Versioning not enabled for bucket %s' % self.bucket_name)
        self.lg('Upload a multipart object onto bucket %s' % self.bucket_name)
        self.file_size = 1073741824
        self.chunk_size = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.lg("Getting backend object path")
        entries_dict = self.keyrouter.iterate_versioning_multipart_backend_bucket_objects(self.bucket_name, 'O',
                                                                                          'before flame job',
                                                                                          object_index=1, part_number=5)
        self.lg('Entries_dict is %s' % entries_dict)
        entries_list = entries_dict.split('/')
        self.backend_buckname = entries_list[1]
        self.backend_obj = entries_list[2]
        self.s3_ops.delete_all_versions(self.user_conn, self.bucket_name)
        self.lg("Deleting backend object path %s/%s" % (self.backend_buckname, self.backend_obj))
        self.s3_ops_backend.delete_object(self.boto_backend, self.backend_buckname, self.backend_obj)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status('object_verifier_report_pending.csv'),
                         'Reports still present in local scalers')
        self.lg('Check for broken object in the csv file')
        self.validate_ok_report()

    def test_010_multi_part_version_enable_kill_marker_link_broken(self):
        self.lg("1. Clean up all existing bucket capacity reports")

        self._buckets_to_clean = []
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Enabling versioing on bucket %s' % self.bucket_name)
        self.bucket.configure_versioning(versioning=True)
        time.sleep(60)
        self.assertTrue(self.bucket.get_versioning_status()['Versioning'] == 'Enabled',
                        'Versioning not enabled for bucket %s' % self.bucket_name)
        self.lg('Upload a multipart object onto bucket %s' % self.bucket_name)
        self.file_size = 1073741824
        self.chunk_size = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.lg("Getting backend object path")
        entries_dict = self.keyrouter.iterate_versioning_multipart_backend_bucket_objects(self.bucket_name, 'O',
                                                                                          'before flame job',
                                                                                          object_index=1, part_number=5)
        self.lg('Entries_dict is %s' % entries_dict)
        entries_list = entries_dict.split('/')
        self.backend_buckname = entries_list[1]
        self.backend_obj = entries_list[2]
        self.lg("deleting object %s" % self.multipart_file)
        self.s3_ops.delete_object(self.user_conn, self.bucket_name, self.multipart_file)
        time.sleep(60)
        self.lg("Deleting backend object path %s/%s" % (self.backend_buckname, self.backend_obj))
        self.s3_ops_backend.delete_object(self.boto_backend, self.backend_buckname, self.backend_obj)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status('object_verifier_report_pending.csv'),
                         'Reports still present in local scalers')
        self.lg('Check for broken object in the csv file')
        self.validate_backend_object(self.bucket_name, object_index=1, errorType=VERIFIER_OBJECT_LINK_BROKEN,
                                     part_number=5, kill_marker=True)

    def test_011_single_object_version_disable_link_broken(self):


        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        responseid, status, reason, versionId = self.s3_ops.upload_single_object(self.user_conn, self.bucket_name,
                                                                     key='obj-0', data='x' * 101)
        self.assertTrue(status == 200, reason)

        self.validate_backend_object(self.bucket_name, 0, versionId)
        self.s3_ops_backend.delete_object(self.boto_backend, self.backend_buckname, self.backend_obj)
        self.assertTrue(status == 200, reason)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status('object_verifier_report_pending.csv'),
                         'Reports still present in local scalers')
        self.validate_backend_object(self.bucket_name, 0, versionId, VERIFIER_OBJECT_LINK_BROKEN)

    def test_012_multi_part_version_disable_link_broken(self):
        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Upload a multipart object onto source bucket in site1.')
        self.file_size = 1073741824
        self.chunk_size = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.validate_backend_object(self.bucket_name, 1, errorType='', part_number=4)

        self.s3_ops_backend.delete_object(self.boto_backend, self.backend_buckname, self.backend_obj)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status('object_verifier_report_pending.csv'),
                         'Reports still present in local scalers')
        self.validate_backend_object(self.bucket_name, 1, errorType=VERIFIER_OBJECT_LINK_BROKEN, part_number=4)

    def test_013_multi_part_version_disable_overwrite_link_broken(self):
        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Upload a multipart object onto source bucket in site1.')
        self.file_size = 1073741824
        self.chunk_size = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.validate_backend_object(self.bucket_name, 1, errorType='', part_number=4)

        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.s3_ops_backend.delete_object(self.boto_backend, self.backend_buckname, self.backend_obj)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status('object_verifier_report_pending.csv'),
                         'Reports still present in local scalers')
        self.validate_ok_report()

    def test_014_multi_part_key_deletion(self):
        """
        Upload the multipart object and delete one part and
        validate missing_part error is generated or not
        :return:
        """
        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Upload a multipart object onto source bucket in site1.')
        self.file_size = 1073741824
        self.chunk_size = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.validate_backend_object(self.bucket_name, 1, errorType='')

        object_key = self.keyrouter.remove_one_part_object(bucket_name=self.bucket_name, vtype='O', part_number=4)

        time.sleep(5)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status(VERIFIER_CRITICAL_CSV_FILE_NAME),
                         'Reports still present in local scalers')
        self.validate_csv(self.bucket_name, 1, errorType=VERIFIER_MISSING_PART)

    def test_015_multi_part_size_mismatch_of_part_object(self):
        """
        Upload the multipart object and modify the size of the object and
        validate mp_obj_size_inconsistent error is generated or not
        :return:
        """
        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Upload a multipart object onto source bucket in site1.')
        self.file_size = 1073741824
        self.chunk_size = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.validate_backend_object(self.bucket_name, 1, errorType='')

        self.keyrouter.modify_multi_part_object_size(bucket_name=self.bucket_name, file_name=self.multipart_file)

        time.sleep(5)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status(VERIFIER_CRITICAL_CSV_FILE_NAME),
                         'Reports still present in local scalers')
        self.validate_csv(self.bucket_name, 1, errorType=VERIFIER_SIZE_MISMATCH)

    def test_016_multi_part_object_etag_mismatch(self):
        """
        Upload the multipart object and modify the etag of part key
        validate mp_obj_etag_inconsistent error is generated or not
        :return:
        """
        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Upload a multipart object onto source bucket in site1.')
        self.file_size = 1073741824
        self.chunk_size = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.validate_backend_object(self.bucket_name, 1, errorType='')

        self.keyrouter.modify_multi_part_etag_of_part_key(bucket_name=self.bucket_name, part_number=4)

        time.sleep(5)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status(VERIFIER_CRITICAL_CSV_FILE_NAME),
                         'Reports still present in local scalers')
        self.validate_csv(self.bucket_name, 1, errorType=VERIFIER_OBJECT_MP_ETAG_MISMATCH)

    def test_017_multi_part_object_dbkey_mismatch(self):
        """
        Upload the multipart object and modify the dkey of part key
        validate mp_obj_part_dbkey_inconsistent error is generated or not
        :return:
        """
        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Upload a multipart object onto source bucket in site1.')
        self.file_size = 1073741824
        self.chunk_size = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.validate_backend_object(self.bucket_name, 1, errorType='', part_number=4)

        self.keyrouter.modify_multi_part_dbkey_type_of_part_key(bucket_name=self.bucket_name, part_number=4)

        time.sleep(5)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status(VERIFIER_CRITICAL_CSV_FILE_NAME),
                         'Reports still present in local scalers')
        self.validate_csv(self.bucket_name, 1, errorType=VERIFIER_OBJECT_MP_DBKEY_MISMATCH, part_number=4)

    def test_018_multi_part_object_offset_mismatch(self):
        """
        Upload the multipart object and modify the checksum of part key
        validate mp_byte_offset_inconsistent error is generated or not
        :return:
        """
        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Upload a multipart object onto source bucket in site1.')
        self.file_size = 1073741824
        self.chunk_size = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.validate_backend_object(self.bucket_name, 1, errorType='', part_number=4)

        self.keyrouter.modify_multi_part_filp_the_last_byte_offset(bucket_name=self.bucket_name, part_number=4)

        time.sleep(5)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status(VERIFIER_CRITICAL_CSV_FILE_NAME),
                         'Reports still present in local scalers')
        self.validate_csv(self.bucket_name, 1, errorType=VERIFIER_OBJECT_MP_OFFSET_MISMATCH, part_number=4)

    def test_019_multi_part_size_mismatch_of_part_key(self):
        """
        Upload the multipart object and modify the size of part key
        validate mp_obj_size_inconsistent error is generated or not
        :return:
        """
        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Upload a multipart object onto source bucket in site1.')
        self.file_size = 1073741824
        self.chunk_size = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.validate_backend_object(self.bucket_name, 1, errorType='')

        self.keyrouter.modify_multi_part_size_of_part_key(bucket_name=self.bucket_name, part_number=4)

        time.sleep(5)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status(VERIFIER_CRITICAL_CSV_FILE_NAME),
                         'Reports still present in local scalers')
        self.validate_csv(self.bucket_name, 1, errorType=VERIFIER_SIZE_MISMATCH)

    def test_020_multi_part_upload_id_mismatch_of_part_key(self):
        """
        Upload the multipart object and modify the upload id of part key
        validate mp_obj_uploadid_inconsistent error is generated or not
        :return:
        """
        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]
        self.lg('Upload a multipart object onto source bucket in site1.')
        self.file_size = 1073741824
        self.chunk_size = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size, self.chunk_size)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.validate_backend_object(self.bucket_name, 1, errorType='', part_number=4)

        self.keyrouter.modify_multi_part_upload_id_of_part_key(bucket_name=self.bucket_name, part_number=4)

        time.sleep(5)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status(VERIFIER_CRITICAL_CSV_FILE_NAME),
                         'Reports still present in local scalers')
        self.validate_csv(self.bucket_name, 1, errorType=VERIFIER_OBJECT_MP_UPLOADID_MISMATCH, part_number=4)

    def test_021_multi_version_of_mp_object_size_mismatch(self):
        """
        Upload the two different mp objects with the same name and modify the size of oop key in one of the mp object
        save oop key before and after executing verifier job, it should be same
        """
        self.flame.clean_local_reports()
        self.lg("1. Clean up all existing bucket capacity reports")
        self.file_exists_bucket, self.init_count_bucket = self.s3_ops.browse_system_bucket_for_file(file_ext='All',
                                                                                                    clean=True)

        self.assertTrue(self.init_count_bucket == 0, 'System bucket not cleaned with reports')

        self.bucket, self.bucket_name = self.s3_ops.create_bucket(self.user_conn)
        self._buckets_to_clean = [self.bucket_name]

        self.lg('Enabling versioing on bucket %s' % self.bucket_name)
        self.bucket.configure_versioning(versioning=True)
        time.sleep(60)
        self.assertTrue(self.bucket.get_versioning_status()['Versioning'] == 'Enabled',
                        'Versioning not enabled for bucket %s' % self.bucket_name)
        responseid, status, reason, versionId = self.s3_ops.upload_single_object(self.user_conn, self.bucket_name,
                                                                                 key='obj-0', data='x' * 101)
        self.assertTrue(status == 200, reason)
        self.lg('Upload a multipart object onto source bucket in site1.')
        self.file_size1 = 1073741824
        self.chunk_size1 = 102428800
        self.multipart_file = 'obj-1'
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size1, self.chunk_size1)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.file_size2 = 1073741832
        self.chunk_size2 = 102428880
        status, self.part_count = self.s3_ops.upload_multipart_object(self.bucket, self.multipart_file,
                                                                      self.file_size2, self.chunk_size2)
        self.assertTrue(status, 'Multi-part upload failed')
        time.sleep(20)

        self.validate_backend_object(self.bucket_name, 1, errorType='', part_number=4)

        oop_key = self.keyrouter.modify_one_object_size_in_multi_version(bucket_name=self.bucket_name, part_number=4)

        self.lg('Multi part object OOP key before running flame job {}'.format(oop_key))

        time.sleep(5)

        self.lg('Trigger verifier job and wait for job to finish ')
        self.run_id = self.flame.run_flame(self.scalers[0], 'scalerdb_verify')
        finished = self.flame.wait_for_flame_job(self.scalers[0], self.run_id)
        self.clean_job = True if not finished else None
        info = self.flame.get_job_info(self.scalers[0], self.run_id)
        self.assertTrue(finished, "Flame job - %s is %s" % (self.run_id, info["status"]))
        self.assertTrue(self.flame.call_csv_upload(), 'CSV upload of reports failed.')
        self.cron_restore = True
        time.sleep(120)
        self.assertFalse(self.flame.get_local_report_status(VERIFIER_CRITICAL_CSV_FILE_NAME),
                         'Reports still present in local scalers')
        self.validate_csv(self.bucket_name, 1, errorType=VERIFIER_OBJECT_MP_UPLOADID_MISMATCH, validate_full_key=True, full_key=oop_key)