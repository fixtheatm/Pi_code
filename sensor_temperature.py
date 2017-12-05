#!/usr/bin/python3

"""
Handle a one wire temperature sensor (DS18B20)
"""

from datetime import datetime
from genericsensor import Sensor
import temperature


class TemperatureSensor(Sensor):
    """Collect temperature sensor value"""
    VALUE_NAME = 'temperature'
    JSON_PREFIX = 'bio_temp'
    MEASUREMENT_FMT = '{:4.1f}'

    def get_value(self):
        with open(temperature.device, 'r') as owfile:
            data = owfile.readlines()
            deg_c = ''
            if data[0].strip()[-3:] == 'YES':
                temp = data[1][data[1].find('t=') + 2:]
                try:
                    ftemp = float(temp)
                    if ftemp == 0:
                        deg_c = 0
                    else:
                        deg_c = ftemp / 1000
                except ValueError:
                    print("Error with t=", temp)
            return deg_c

    def _monitor_value(self, callback):
        raise NotImplementedError(
            "Temperature sensor does not support monitoring.")


def main():
    """Code to run when module is executed standalone"""
    sensor = TemperatureSensor()
    value = sensor.get_value()
    print(value)
    sensor.generate_file(
        TemperatureSensor.VALUE_NAME,
        TemperatureSensor.MEASUREMENT_FMT.format(value),
        TemperatureSensor.JSON_PREFIX,
        datetime.utcnow())


if __name__ == '__main__':
    main()
