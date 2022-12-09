# -*- coding: utf-8 -*-

from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()


class InteriorTemperature:
    def __init__(self):
        self.temperature = 0

    def get_temperature_int(self):
        self.temperature = sensor.get_temperature()


interior_temperature = InteriorTemperature()
