import unittest
from unittest.mock import *

from training.Python_basics.unit_testing.stub_example import Alarm


class AlarmTest(unittest.TestCase):
    def test_check_with_high_pressure(self):
        with patch('unit_testing.stub_example.Sensor') as test_sesnor_class:
            test_sensor_instance = Mock()
            test_sensor_instance.sample_pressure.return_value = 22
            test_sesnor_class.return_value = test_sensor_instance
            alarm = Alarm()
            alarm.check()
            self.assertTrue(alarm.is_alarm_on)
    @patch('unit_testing.stub_example.Sensor')
    def test_check_with_low_pressure(self, test_sesnor_class):
        test_sensor_instance = Mock()
        test_sensor_instance.sample_pressure.return_value = 15
        test_sesnor_class.return_value = test_sensor_instance
        alarm = Alarm()
        alarm.check()
        self.assertTrue(alarm.is_alarm_on)

