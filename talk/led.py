import sys
from time import sleep

import RPi.GPIO as GPIO


class LED:
    def __init__(self, led_pin):
        self.led_pin = led_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def __del__(self):
        GPIO.output(self.led_pin, GPIO.LOW)

    def turn_on(self):
        GPIO.output(self.led_pin, GPIO.HIGH)

    def turn_out(self):
        GPIO.output(self.led_pin, GPIO.LOW)

    def blink(self):
        while True:
            try:
                led.turn_on()
                sleep(0.5)
                led.turn_out()
                sleep(0.5)
            except KeyboardInterrupt:
                GPIO.cleanup()
                sys.exit()


if __name__ == '__main__':
    led_pin = 16
    led = LED(led_pin)
    led.blink()
