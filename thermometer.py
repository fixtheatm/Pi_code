# This python script reads the temperature from the sensor
# formats the result and outputs a json text file into the
# data folder
#
#
import os
import glob
import datetime
import time

# to determine the id for a thermometer, do the following at a terminal window
#   sudo modprobe w1-gpio
#   sudo modprobe w1-therm
#
#   ls /sys/bus/w1/devices
#                  chip            probe version
# our therm_ids are 28-000007080860 28-0000075d2009 28-041590822aff

bioreactor_folder='/usr/local/bin/BioReactor/'

# get the device_id from the file 'device_id'. This id is hard coded for 
# each customer's raspberry as a different id!!

device_id_filename=bioreactor_folder + 'device_id'

idfile= open(device_id_filename, 'r')
device_id= idfile.readline()
idfile.close()

device_id=device_id.strip('\n')

#print(device_id)

# We have a startup script named get_therm_id.sh which runs at reboot
# It determines the thermometer id and places that in the file 'thermometer_id
# We will just read it. Note we strip the string to avoid the newline character!

id_filename=bioreactor_folder + 'thermometer_id'

idfile= open(id_filename, 'r')
therm_id= idfile.readline()
idfile.close()

device_path='/sys/bus/w1/devices/' + therm_id.strip('\n') + '/w1_slave'

#print(device_path)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

json_date= time.strftime('%Y%m%d_%H%M%S')

json_file=bioreactor_folder + 'bio_temp_' + json_date + '.json'


recorded_on = time.strftime('%Y-%m-%d %H:%M:%S')

lst=[]
lst.append(device_path)

def get_temp(device):
    f = open(device, 'r')
    data=f.readlines()
    f.close()
    deg_c=''
    if data[0].strip()[-3:] == 'YES':
        temp=data[1][data[1].find('t=')+2:]
        try:
            if float(temp)==0:
                deg_c=0
            else:
                deg_c = (float(temp)/1000)
        except:
            print ("Error with t=",temp)
            pass
    
    return deg_c;

for device in lst:
    device_name = device.split('/')[5]
    stemp = "%4.1f" % (get_temp(device))

    with open(json_file, 'w') as f:
        s='[{"device_id":"' + device_id + '","temperature":"' + stemp + '","recorded_on":' + \
            '"' + recorded_on + '"}]'
        f.write(s)
        f.close()
    #print (s)
    
