import minimalmodbus
import serial
import time

# Setting up Modbus RTU to work with the device
class SoilSensorRS485(minimalmodbus.Instrument):
    def __init__(self, port, slave_address):
        super().__init__(port, slave_address)
        self.serial.baudrate = 4800  # Data transmission speed
        self.serial.timeout = 10     # Response timeout
        self.mode = minimalmodbus.MODE_RTU

    # Reading soil moisture data
    def read_moisture(self):
        return self.read_register(0, 1)  # No scaling

    # Reading soil temperature data
    def read_temperature(self):
        return self.read_register(1, 1)  # No scaling

    # Reading soil pH level
    def read_ph(self):
        return self.read_register(3, 1)  # No scaling

    # Reading electrical conductivity (EC) and scaling the result to real values
    def read_conductivity(self):
        raw_value = self.read_register(2, 1)
        return raw_value * 100  # Scale EC value to µS/cm

# Main function to work with the sensor
def main():
    try:
        # Create an object to work with the sensor on port '/dev/cu.usbserial-311430'
        sensor = SoilSensorRS485(port='/dev/cu.usbserial-311430', slave_address=1)

        # Reading data from the sensor
        moisture = sensor.read_moisture()
        temperature = sensor.read_temperature()
        ph = sensor.read_ph()
        conductivity = sensor.read_conductivity()

        # Displaying the data
        print(f'Soil Moisture: {moisture}%')
        print(f'Soil Temperature: {temperature}°C')
        print(f'Soil pH: {ph}')
        print(f'Soil Conductivity (EC): {conductivity} µS/cm')

    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()