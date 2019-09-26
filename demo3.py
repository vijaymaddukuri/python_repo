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
VERIFIER_CRITICAL_CSV_FILE_NAME = "object_verifier_report_critical_pending.csv"
VERIFIER_CRITICAL_CSV_GZ_FILE_NAME = "object_verifier_report_critical_pending.csv.gz"
VERIFIER_OK_CSV_FILE_NAME = "object_verifier_report_ok.csv"
VERIFIER_OK_CSV_GZ_FILE_NAME = "object_verifier_report_ok.csv.gz"
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
        self.s3_ops.browse_system_bucket_for_file(file_ext=VERIFIER_OK_CSV_GZ_FILE_NAME, clean=False)
        print "th_file_exists_bucket" , th_file_exists_bucket
        print "th_count_bucket", th_count_bucket
        self.assertTrue(th_count_bucket == self.init_count_bucket + 1,
                            'New report not uploaded to system bucket after verifier job')

    def validate_backend_object(self, bucket_name, object_index, versionId='null', errorType='', part_number=0, kill_marker=False):
        self.lg("validating bucket_name: %s object:obj-%s versionId:%s"%(bucket_name, object_index, versionId))

        if part_number != 0:
            entries_dict = self.keyrouter.iterate_versioning_multipart_backend_bucket_objects(bucket_name, 'O', 'before flame job', object_index, part_number)
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
            self.validate_csv(bucket_name=bucket_name, object_index=object_index, errorType=errorType, part_number=part_number)

    def validate_csv(self, bucket_name, object_index, errorType='', part_number=0, validate_full_key=False,
                     full_key=None):
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
                    if metering_stats['Full Key'] == full_key:
                        full_key_validation = True
                    else:
                        full_key_validation = False
                    self.assertTrue(full_key_validation, "Multiple version mismatch of OOP key")

        self.assertTrue(object_found, "Object  not found in csv")


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


