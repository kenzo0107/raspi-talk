import sys
from time import sleep

import RPi.GPIO as GPIO


class TactSwitch:
    def __init__(self, switch_pin):
        self.switch_pin = switch_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(switch_pin, GPIO.IN)

    def on(self):
        return GPIO.input(self.switch_pin) == GPIO.HIGH

    def off(self):
        return GPIO.input(self.switch_pin) == GPIO.LOW


if __name__ == '__main__':
    tactSwitch = TactSwitch(switch_pin=14)
    led_pin = 16
    try:
        while True:
            if tactSwitch.on():
                GPIO.output(led_pin, GPIO.HIGH)
            else:
                GPIO.output(led_pin, GPIO.LOW)
            sleep(0.3)
    except KeyboardInterrupt:
        GPIO.output(led_pin, GPIO.LOW)
        GPIO.cleanup()
        sys.exit()
