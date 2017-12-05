# Raspberry Pi code for a PhotoBioReactor station

This is part of the [Fixing the Atmosphere](http://www.fixingtheatmosphere.com/) project and education materials.  It contains the code to read sensors connected to a Raspberry Pi, and send the information to the web site for viewing.

## Programs, Scripts, Tools

send_json_to_server.sh
: Script to be run regularly to transfer collected reading to the website database

thermometer.py
: Program to read the current temperature sensor, and save the information in a json file

bh1750.py
: sample program to read the I2C digital light sensor

get_therm_id.sh
: The original shell script to determine the address of an attached 1-wire device.

make3jsonposts.sh
: A test script to generate fake data for all of the sensor.  This can be used when testing sending of data to the website.

makejsondata.sh
: A test script to generate fake data for a single specified sensor.

master_datavalue.json
: A template used to generate fake data in the (website) expected json format.
