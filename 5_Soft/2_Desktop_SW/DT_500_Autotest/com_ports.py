import serial.tools.list_ports

class Com_Ports(object):
    '''Опрашиваем порты и ищем наши приборы подключенные '''
    def __init__(self):
        self.port_stend = 0
        self.speed = {"port_commutator": 9600,
                      "port_power_supply_measure": 115200,
                      "power_supply_sensor": 115200}

        # поисковые сообщения
        self.search_message = {"commutator": bytes([0xAA]),
                               "": *IDN}
        self.antwort_message = {"":,}


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