#!/usr/bin/python3

"""
Handle a one wire temperature sensor (DS18B20)
"""

from datetime import datetime
from genericsensor import Sensor
import temperature


def chomp(str_data: str):
    '''Remove a single new line from the end of a string'''
    if str_data.endswith('\n'):
        return str_data[:-1]
    return str_data


class TemperatureSensor(Sensor):
    '''Collect temperature sensor value'''
    VALUE_NAME = 'temperature'
    JSON_PREFIX = 'bio_temp'
    SENSOR_PATH = '/sys/bus/w1/devices/{}/w1_slave'
    SLAVES_PATH = '/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves'
    IMPORT_SPEC = 'temperature.py'
    MEASUREMENT_FMT = '{:4.1f}'

    def get_value(self):
        data = []
        try:
            with open(self.SENSOR_PATH.format(temperature.address), 'r') as sensor_file:
                data = sensor_file.readlines()
        except FileNotFoundError as exc:
            sens_add = self.get_sensor_address()
            if sens_add:
                with open(self.SENSOR_PATH.format(sens_add), 'r') as sensor_file:
                    data = sensor_file.readlines()
            else:
                raise RuntimeError('Could not find temperature sensor to read')
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

    @staticmethod
    def get_sensor_address():
        '''get a DS18B20 one wire temperature sensor address'''
        temperature_sensor = None
        sensor_slaves = []
        all_slaves = []
        try:
            with open(TemperatureSensor.SLAVES_PATH, 'r') as slaves_fl:
                for line in slaves_fl:
                    all_slaves.append(chomp(line))
        except FileNotFoundError as exc:
            print(exc)
            print('Something is REALLY BAD: w1 slaves file not found')
            print('ABORT! ABORT!')
            raise
        for address in all_slaves:
            if address[0:2] == '28':
                sensor_slaves.append(address)
        if sensor_slaves:
            if len(sensor_slaves) == 1:
                temperature_sensor = sensor_slaves[0]
                TemperatureSensor.save_temperature_path(temperature_sensor)
            else:
                print('multiple temperature sensors found: should only be one attached')
        else:
            if all_slaves:
                print('No one wire slave devices detected')
            else:
                print('No temperature sensor devices detected')
        return temperature_sensor

    @staticmethod
    def save_temperature_path(address: str):
        '''Save the address of the detected sensor, so do not need to repeat the lookup every time'''
        with open(TemperatureSensor.IMPORT_SPEC, 'w') as import_fl:
            import_fl.write("address = '{}'\n".format(address))

    def _monitor_value(self, callback):
        raise NotImplementedError(
            'Temperature sensor does not support monitoring.')


def main():
    '''Code to run when module is executed standalone'''
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
