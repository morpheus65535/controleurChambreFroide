import RPi.GPIO as GPIO
from time import time, sleep

from config import settings
from sensor import interior_temperature
from database import TempLog


class Relay:
    def __init__(self):
        self.pin = 14

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT, initial=False)

    def set_high(self):
        GPIO.output(self.pin, True)

    def set_low(self):
        GPIO.output(self.pin, False)

    def cleanup(self):
        GPIO.cleanup(self.pin)

    def get_state(self):
        return GPIO.input(self.pin)


relay = Relay()


def set_required_relay_state():
    from weather import get_latest_logged_exterior_temp

    t_end = time() + 60 * 10
    while time() < t_end:
        sleep(60)
        if settings.getboolean('general', 'enabled'):
            temp_int = interior_temperature.temperature
            temp_ext = get_latest_logged_exterior_temp()
            temp_low = settings.getint('general', 'temp_low')
            temp_high = settings.getint('general', 'temp_high')
            if not all([temp_int, temp_ext, temp_low, temp_high]):
                continue

            if temp_int < temp_low:
                # it's too cold in the cold room
                if temp_ext > temp_low:
                    # we use heat from outdoor
                    relay.set_high()
                    update_last_relay_state()
                else:
                    # we shut it down because outdoor can't help us
                    relay.set_low()
            elif temp_low <= temp_int <= temp_high:
                # we're in the desired range, we can take a brake!
                relay.set_low()
            elif temp_int > temp_high:
                # it's too hot in the cold room
                if temp_ext < temp_high:
                    # we use cold from outdoor
                    relay.set_high()
                    update_last_relay_state()
                else:
                    # we shut it down because outdoor can't help us
                    relay.set_low()


def update_last_relay_state():
    relay_state = TempLog.select().order_by(TempLog.timestamp.desc()).get_or_none()
    if relay_state:
        relay_state.state = True
        relay_state.save()
