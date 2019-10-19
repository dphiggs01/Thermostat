# Smart Home Thermostat

The Smart Home Thermostat is a simplified version of the Nest Thermostat. That uses AWS infrastructure to create a cloud enabled IoT Thermostat device.

An EC2 Instance runs a Python Flask based web site for administration of the Thermostat. Currently we have only one
[Raspberry Pi](https://www.amazon.com/seeed-studio-Raspberry-Computer-Model/dp/B07WBZM4K9/ref=sr_1_18?crid=3EBM5DV9C9TD5&keywords=raspberry+pi&qid=1571501784&sprefix=raspb%2Caps%2C153&sr=8-18)
connected but the site is configured to manage multiple devices.

The Website communicates to the Pi through a restful services API using Lambada Functions also written in Python. These simple functions use an MQTT client to interface with an AWS IoT Thing that securely connects to the Pi.

The Pi in turn connects to a [TI SensorTag](http://www.ti.com/design-resources/embedded-development/hardware-kits-boards.html)
 for Room Temperature data using BLE (This sensor is currently the weak link in the system as the Battery life of the device is poor.) The Pi uses a simple relay to actuate the furnace on and off.

The furnace runtime stats (i.e when the furnace was on or off) are being sent back to a Dynamo DB instance for further optimization of the schedule.
Note: This component is currently not available in the provided source.
(I'll check this in as a seperate project.)

A final component provides the current weather data and displays this on the Website.


## Architecture

Here a high level view of the architecture.

<img src="./thermo_docs/Architecture.png"  height="250" width="450"/>


## UI Design

The thermostat has a simple user interface allowing you to easily set
or check any of the zones current temperatures.

Each Zone has a four (4) season schedules that allows for setting
specific temperature set-points on any day of the week and at any time of the day.
Additionally these schedules can be adjusted by season (Summer, Fall,
Winter, Spring).

A fifth (5) Away Schedule is also provided that allows you to easily
set the whole house (all zones) to a schedule best suited for when the
home is unoccupied.

<img src="./thermo_docs/pisite.png"  height="540" width="500"/>


<img src="./thermo_docs/schedule.png"  height="460" width="500"/>

__Note__: The schedule is currently manually defined in a JSON file.
The above interface is provided in the code and will enable configuration
from the website. (This feature is not currently fully coded.)
