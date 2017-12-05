#!/usr/bin/python
from genericsensor import Sensor
from datetime import datetime
from Adafruit_ADS1x15 import ADS1x15

ADS1115 = 0x01

class PHSensor(Sensor):
    """Collect pH sensor value and output it to a json file for transfer to server."""
    def __init__(self):
        super(PHSensor, self).__init__()
        self.ADS1115 = 0x01
        self.adc = ADS1x15(ic=self.ADS1115)

    def get_value(self):
        # Get voltage in the range of 414.12 (ph 0) to -414.12 (pH 14)
        voltage = self.get_voltage()

        # Convert voltage to pH. Each drop in 59.16mV from 414.12mV is an increase of pH by one.
        # Range should be -414.12 to +414.12 for pH 0-14,
        #return (414.12 - voltage) / 59.16
        # Appears to actually function as 0-4v for pH 0-14
        return ((voltage / 4096) * 14.0) + 0.34

    def get_voltage(self):
        # Read voltage from ADS1115
        return self.adc.readADCSingleEnded(0)

    def _monitor_value(self, callback):
        raise NotImplementedError("pH sensor does not support monitoring.")

if __name__ == '__main__':
    sensor = PHSensor()
    value = sensor.get_value()
    print("pH Value")
    print(value)
    sensor.generate_file( 'ph', "{:4.1f}".format( value ), 'bio_ph', datetime.utcnow())
