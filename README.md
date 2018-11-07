# Smart Home Thermostat

## Architecture
![Architecture](./thermo_docs/Architecture.png)

The Smart Home Thermostat is a simplified version of the Nest Thermostat. That uses AWS infrastructure to create a cloud enable IoT device.

An EC2 Instance runs a Python Flask based web site for administration of the Thermostat. Currently we have only one Pi connected but the site is configured to manage multiple devices.

The Website communicates to the Pi though a restful services API using Lambada Functions also written in Python. These simple functions use an MQTT client to interface with AWS IoT Thing that securely connects to the Pi

The Pi in turn connects to a Texas Instruments Sensor using BLE (This sensor is currently the weak link in the system as the Battery life if the device is poor) The Pi uses a simple relay to actuate the furnace on and off.

Furnace run time stats where being sent back to a Dynamo DB instance for further optimization of the schedule. This components is currently not available.

A final component provides current weather data and displays this on the Website

![Website](./thermo_docs/pisite.png)
