#!/usr/bin/python3
import time
import psutil
import argparse


#
# Need write access to /sys/devices/pwm-fan/target_pwm or run as root.
#

class FanCtrl:

    def __init__(self):
        args = self._args()
        self._low = args.low
        self._high = args.high
        self._delay = args.delay
        if args.verbose != 0:
            self._verbose = True
        else:
            self.verbose = False
        return

    @classmethod
    def _args(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument("--low", help="Temp in degrees c at which fan turns off", default=25)
        parser.add_argument("--high", help="Temp in degrees c at which fan runs at max", default=45)
        parser.add_argument("--delay", help="Interval in seconds between fan speed updates", default=2)
        parser.add_argument("--verbose", help="If non zero then log verbose commentary to stdout", default=1)
        return parser.parse_args()

    def _speed(self):
        curr_temp = psutil.sensors_temperatures()['thermal-fan-est'][0].current
        if self._verbose:
            print("Curr Temp :" + str(curr_temp))
        spd = 255 * ((curr_temp - self._low) / (self._high - self._low))
        return int(min(max(0, spd), 255))

    def _update(self):
        spd = self._speed()
        if self._verbose:
            print("New fan speed {:.0f} %".format((spd / 255) * 100))
        with open("/sys/devices/pwm-fan/target_pwm", "w") as file:
            file.write(f"{spd}")
        return

    def manage_fan_speed(self):
        while True:
            self._update()
            time.sleep(self._delay)


if __name__ == '__main__':
    FanCtrl().manage_fan_speed()
