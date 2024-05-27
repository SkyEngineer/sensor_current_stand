import serial.tools.list_ports
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
                               "*IDN?"]
        # порты аппаратуры
        self.port_voltmeter = None
        self.port_PS_measure = None
        self.port_PS_sensor = None
        self.port_stend = None

    def search_ports(self):
        out = []
        ports = serial.tools.list_ports.comports()

        if len(ports) < 4:
            return [1, "Аппаратура не подключена", None]
        else:
            # опрашиваем каждый порт, посылаю туда запрос по списку
            # GPP 115200
            for port in ports:
                # перебираем скорость
                for speed_data in self.speed:
                    ser = serial.Serial(port.device,
                                        baudrate=speed_data,
                                        timeout=100)
                    # посылаем сообщения и читаем ответ
                    for send_data in self.search_message:
                        ser.write(send_data)
                        # читаем данные, надо учесть,ч т стенд выдает 1 байт, но остальные выдают целые сообщения
                        # надо читать пока не встретиться определенный символ
                        data_read = ser.read(2)
                        # ищем чему соответсвует
                        # разные приборы дают разные ответы по формату...
                        # *IDN?   GPP: GW INSTEK, GPP-3323, SN: xxxxxxxx, Vx.xx
                        match data_read[0]:
                            # стенд
                            case 0xAA:
                                out = ser
                                pass
                            # # вольтметр
                            # case 0xAB:
                            #     pass
                            # # источник питания датчиков
                            # case 0xAC:
                            #     pass
                            # # источник тока
                            # case 0xAF:
                            #     pass
                            # # остальные ответы
                            case _:
                                pass
                    ser.close()
        return out