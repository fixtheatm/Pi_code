#!/usr/bin/python3
from genericsensor import Sensor
import RPi.GPIO as GPIO
import time
from datetime import datetime


class GasSensor(Sensor):
    """Collect oxygen cycle values and output them to json files for transfer to server."""
    pulse_volume = 7.5 # millilitres

    def __init__(self):
        super().__init__()
        self.gpiopin = 16
        GPIO.setmode(GPIO.BCM)  # With BCM mode, the pin matches the label on the board. 16 above is GPIO16.
        GPIO.setup(self.gpiopin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # We want to monitor the pin as input to detect the water cycling through.

    def get_value(self):
        raise NotImplementedError("Gas sensor can not return instant values, must monitor for activity.")

    def _monitor_value(self, callback):
        GPIO.add_event_detect(self.gpiopin, GPIO.FALLING, callback=callback, bouncetime=10000)
        while self.continue_monitor:
            time.sleep(5)  # The max potential delay before the monitor shuts down after stop_monitor is called.
        GPIO.remove_event_detect(self.gpiopin)

    def gas_callback(self, channel):
        print("Callback on channel: ", channel)
        # We detected a gas cycle! Push it out to a new file.
        # Every pulse always indicates the same volume of oxygen passing through the sensor.
        print("Value: ", self.pulse_volume)
        sensor.generate_file('flow', "{:4.1f}".format(self.pulse_volume), 'bio_gas', datetime.utcnow())

if __name__ == '__main__':
    sensor = GasSensor()
    sensor.start_monitor(sensor.gas_callback)
    sensor.wait_monitor()
