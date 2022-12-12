import RPi.GPIO as GPIO


class Relay:
    def __init__(self):
        self.pin = 14

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT, initial=False)

    def set_high(self):
        GPIO.output(self.pin, True)

    def set_low(self):
        GPIO.output(self.pin, False)

    def cleanup(self):
        GPIO.cleanup(self.pin)

    def get_state(self):
        return False
        # return GPIO.input(self.pin)


relay = Relay()
