import serial.tools.list_ports
import pyvisa
import time
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
            #if byte_in != None:
            byte_in = ser.read(1)
            data_in.append(byte_in.decode())
            #else:
             #   break
        data_in_str = ''.join(data_in)

        return data_in_str
    def search_instek(self):
        out = []
        ports = serial.tools.list_ports.comports()

        for port in ports:
            for speed in [115200,9600]:
                ser = serial.Serial(port.device,
                                    baudrate=speed,
                                    timeout=100)
                ser.write("*IDN?\n".encode())

                rx_from_port = self.read_data_com(ser)
                if "GW INSTEK" in rx_from_port:
                    out = port
                    break
                ser.close()
        return out

    def search_measure_supply(self):
        out = []
        ports = serial.tools.list_ports.comports()

        for port in ports:
            for speed in [115200,9600]:
                ser = serial.Serial(port.device,
                                    baudrate=speed,
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

