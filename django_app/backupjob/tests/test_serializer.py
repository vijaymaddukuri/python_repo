import unittest
from backupjob.serializer import BackupSerializer
class TestBackupSerializer(unittest.TestCase):
    def test_backupserializer(self):
        val_dict = {
            "RetentionDays": 72,
            "Callback": "example.com",
            "VirtualMachineID": "8E87A82F-D40C-4200-A62E-A8E12291B0BD",
            "TenantID": "8E87A82F-D40C-4200-A62E-A8E12291B0BD",
            "VirtualMachineHostName": "SHWETAGARG071018B"}
        serializer = BackupSerializer(data=val_dict)
        self.assertEqual(serializer.is_valid(), True)
