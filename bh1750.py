#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____          
#   / _ \/ _ \(_) __/__  __ __ 
#  / , _/ ___/ /\ \/ _ \/ // / 
# /_/|_/_/  /_/___/ .__/\_, /  
#                /_/   /___/   
#
#           bh1750.py
#  Read data from a digital light sensor.
#
# Author : Matt Hawkins
# Date   : 15/04/2015
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------
import smbus
import time

bioreactor_folder='/usr/local/bin/BioReactor/'
json_date= time.strftime('%Y%m%d_%H%M%S')

json_file=bioreactor_folder + 'bio_light_' + json_date + '.json'

# get the device_id from the file 'device_id'. This id is hard coded for 
# each customer's raspberry as a different id!!

device_id_filename=bioreactor_folder + 'device_id'

idfile= open(device_id_filename, 'r')
device_id= idfile.readline()
idfile.close()

device_id=device_id.strip('\n')

#print(device_id)

recorded_on = time.strftime('%Y-%m-%d %H:%M:%S')


# Define some constants from the datasheet

DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number
  return ((data[1] + (256 * data[0])) / 1.2)

def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_2)
  return convertToNumber(data)

def main():

  slux = "%7.1f" % (readLight())

  with open(json_file, 'w') as f:
    s='[{"deviceid":"' + device_id + '","lux":"' + slux.strip() + '","recorded_on":' + \
            '"' + recorded_on + '"}]'
    f.write(s)
    f.close()
    
  
if __name__=="__main__":
   main()
