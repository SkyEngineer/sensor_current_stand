import serial.tools.list_ports

class Com_Ports(object):

    def __init__(self):
        self.port_stend = 0
        self.speed = {"port_stend": 9600}
        self.search_message_stend = bytes([0xAA])

        self.port_BP1 = 0
        self.port_BP2 = 0

    def search_ports(self):
        ports = serial.tools.list_ports.comports()

        # список всех портов
        for port in ports:
            print(port.device)

        # опрашиваем каждый порт, посылаю туда запрос 0xAA
        for port in ports:
            ser = serial.Serial(port.device,
                                baudrate=self.speed["port_stand"],
                                timeout=1)
            ser.write(self.search_message_stend)

            data = ser.read(1)  # Read 1 bytes from the COM port
            print(data, port.device)
            match data:
                # стенд
                case bytes([0xBB]):
                    self.port_stend = port

                # всё остальное
                case _:
                    print("None")
            ser.close()
        print(self.port_stend)