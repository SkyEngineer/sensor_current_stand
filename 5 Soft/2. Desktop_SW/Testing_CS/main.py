import serial.tools.list_ports
from time import monotonic
# скорость
BAUDRATE = 9600

# запрос
SEARCH_MESSAGE = bytes([0xAA])



if __name__ == '__main__':
    ports = serial.tools.list_ports.comports()

    # список всех портов
    for port in ports:
        print(port.device)

    # опрашиваем каждый порт, посылаю туда запрос 0xAA
    for port in ports:
        ser = serial.Serial(port.device, baudrate=BAUDRATE, timeout=1)
        ser.write(SEARCH_MESSAGE)

        data = ser.read(1)  # Read 1 bytes from the COM port
        print(data, port.device)
        match data:
            # стенд
            case bytes([0xBB]):
                serial_port_stand = port

            # всё остальное
            case _:
                print("None")
        ser.close()



