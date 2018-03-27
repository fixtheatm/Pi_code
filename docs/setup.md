# Setup

* [Summary](#link_summary)
* Creating a bootable [Raspbian](#link_raspbian) SD card
* [Basic](#link_basic) Raspbian Configuration
* [Prerequisites](#link_prereq) installation
* [Station](#link_station) Configuration

## <a name="link_summary"></a>Summary

The current photobioreactor sensors use the [I²C](https://en.wikipedia.org/wiki/I%C2%B2C),  [SMBus](https://en.wikipedia.org/wiki/System_Management_Bus) and [1-wire](https://en.wikipedia.org/wiki/1-Wire) ports and protocols, as well as direct [GPIO](https://en.wikipedia.org/wiki/General-purpose_input/output) on a [Raspberry Pi](https://www.raspberrypi.org/).
The code that reads the sensors, and sends the measurements to the [web site](http://pbr.fixingtheatmosphere.org/) uses python3 with the SMBus library and [httpie](https://httpie.org/) client.  That all needs to be setup correctly before the code in this repository can be used.  There are many ways to get to a running system.  This document provides reference links, plus details for one of those paths.

## <a name="link_raspbian"></a>Creating a bootable Raspbian SD card

The photobioreactor reactor code was written for the [Raspbian](https://www.raspbian.org/) distro.  Several variants are available.  We used the image available from [The Raspberry Pi Foundation](https://www.raspberrypi.org/).  Download the [Raspbian Stretch](https://downloads.raspberrypi.org/raspbian_latest) zip image from the [raspbian](https://www.raspberrypi.org/downloads/raspbian/) page.  As of this writing, that gets the March 2018 (2018-03-13) version, as file 2018-03-13-raspbian-stretch.zip.

Download and install the appropriate [Etcher](https://etcher.io/) version for your computer.

Use Etcher to flash the Raspbian Stretch image to a micro SD card.

## <a name="link_basic"></a>Basic Raspbian Configuration

Photobioreactors are installed in semi-public locations, with live internet connections.  For security, the account password needs to be changed, so that it is [at least] not trivial for someone to take if over.  Also, the initial configuration is for the United Kingdom.  Updating the locale, timezone, and keyboard layout make working with it less frustrating.

Insert the flashed SD card in the Raspberry Pi, connect hdmi monitor, keyboard, mouse, and power.  A hardwired internet connection will simplify the initial setup.  If that is not possible, configuring wireless access will need to be done before installing new, or updating existing software.  The sensors do **not** need to be connected yet.

Open a terminal window.

```sh
sudo apt-get update
sudo apt-get upgrade
sudo raspi-config
```

There are 2 different cases for the configuration settings.  For a specific station, and as a base setup for creating a master image to be cloned to other stations.  The master image should stay very generic, setting up the things that should be common to all (or most) expected stations.  Setting up wi-fi for the master is probably not helpful.  A generic hostname is good, so only need to add the suffix for individual stations.  Most of the localization is likely to be common, so doing that for the master image means it should only need to be done one time.

* Change User Password
  * A normally running photobioreactor station has a permanent connection to the internet.  There is malware that [specifically targets Raspberry Pi systems](https://hackaday.com/2017/06/08/raspberry-pi-malware-mines-bitcoin/).  It is **IMPORTANT** that the default password is changed to something different.
* Update
  * The raspi-config script evolves over time.  Update it to make sure you have the latest capabilities.  Internet access is needed to do the update, so either a direct connection is needed, or wi-fi has to be set up first.
* Network Options
  * Hostname
    * Changing this is optional, **IF** only one Raspberry Pi will be connected to a network (LAN) at any one time.  If there can be multiple Raspberry Pi´s connected, each should have a unique name.  As an initial safety measure, change the hostname to something like `photobioreactor` or `solarbiocell`.  If multiple stations will be connected to a single LAN, each will need a unique name.  Add a class name or sequence number to the end of name for each bioreactor.
      * NOTE: Some IT groups may have additional rules about what the names should be.  Check with them if uncertain.
    * Wi-fi
      * If a physical ([RG45](https://en.wikipedia.org/wiki/Registered_jack)) cable is used to connect the rPi to the internet, No wi-fi setup is needed.  If a wireless connection is to be used, each bioreactor system will need to have the ssid and password configured.  There are various ways of setting the wi-fi configuration. There are various ways of learning what access points are available.  To many to give much for details here.  `sudo iwlist wlan0 scan` is one way to get information about the access points visible from the current rPi location.  That may provide way more information than you want to look at.  `sudo iwlist wlan0 scan | grep "SSID\|Quality"` will cut that down to just the SSID and signal quality information.
      * Some LANs are setup to need additional information to be able to connect.  To many variations to provide any reasonable information here.  Check with the local IT group.
* Localisation Options
  * Change Locale
    * The initial Raspbian locale is `en_GB.UTF-8 UTF-8`.  That will (mostly) work for English, but adding a more exact locale can improve some things.  The photobioreactor data collection will work fine without changing this.  I suggest using the `en_CA.UTF-8 UTF-8` or `fr_CA.UTF-8 UTF-8` in Canada.  `en_US.UTF-8 UTF-8` is a another reasonable choice for English in North America.
    * Pick the default locale for the system environment as well.   The first configuration page set the (possibly multiple) locales that are installed, and will be directly available.  The second page sets single locale that will be the default across the system.
    * The data collection code does not care what locales are used.
  * Change Timezone
    * This is set in 2 stages.  For Canada, select `America` (not `US`).  On the second page, select `Edmonton` for Alberta.
    * The data collection code does not care what timezone is set.  It always uses GMT when recording measurements.
  * Change Keyboard Layout
    * In regular use, a photobioreactor station is run [headless](https://en.wikipedia.org/wiki/Headless_computer).  Without a keyboard attached, the layout configuration is not important.  If a screen and keyboard are occasionally attached, have a reasonable configuration will make things less frustrating.  Since it might not always be the same keyboard being connected, I suggest keeping the model fairly generic.  I normally set the model to `Generic 104-key PC`, `English (US)` for country of origin, and `English (US)` on the layout screen.  Adjust that for the keyboards that will typically be available.
    * The keyboard configuration settings are much more personal choices.  They will only matter if special characters need to be entered directly from the rPi.
    * The data collection code does not care what keyboard layout is set up.  Having it correct (or close) can simplify other things.
  * Change Wi-fi Country
    * For general wireless safety, the country the rPi is to be used in should be set, if wi-fi is being used.
* Interfacing Options
  * SSH
    * SSH can be used to connect to photobioreactor stations from other systems.  Without needed to connect a screen and keyboard.  **Only** enable the SSH server if it is needed.  As long as a good password is being used, it is reasonably safe, but having the server running on the rPi does open another potential way for undesired access to the system.
      * A good password is on that can not be easily guessed, and is known by as few people as possible.

## <a name="link_prereq"></a>Prerequisites setup

This describes the steps for one way to get the code prerequisites configured and installed.  This has changed over time, as the basic downloaded Raspbian image and raspi_config script have evolved.

This configuration only needs to be done (or redone) when creating the master photobioreactor image.

Open a terminal window.

```sh
sudo raspi-config
```

* Interfacing Options
  * I2C
    * The current light sensor needs to have the ARM I2C interface enabled
  * 1-Wire
    * The current temperature sensor needs to have the one-wire interface enabled

```sh
sudo apt-get install httpie
git clone https://github.com/fixtheatm/Pi_code.git
sudo mv Pi_code /usr/local/bin/BioReactor
cd /usr/local/bin/BioReactor
./sensor_light.py
crontab -e
```

* sensor_light.py
  * Running this manually forces the creation of the photobioreactor.py import file.  That *would* be created automatically the first time a station is started up, but this way the file exists, and can be edited when cloning from the master image.  It is easier to edit the file, and change the station id, than to create the whole thing manually.
* crontab -e
  * pick the default editor to use.  `nano` is convenient
  * go to the end of the file (initial it only contains comments).  Import the crontab.txt file.  When using nano, that can be done with `page down` then `«ctrl» r` `/usr/local/bin/BioReacter/crontab.txt «enter»`
  * save the changes with `«ctrl» o «enter»`
  * exit with `«ctrl» x`

That should have a photobioreactor up and running.  If the sensors are attached, measurements will be recorded and sent to the web server at 5 minute intervals.  Although the station id is still set to `None`.  If making any adjustments on the master image, It is best to not have the sensors attached.  That way, no garbage measurements will be sent to the web site, for a photobioreactor station that does not really exist.

## <a name="link_station"></a>Station Configuration

Each station needs to have a unique ID for the information to be recorded and shown properly on the web site.  As a minimum, the file `/usr/local/bin/BioReactor/photobioreactor.ph` needs to be modified.  This can be done by booting the cloned image in an rPi, and modifying the file there.  It is likely easier to use an SD card reader to make the change.  After creating an image from the master, reinsert the SD card in the (Windows, Mac, or Linux) computer, and edit the file `/usr/local/bin/BioReactor/photobioreactor.ph` in the root partition.  Change `None` to the station id to use.  Currently that is a 5 digit number, but as a string.  Include single quote character around the station id.  EG. `'00001'`

The hostname and wi-fi configuration may need to be changed for the station as well.  See the [Basic Raspbian Configuration](#link_basic) information for the details.  The station can be started up without configuring the wi-fi.  Measurements will be taken, and stored locally, but will not be sent to the web site until an internet connection is available.
