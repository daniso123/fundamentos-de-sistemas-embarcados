import RPi.GPIO as GPIO


class TemperatureControlModule:
    def __init__(self):
        self.heating_resistor_port = 23
        self.cooling_resistor_port = 24

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.heating_resistor_port, GPIO.OUT)
        GPIO.setup(self.cooling_resistor_port, GPIO.OUT)

        self.heater = GPIO.PWM(self.heating_resistor_port, 1000)
        self.heater.start(0)

        self.cooler = GPIO.PWM(self.cooling_resistor_port, 1000)
        self.cooler.start(0)

    def heat_the_oven(self, pid):
        self.heater.ChangeDutyCycle(pid)

    def cool_the_oven(self, pid):
        self.cooler.ChangeDutyCycle(pid)