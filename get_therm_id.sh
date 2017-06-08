#!/usr/bin/env bash
#
# This script determines the thermometer id.
# The output can be redirected to a file.
# That file is used as input for the thermometer polling
# python script.
# The thermometer ids all start with 28 so we take the output 
# of the FIND command and parse out the name only.
# Example thermometer id:  28-000007080860
#
# This script is to be run once on bootup. The output should 
# be directed into the file /usr/local/bin/BioReactor/thermometer_id
sudo modprobe w1-gpio
sudo modprobe w1-therm

find /sys/bus/w1/devices/28* -exec basename {} \;
