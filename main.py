import minimalmodbus
import serial
import time

# Настройка Modbus RTU для работы с устройством
class SoilSensorRS485(minimalmodbus.Instrument):
    def __init__(self, port, slave_address):
        super().__init__(port, slave_address)
        self.serial.baudrate = 4800  # Скорость передачи данных
        self.serial.timeout = 10     # Таймаут ответа
        self.mode = minimalmodbus.MODE_RTU

    # Чтение данных влажности почвы (значение увеличено в 10 раз)
    def read_moisture(self):
        return self.read_register(0, 1) / 10.0

    # Чтение температуры (значение увеличено в 10 раз)
    def read_temperature(self):
        return self.read_register(1, 1) / 10.0

    # Чтение уровня pH (значение увеличено в 10 раз)
    def read_ph(self):
        return self.read_register(2, 1) / 10.0

    # Чтение электропроводности (значение увеличено в 10 раз)
    def read_conductivity(self):
        return self.read_register(3, 1) / 10.0

    # Если есть дополнительные параметры, например, содержание нитрогена, фосфора и калия
    def read_nitrogen(self):
        return self.read_register(4, 1)

    def read_phosphorus(self):
        return self.read_register(5, 1)

    def read_potassium(self):
        return self.read_register(6, 1)

# Основная функция работы с датчиком
def main():
    try:
        # Создаем объект для работы с датчиком на порту '/dev/cu.usbserial-311430'
        sensor = SoilSensorRS485(port='/dev/cu.usbserial-311430', slave_address=1)

        # Чтение данных с датчика
        moisture = sensor.read_moisture()
        temperature = sensor.read_temperature()
        ph = sensor.read_ph()
        conductivity = sensor.read_conductivity()
        nitrogen = sensor.read_nitrogen()  # Если есть поддержка этих параметров
        phosphorus = sensor.read_phosphorus()
        potassium = sensor.read_potassium()

        # Вывод данных
        print(f'Soil Moisture: {moisture}%')
        print(f'Soil Temperature: {temperature}°C')
        print(f'Soil pH: {ph}')
        print(f'Soil Conductivity (EC): {conductivity} µS/cm')
        print(f'Nitrogen Content: {nitrogen} mg/L')
        print(f'Phosphorus Content: {phosphorus} mg/L')
        print(f'Potassium Content: {potassium} mg/L')

    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()