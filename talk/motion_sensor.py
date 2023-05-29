import sys
import time

import RPi.GPIO as GPIO


class MotionSensor:
    def __init__(self, motion_sensor_pin: int):
        self.motion_sensor_pin = motion_sensor_pin

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motion_sensor_pin, GPIO.IN)

    def detect(self) -> bool:
        return GPIO.input(self.motion_sensor_pin) == GPIO.HIGH

    def continuous_detect(self):
        while True:
            try:
                if self.detect():
                    return True
                time.sleep(1)
            except KeyboardInterrupt:
                GPIO.cleanup()
                sys.exit()


if __name__ == '__main__':
    motion_sensor_pin = 26

    motionSensor = MotionSensor(motion_sensor_pin)

    isDetect = motionSensor.continuous_detect()
    if isDetect:
        print('I detect you !')
