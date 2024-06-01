import serial.tools.list_ports
import pyvisa
# GPP-74323           питание датчиков
# АКИП-2101/1         Вольтметр
# АКИП 1162-10-1020	Источник измеряемого тока
# АКИП-1162-10-510	Источник измеряемого тока


class Com_Ports(object):
    '''Опрашиваем порты и ищем наши приборы подключенные '''
    def __init__(self):
        self.speed = [9600,
                      115200]

        # поисковые сообщения
        self.search_message = [bytes([0xAA]),
                               "*IDN?\n".encode()]
        # порты аппаратуры
        self.port_voltmeter = None
        self.port_PS_measure = None
        self.port_PS_sensor = None
        self.port_stend = None

    def read_data_com(self, ser):
        data_in = []
        byte_in = None
        data_in_str = None

        while (byte_in != b'\n'):
            byte_in = ser.read(1)
            data_in.append(byte_in.decode())
        data_in_str = ''.join(data_in)

        return data_in_str

    def search_stand(self):
        out = []
        ports = serial.tools.list_ports.comports()

        for port in ports:
            ser = serial.Serial(port.device,
                                baudrate=9600,
                                timeout=100)
            ser.write(bytes([0xAA]))
            byte_in = ser.read(1)
            if byte_in == b'\xbb':
                out = ["port_stand", port]

                break
                #print("stand")
        ser.close()
        return out

    def search_instek(self, stand_port):
        out = []
        ports = serial.tools.list_ports.comports()
        ports.remove(stand_port)

        for port in ports:
            ser = serial.Serial(port.device,
                                baudrate=115200,
                                timeout=100)
            ser.write("*IDN?\n".encode())
            rx_from_port = self.read_data_com(ser)
            if "GW INSTEK,GPP-74323" in rx_from_port:
                out = ["power_supply_sensor", port, port]

                break
        ser.close()
        return out

    def search_measure_supply(self, stand_port, instek_port):
        out = []
        ports = serial.tools.list_ports.comports()
        ports.remove(stand_port)
        # ports.remove(instek_port)

        for port in ports:
            ser = serial.Serial(port.device,
                                baudrate=115200,
                                timeout=100)
            ser.write("*IDN?\n".encode())
            rx_from_port = self.read_data_com(ser)

            if "ITECH,IT-M3910D" in rx_from_port:
                out = ["power_supply_measure", port, port]

                break
        ser.close()
        return out

    def search_visa_voltmeter(self):
        out = []
        rm = pyvisa.ResourceManager()
        list_visa = rm.list_resources()

        for visa_item in list_visa:
            inst = rm.open_resource(visa_item)
            ident = inst.query("*IDN?")
            if "AKIP-2101" in ident:
                out = ["voltmeter", visa_item, ident.split(",")[1]]
                break

        return out