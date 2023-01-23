import smbus2
import bme280


class LeitorTemperaturaExterna:

    def __init__(self):
        self.port = 1
        self.address = 0x76
        self.bus = smbus2.SMBus(self.port)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)
        self.data = bme280.sample(self.bus, self.address, self.calibration_params)

    def show_full_sensor_data(self):
        print(self.data.id)
        print(self.data.timestamp)
        print(self.data.temperature)
        print(self.data.pressure)
        print(self.data.humidity)

    def get_external_temperature(self):
        self.data = bme280.sample(self.bus, self.address, self.calibration_params)
        return self.data.temperature