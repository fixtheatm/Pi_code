# Protoboard

* [Parts](#link_parts) used
* [Layout](#link_layout)
* [Protoboard Assembly](#link_assembly)
* [Sensor Wiring](#link_wiring)
* [Reference](#link_reference) information
</br></br>

## <a name="link_parts"></a>Parts

* [breadboard layout protoboard](http://www.gikfun.com/electronic-pcb-board-c-60/3x-solderable-breadboard-gold-plated-finish-proto-board-pcb-p-725.html)
* [Pi Cobbler](https://www.adafruit.com/product/2029)
* [Waterproof DS18B20 Digital temperature sensor](https://www.adafruit.com/product/381)
* I2C Light Sensor
* 1 x 3-position wire connector (37-6203)
* 1 x 4-position wire connector (37-6204)
* 2 x 5-position wire connector (one right angle)  (37-6205 and 37-6305)
  * [Mode Electronics](http://mode-elec.com/), enter "37-62" or "37-63" in the part search box to see the part numbers in the drop down list
* 2 x 470K resistor
* 1 x 4.7K resistor
* 2 x 3V zener diode (not installed; possible future)

## <a name="link_layout"></a>Protoboard Layout

This version of the photobioreactor station is using a protoboard with a Pi Cobbler to connect to a Raspberry Pi.  The protoboard has headers to connect to the sensors.  This is a fairly direct translation from the original breadboard.  A future version will likely use a [Perma-Proto HAT](https://www.adafruit.com/product/2310) or similar, instead of the protoboard and cobbler.

The following uses the hole labelling on the Gikfun protoboard.  The [layout](breadboard_layout.pdf) can be viewed as a pdf.  Currently, that layout is for a breadboard, but that is very close to what the protoboard uses.  With a few discrepancies.  The [Fritzing](http://fritzing.org/) tool that I am using does not currently have components that match the 3 and 5 pin headers.  The diagram uses 4 and 6 pin headers instead.  Ignore the unused pins.  Another pdf has view of the [schematic](protoboard_schematic.pdf) for the protoboard and attached sensors.  Again, JP2, JP3, JP4, JP5 show a pin that does not really exist.  In the diagrams, the gas flow sensor is shown as a pair of push button switches.  There is nothing in the available components even close visually, and the switches are the correct functionally.  Each flow sensor is either open or closed.

* Cobbler and male headers
  * Cobbler : 3v3 (pin 1) to d11; gpio 21 (pin 21) to h30
  * «JP3» 5 position wire connector (pin 1) to c3; pin 5 to c7 : vertical flat side of male header toward row "b"
  * «JP2» 3 position wire connector (gas flow sensor) (pin 1) to f1; pin 3 to f3 : vertical flat side of male header toward row "e"
  * «JP1» 4 position wire connector (temperature sensor) (pin 1) to j6; pin 4 to j9 : vertical flat side of male header toward row "i"

* Components
  * 470k resistor i2 to «-»2 (leave room for zener diode to connect to j2)
  * 470k resistor i4 to «-»4
  * 4.7k resistor a14 to «+»14(leave room for zener diode to connect to j4)
  * zener diode not installed from j2 to «-»1
  * zener diode not installed from j4 to «-»3

* ground connections
  * a15 to «-»15 ¦ a15 ==> d15 (cobbler GND)
  * a7 to «-»7 ¦ a7 ==> c7, which is the end (ground) pin for the 5 pin header
  * j20 to «-»19 ¦ j20 ==> h20 (cobbler GND)
  * g7 to g8 (do not bother keeping insulation)
  * e7 to f7

* power (3V3) connections
  * a19 to «+»19 ¦ a19 ==> d19 (cobbler 3V3)
  * a3 to «+»3 ¦ a3 ==> c3, which is pin 1 of the 5 pin header
  * e3 to f5 (curve to avoid where JP2 will be placed)
  * g5 to h2 (curve to avoid JP2; leave room for data wire in h3)

* data connections
  * c14 to f6 ¦ c14 ==> d14 (cobbler gpio 4) (curve to avoid cobbler and JP3)
  * b4 to b13 ¦ b13 ==> d13 (cobbler SCL)
  * a4 to a12 ¦ a12 ==> d12 (cobbler SDA)
  * h1 to j19 ¦ j19 ==> h19 (cobbler gpio 24) (leave room for power wire in h2) (curve to avoid cobbler and JP1)
  * h3 to i18 ¦ j18 ==> h18 (cobbler gpio 23) (leave room for power wire in h2) (curve to avoid cobbler and JP1)

## <a name="link_assembly"></a>Protoboard Assembly

The [Layout](#link_layout) section describes where the pieces actually go.  This provides tips on the order to insert and solder the parts.  Soldering the Pi cobbler and headers first would make it easier to see where the wires belong.  However, that makes getting the wires into position, and soldering them in place more difficult.  Instead, I recommend doing all of the wires first, then the resistor, Pi cobbler, and finally the headers.

At any stage of the wiring, the cobbler and/or headers can be inserted temporarily, to verify that the wires are going to the right pins.

Wires are cut to fit.  Leave the stripped ends a little long.  They can be trimmed after the soldering is all done.  Leave (especially) the longer wires a little long.  That leaves a little slack, so that they can be bent around where the cobbler and headers are mounted.

Wire colours are arbitrary and by convention.  Ground (-) and Power (+) are by convention black and red.  There is no fixed convention for data wires.  Using multiple colours makes visual inspection easier.  The colours used here are what was on hand.  The diagrams were created with the same colours.

Step by step:

* Solder all (5) of the ground (black) wires first.  Do not bother to try to keep the insulation on the jumper from g7 to g8.
* Solder all (4) of the power (red) wires.  In the current version of the protoboard, these all connect back to a 3.3 volt pin on the cobbler.
  * This is a good time to temporarily insert the cobbler and headers into the protoboard.  Verify that each of the power and ground wires is connecting to the expected pins.
* blue wire (SDA) from a4 to a12
* green wire (SCL) from a4 to a13
  * This can use a5 instead of a4 (cleaner some ways), but the spacing is very tight with JP3 (the 5 pin header).  Want to make sure that the header can be inserted all of the way, sitting flat against the protoboard.
* white wire (GPIO4) from f6 to c14
  * leave slack to bend it to avoid the cobbler pins and JP3.  I also bent it around the ground wire at f7 to e7.  I like the wire to lay flat on the protoboard where possible, instead of crossing over each other.
* green wire (GPIO23) from h3 to i18
* yellow wire (GPIO24) from h1 to i19
* 4.7K resistor from a14 to power bus (+)
* 470K resistor from i1 to ground (-)
* 470K resistor from i1 to ground (-)
  * use the 2nd and 4th holes on the (-) line, to leave room in case protection diodes needs to be added later.  That is also why "i" holes are used instead of "j".
  * If you want to add insulation to the resistor leads, do it only on the end towards "i".  Bend the other lead close to the body, so no insulation is needed for the end going to ground.
* insert the Pi Cobbler.  Initially, only solder 2 pins, one on each end, in opposite corners.
* insert each of the headers.  Make sure the orientation is correct. All of the flat sides should point the same way, towards the "a" row line of holes on the protoboard.
* Do a last round of verifying that everything is in the right place, and connects the right pieces together.  Make sure that the cobbler and header are sitting flat on the protoboard.  If not, reheat a corner pin, and push them down.  Solder all of the cobbler and header pins.

## <a name="link_wiring"></a>Sensor Wiring

* Install a 5 pin right angle header on the **back** of the light sensor breakout board.  This will position it out of the way of the light, and the mounting holes are on the other end.
* The 5 wire cable for the light sensor is 'straight through'.  Just make sure that cable is the right way up, so that that ground and power do not get reversed when connecting from the header on the protoboard, to the right angle header on the sensor breakout board.
* Many of the temperature sensors only have 3 wires.  Some have a fourth wire for the shield on the cable.  If it exists, the shield connects to the extra pin on the 4 pin header.

## <a name="link_reference"></a>Reference Information

* [BH1750FVI](https://www.raspberrypi-spy.co.uk/2015/03/bh1750fvi-i2c-digital-light-intensity-sensor/) I2C Digital Light Intensity Sensor
* [DS18B20](https://www.adafruit.com/product/381) 1 Wire temperature sensor
* [https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing)
