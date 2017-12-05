#!/usr/bin/python3
from genericsensor import Sensor
from datetime import datetime


class TemperatureSensor(Sensor):
    """Collects temperature sensor values and outputs them to a json file for transfer to server."""
    def __init__(self):
        super().__init__()
        self.device = '/sys/bus/w1/devices/28-0000075d2009/w1_slave'

    def get_value(self):
        with open(self.device, 'r') as f:
            data = f.readlines()
            deg_c = ''
            if data[0].strip()[-3:] == 'YES':
                temp = data[1][data[1].find('t=') + 2:]
                try:
                    if float(temp) == 0:
                        deg_c = 0
                    else:
                        deg_c = (float(temp) / 1000)
                except:
                    print("Error with t=", temp)
                    pass
            return deg_c

    def _monitor_value(self, callback):
        raise NotImplementedError("Temperature sensor does not support monitoring.")

if __name__ == '__main__':
    sensor = TemperatureSensor()
    value = sensor.get_value()
    print(value)
    sensor.generate_file( 'temperature', "{:4.1f}".format( value ), 'bio_temp', datetime.utcnow())
