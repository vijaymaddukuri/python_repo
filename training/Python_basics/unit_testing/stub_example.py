# Race Car Example
# Alert driver when tire pressure increases

class Alarm(object):

    def __init__(self, sensor=None):
        self._low_pressure_threshold = 17
        self._high_pressure_threshold = 21
        self._sensor = sensor or Sensor()
        self._is_alaram_on = False

    def check(self):
        psi_pressure_value = self._sensor.sample_pressure()
        if psi_pressure_value < self._low_pressure_threshold \
            or self._high_pressure_threshold < psi_pressure_value:
            self._is_alaram_on = True

    @property
    def is_alarm_on(self):
        return self._is_alaram_on

import random

class Sensor(object):
    _OFFSET = 16
    def sample_pressure(self):
        pressure_value = self.sample_pressure()
        return Sensor._OFFSET + pressure_value

    @staticmethod
    def sample_actual_pressure():
        pressure_value = 6 *  random.random() * random.random()
        return pressure_value

