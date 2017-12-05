#!/usr/bin/python3
# -------------------------------------------------------------
# Based off of bh1750.py from http://www.raspberrypi-spy.co.uk/
# -------------------------------------------------------------
from genericsensor import Sensor
import smbus
from datetime import datetime


class LightSensor(Sensor):
    """Collect light intensity sensor value and output it to a json file for transfer to server."""
    DEVICE = 0x23  # Default device I2C address
    # Start measurement at 0.5lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_2 = 0x21
    RPI_SMBUS = 1 # Rev 1 Pi uses 0, Rev 2 Pi uses 1

    def __init__(self):
        super().__init__()
        self.bus = smbus.SMBus( LightSensor.RPI_SMBUS )

    def get_value(self):
        data = self.bus.read_i2c_block_data(LightSensor.DEVICE, LightSensor.ONE_TIME_HIGH_RES_MODE_2)
        return ((data[0] << 8) | data[1]) / 1.2

    def _monitor_value(self, callback):
        raise NotImplementedError("Light sensor does not support monitoring.")

if __name__ == '__main__':
    sensor = LightSensor()
    value = sensor.get_value()
    print(value)
    sensor.generate_file( 'lux', "{:7.1f}".format( value ), 'bio_light', datetime.utcnow())

