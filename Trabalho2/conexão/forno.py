class Forno:
    def __init__(self):
        self.on = False
        self.working = False
        self.temperature_curve_mode = False
        self.outside_temperature = 9999.0
        self.oven_temperature_target = 9999.0
        self.internal_temperature = 9999.0