# Raspberry Pi code for a PhotoBioReactor station

This is part of the [Fixing the Atmosphere](http://www.fixingtheatmosphere.com/) project and education materials.  It contains the code to read sensors connected to a Raspberry Pi, and send the information to the web site for viewing.

## Programs, Scripts, Tools

<dl>
<dt>genericsensor.py</dt>
<dd>Base classs inherited by all concrete sensors.</dd>

<dt>sensor_gas.py</dt>
<dd>Monitor and report discrete gas (oxygen) flow steps.</dd>

<dt>sensor_light.py</dt>
<dd>Report instantaneous light intensity measurments.</dd>

<dt>sensor_temperature.py</dt>
<dd>Report instantaneous temperature measurments.</dd>

<dt>temperature.py</dt>
<dd>import file that specifies the 1-wire device id for the temperature sensor.</dd>

<dt>photobioreactor.py</dt>
<dd>import file that specifies the id for the local PhotoBioReactor station.</dd>

<dt>send_json_to_server.sh</dt>
<dd>Script to be run regularly to transfer collected reading to the website database.</dd>

<dt>get_therm_id.sh</dt>
<dd>The original shell script to determine the address of an attached 1-wire device.</dd>

<dt>make3jsonposts.sh</dt>
<dd>A test script to generate fake data for all of the sensor.  This can be used when testing sending of data to the website.</dd>

<dt>makejsondata.sh</dt>
<dd>A test script to generate fake data for a single specified sensor.</dd>

<dt>master_datavalue.json</dt>
<dd>A template used to generate fake data in the (website) expected json format.</dd>

## Reference information sources

* [BH1750FVI](https://www.raspberrypi-spy.co.uk/2015/03/bh1750fvi-i2c-digital-light-intensity-sensor/) I2C Digital Light Intensity Sensor
* [ADS1115](https://www.adafruit.com/product/1085) I2C ADC
* [DS18B20](https://www.adafruit.com/product/381) 1 Wire temperature sensor
