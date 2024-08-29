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

    # Чтение данных влажности почвы
    def read_moisture(self):
        return self.read_register(0, 1)  # Без деления

    # Чтение температуры почвы
    def read_temperature(self):
        return self.read_register(1, 1)  # Без деления

    # Чтение уровня pH
    def read_ph(self):
        return self.read_register(3, 1)  # Без деления

    # Чтение электропроводности (EC), где результат увеличивается для приведения к реальным значениям
    def read_conductivity(self):
        raw_value = self.read_register(2, 1)
        return raw_value * 100  # Предположительно корректируем значение EC в µS/cm

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

        # Вывод данных
        print(f'Soil Moisture: {moisture}%')
        print(f'Soil Temperature: {temperature}°C')
        print(f'Soil pH: {ph}')
        print(f'Soil Conductivity (EC): {conductivity} µS/cm')

    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()