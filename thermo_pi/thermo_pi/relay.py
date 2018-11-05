import RPi.GPIO as GPIO
import time
import logging

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
    Relay.on()
    time.sleep(2)
    Relay.off()
