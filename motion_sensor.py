import time

import RPi.GPIO as GPIO

GPIO_PIN = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN)

if __name__ == "__main__":

    while True:
        if GPIO.input(GPIO_PIN) == GPIO.HIGH:
            print("I found you")
            time.sleep(2)
