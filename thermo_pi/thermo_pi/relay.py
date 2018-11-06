import RPi.GPIO as GPIO
import time
import logging
import sys

logger = logging.getLogger()

class Relay:
    GPIO_PIN_18 = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN_18, GPIO.OUT)
    @staticmethod
    def on():
        GPIO.output(Relay.GPIO_PIN_18, GPIO.HIGH)
        logging.debug("GPIO.HIGH ON")


    @staticmethod
    def off():
        GPIO.output(Relay.GPIO_PIN_18, GPIO.LOW)
        logging.debug("GPIO.LOW OFF")

if __name__ == "__main__":
    print("sys argv")
    on_off = "na"
    if len(sys.argv)>1:
        on_off = sys.argv[1]
    if on_off == "on":
        Relay.on()
    elif on_off == "off":
        Relay.off()
    else:
        print("pass on ot off on the commandline!")
        
