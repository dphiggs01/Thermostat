import datetime
import time

from bluepy.btle import BTLEException
from bluepy.sensortag import SensorTag
import logging

logger = logging.getLogger()

SENSORTAG_ADDRESS = "54:6C:0E:80:94:06"
FREQUENCY_SECONDS = 5.0

# http://www.ti.com/tool/cc2650stk
# Older version http://www.ti.com/tool/CC2541DK-SENSOR

class TempSensor(object):
    def __init__(self):
        self._tag = SensorTag(SENSORTAG_ADDRESS)

    def enable_sensors(self):
        """Enable sensors so that readings can be made."""
        self._tag.IRtemperature.enable()
        # self._tag.accelerometer.enable()
        self._tag.humidity.enable()
        # tag.magnetometer.enable()
        self._tag.barometer.enable()
        # tag.gyroscope.enable()
        self._tag.keypress.enable()
        # tag.lightmeter.enable()
        self._tag.battery.enable()

        # Some sensors (e.g., temperature, accelerometer) need some time for initialization.
        # Not waiting here after enabling a sensor, the first read value might be empty or incorrect.
        time.sleep(1.0)

    def disable_sensors(self):
        """Disable sensors to improve battery life."""
        self._tag.IRtemperature.disable()
        #self._tag.accelerometer.disable()
        self._tag.humidity.disable()
        #self._tag.magnetometer.disable()
        self._tag.barometer.disable()
        #self._tag.gyroscope.disable()
        self._tag.keypress.disable()
        #self._tag.lightmeter.disable()
        self._tag.battery.disable()

    def raw_readings(self):
        """Get sensor readings and collate them in a dictionary."""
        try:
            self.enable_sensors()
            readings = {"ir_temp": self._tag.IRtemperature.read()[0], "ir": self._tag.IRtemperature.read()[1],
                        "humidity_temp": self._tag.humidity.read()[0], "humidity": self._tag.humidity.read()[1],
                        "baro_temp": self._tag.barometer.read()[0], "pressure": self._tag.barometer.read()[1],
                        "battery": self._tag.battery.read()}
            self.disable_sensors()

            # round to 2 decimal places for all readings
            readings = {key: round(value, 2) for key, value in readings.items()}
            return readings

        except BTLEException as e:
            logging.debug("Unable to take sensor readings.")
            logging.debug(e)
            return {}

    def reconnect(self):
        try:
            self._tag.connect(self._tag.deviceAddr, self._tag.addrType)
        except Exception as e:
            self._tag = SensorTag(SENSORTAG_ADDRESS)
            raise e

    def to_fahrenheit(self, celsius):
        return (celsius * 1.8) + 32

    def thermostat_readings(self):
        ret_val = {}
        raw_readings = self.raw_readings()
        if not raw_readings:
            self.reconnect()
            raw_readings = self.raw_readings()

        if raw_readings:
            est_time = datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')
            ret_val['time'] = est_time
            ret_val['humidity'] = raw_readings['humidity']
            ret_val['pressure'] = raw_readings['pressure']
            ret_val['battery'] = raw_readings['battery']
            # IR Temperature, both object and ambient temperature (deprecated from June 2017)
            # http://processors.wiki.ti.com/index.php/CC2650_SensorTag_User%27s_Guide#Calibration
            #temperature = round((self.to_fahrenheit(raw_readings["ir_temp"]) +
            #                     self.to_fahrenheit(raw_readings["humidity_temp"]) +
            #                     self.to_fahrenheit(raw_readings["baro_temp"])) / 3, 1)
            temperature = round((self.to_fahrenheit(raw_readings["humidity_temp"]) +
                                 self.to_fahrenheit(raw_readings["baro_temp"])) / 2, 1)

            ret_val['temperature'] = temperature

        return ret_val


def main():
    print('Connecting to {}'.format(SENSORTAG_ADDRESS))

    not_connected=True

    while not_connected:
        try:
            thermostat = TempSensor()
            not_connected = False
        except Exception as e:
            print("Send notification unable to connect.")


    print('Press Ctrl-C to quit.')
    while True:
        # get sensor readings
        readings = thermostat.thermostat_readings()
        print("Thermostat:\t{}\n".format(readings))
        time.sleep(FREQUENCY_SECONDS)


if __name__ == "__main__":
    main()
