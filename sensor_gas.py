#!/usr/bin/python3

"""
Handle direct sensing of gas flow state changes
"""

import time
from datetime import datetime
from enum import Enum

import RPi.GPIO as GPIO
# pylint: disable=no-member
# pylint can not see the RPi.GPIO members.  Shutting that error off

from genericsensor import Sensor


class FlowState(Enum):
    """Names for possible states of the gas flow sensor"""
    FIRED = 0   # change to this state when a bubble passes through
    PRIMED = 1  # change to this state when bubble almost ready
# end class FlowSate


class GasSensor(Sensor):
    """
    Collect gas flow values and output them to json files.
    """

    SOURCE = 23  # gpio23
    DRAIN = 24   # gpio24
    SENSE_PINS = (SOURCE, DRAIN)
    SENSOR_UNCOVERED = 0  # using pull down, so open is low
    SENSOR_COVERED = 1    # completing the circuit pulls pin high

    SLEEP_TIME = 5      # seconds
    PULSE_VOLUME = 7.5  # millilitres of air in a bubble

    def __init__(self):
        """Gas Flow Sensor constructor"""
        super().__init__()
        GPIO.setmode(GPIO.BCM)  # Pin number matches board label. 16 is GPIO16.
        GPIO.setup(self.SENSE_PINS, GPIO.IN)
        # Input pins without internal pull up/down resistor: use external

        self.channelstate = {}
        for channel in self.SENSE_PINS:
            self.channelstate[channel] = GPIO.input(channel)
        self.flowstate = FlowState.FIRED
        if (self.channelstate[self.SOURCE] == self.SENSOR_UNCOVERED and
                self.channelstate[self.DRAIN] == self.SENSOR_COVERED):
            self.flowstate = FlowState.PRIMED
    # end def __init__()

    def get_value(self):
        """return the current (instantanious) flow"""
        raise NotImplementedError("Gas flow sensor can not return instant \
            values, must monitor for activity.")

    def _monitor_value(self, callback):
        """Monitor gas flow"""
        # Setup callbacks to handle transitions on the gas flow sensor pins
        for chn in self.SENSE_PINS:
            GPIO.add_event_detect(chn, GPIO.BOTH, callback=callback)

        while self.continue_monitor:
            # Do regular checks to make sure that the detected transitions
            # match the physical reality state
            self.resync()

            # The max potential delay before the monitor shuts down after
            # stop_monitor is called... ALSO the maximum delay before
            # resyncronization of the recorded sensor states with the current
            # reality.
            time.sleep(self.SLEEP_TIME)

        # monitoring is shutting down
        for chn in self.SENSE_PINS:
            GPIO.remove_event_detect(chn)
        print('monitoring shut down')  # TRACE

    def gas_callback(self, channel):
        """
        callback function for edge detection on the flow sensors
        """
        edgeresult = GPIO.input(channel)  # Current reality for this channel
        self.channelstate[channel] = edgeresult
        self.track_flow()
    # end def gas_callback()

    def resync(self):
        """
        Update recorded sensor states, if the transitions go out of sync with
        reality
        """
        didresync = False
        for chnl in self.SENSE_PINS:
            realstate = GPIO.input(chnl)
            if realstate != self.channelstate[chnl]:
                self.channelstate[chnl] = realstate
                didresync = True
        if didresync:
            print('resyncing ... ', end='')  # DEBUG
            self.track_flow()
            print('resync done')  # DEBUG
    # end def resync()

    def track_flow(self):
        """
        Track and report the state of the gas flow sensor
        """
        if (self.channelstate[self.SOURCE] == self.SENSOR_UNCOVERED
                and self.channelstate[self.DRAIN] == self.SENSOR_COVERED):
            if self.flowstate != FlowState.PRIMED:  # DEBUG
                # only report once per cycle
                print('flow primed')  # DEBUG
            self.flowstate = FlowState.PRIMED
        if (self.flowstate == FlowState.PRIMED
                and self.channelstate[self.SOURCE] == self.SENSOR_COVERED
                and self.channelstate[self.DRAIN] == self.SENSOR_UNCOVERED):
            self.flowstate = FlowState.FIRED
            self.generate_file(
                'flow',
                "{:4.1f}".format(self.PULSE_VOLUME),
                'bio_gas',
                datetime.utcnow())
# end class GasSensor


if __name__ == '__main__':
    print('GPIO version {}'.format(GPIO.VERSION))  # DEBUG
    SENSOR = GasSensor()
    SENSOR.start_monitor(SENSOR.gas_callback)
    SENSOR.wait_monitor()

    GPIO.cleanup()
