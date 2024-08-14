import time
import power_supply_sensor
import power_supply_measure
import voltmeter
import serial.tools.list_ports
import pyvisa

from PyQt6 import QtCore
import doc_make

# класс процесса тестирования
class MyThread(QtCore.QThread):
    mysignal_status = QtCore.pyqtSignal(str)
    mysignal_measure = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.running = False
        self.com_ports = None
        self.testing_done = False
        self.report_excel = doc_make.Doc_Report()
        self.measure_data_for_doc = []
        self.abort_testing = False
        # k = 3.75/500 +- 0.25/500 = 7.5e-3 +- 0.5e-3 допущение: коридор погрешности линенен
        self.norm_table = [[0.0, 0.1],
                            [0.8, 0.9],
                            [1.5, 1.7],
                            [2.2, 2.5],
                            [2.9, 3.3],
                            [3.6, 4.1]]
        self.measure_data = None
        self.num_of_sensors = 1
        self.num_SN_sensor = "000"
        self.doc_name = 0

    def quit(self):
        self.running == False

    def exam_data(self, list_data):
        all_status = []
        # при задании токов
        for i, data in enumerate(list_data[4]):
            if  (self.norm_table[i][0] <= data < self.norm_table[i][1]):
                # норма
                all_status.append(0)
            else:
                # не норма
                all_status.append(1)

        if 1 in all_status:
            list_data[1] = "Брак"
        else:
            list_data[1] = "Годен"

        # # ток потребления
        # if list_data[3]<=IsL and list_data[3]<=IsH

        return list_data.append(all_status)

    def read_data_com(self, ser):
        data_in = []
        byte_in = None
        data_in_str = None

        while (byte_in != b'\n'): #or (byte_in != b''):
            #if byte_in != None:
            byte_in = ser.read(1)
            data_in.append(byte_in.decode())
            #else:
             #   break
        data_in_str = ''.join(data_in)

        return data_in_str

    def init_instruments(self):
        # стенд
        # self.ser_stand.write(bytes(0xFF))
        # time.sleep(0.1)

        # Вольтметр
        # Измерение в В, Вольтметр изначально при включении в таком режиме
        #temp_rx = self.visa_voltmeter.query("SENS:VOLT:DC")
        #temp_rx = self.visa_voltmeter.query("CONF:VOLT:DC")
        #print(temp_rx)

        # # БП датчиков
        # # отключаем выход
        #self.ser_supply_sensor.write("OUTP1:STAT OFF\n".encode())
        #time.sleep(0.1)
        # # ставим 16 В
        #self.ser_supply_sensor.write("SOUR1:VOLT 16.000\n".encode())
        #time.sleep(0.1)
        
        
        # БП тока
        # отключаем выход
        self.ser_measure_supply.write("OUTP:STAT OFF\n".encode())
        time.sleep(0.1)
        # Ставим ток в 0 А
        self.ser_measure_supply.write("CURR 0\n".encode())
        # Ставим напряжение в 10 В
        self.ser_measure_supply.write("VOLT 10\n".encode())
    
    def debug_print(self, data):
        for i in data:
            print(i)

    def run(self):

        if self.running == True:
            #print(self.com_ports["port_instek"])
            self.ser_supply_sensor = serial.Serial(self.com_ports["port_instek"][1].device,
                                                    baudrate=115200,
                                                    timeout=100)

            self.ser_measure_supply = serial.Serial(self.com_ports["port_measure_supply"][1].device,
                                                     baudrate=115200,
                                                     timeout=100)
            self.visa_voltmeter = pyvisa.ResourceManager().open_resource(self.com_ports["port_visa_voltmeter"][1])
            
            # self.ser_stand = serial.Serial(self.com_ports["port_stend"][1].device,
            #                                baudrate=9600,
            #                                 timeout=100)
            
            self.init_instruments()
            
            
            self.mysignal_status.emit("Инициализация выполнена")
            time.sleep(1)

            self.mysignal_status.emit("Тестирование...")


            for num_sensor in range(1, 2):
                if self.running == False:
                    break
                # 1. включаем датчик
                # 1.1 включаем землю на стенде
                # self.ser_stand.write(bytes([0xFF]))
                # time.sleep(0.1)
                # self.ser_stand.write(bytes([num_sensor]))
                # time.sleep(0.1)

                self.ser_supply_sensor.write(f"VSET1:0\n".encode())
                time.sleep(0.1)
                self.ser_supply_sensor.write("OUTP1:STAT ON\n".encode())
                time.sleep(0.1)
                
                for u_supply_sensor in [16, 27, 32]:
                    if self.running == False:
                        break
                    self.ser_supply_sensor.write(f"VSET1:0\n".encode())
                    time.sleep(0.1)

                    self.measure_data = [self.num_SN_sensor, None, u_supply_sensor]
                    time.sleep(0.1)

                    # 1.2 устанавливаем и включаем питание датчика (GPP Instek)
                    # установка напряжения
                    self.ser_supply_sensor.write(f"VSET1:{u_supply_sensor}\n".encode())
                    time.sleep(3)

                    # читаем значение тока датчика в покое
                    self.ser_supply_sensor.write("IOUT1?\n".encode())
                    current_data_sensor = self.read_data_com(self.ser_supply_sensor)
                    self.measure_data.append(float(current_data_sensor.split("A")[0]))
                    #self.debug_print(self.measure_data)

                    sensor_measure = []
                    for current_measure in [0, 20, 40, 60, 80, 100]:
                        # 3. Блок фомирования тока
                        # отключаем выход
                        self.ser_measure_supply.write(f"OUTP 0\n".encode())
                        time.sleep(0.1)

                        # задаем ток
                        self.ser_measure_supply.write(f"CURR {str(current_measure)}\n".encode())
                        time.sleep(0.1)
                        
                        # включаем выход
                        self.ser_measure_supply.write(f"OUTP 1\n".encode())
                        time.sleep(1)

                        # 4. Меряем выдаваемое датчиком напряжение
                        # sensor_measure.append(volt_meter.get_data())
                        temp_rx = self.visa_voltmeter.query("MEAS:VOLT:DC?")
                        # print("***")
                        # print(num_sensor)
                        # print(u_supply_sensor)
                        # print(current_measure)
                        # print(float(temp_rx))
                        sensor_measure.append(round(float(temp_rx), 2))
                    
                    # отключаем блок форимрования тока
                    self.ser_measure_supply.write(f"OUTP 0\n".encode())
                    # отключаем ключи стенда
                    #self.ser_stand.write(bytes([0xFF]))
                    
                    # формируем массив
                    self.measure_data.append(sensor_measure)

                    # проверяем, что данные находятся в допуске
                    self.exam_data(self.measure_data)
                   
                    # выдаем весь сформированный массив
                    self.measure_data_for_doc.append(self.measure_data)
                    self.mysignal_measure.emit(self.measure_data)
                    #print(self.measure_data)

                # окончание тестирования
                self.mysignal_status.emit("Тестирование завершено")
                # self.ser_stand.write(bytes([0xFF]))

                # отключаем блок форимрования тока
                self.ser_measure_supply.write(f"OUTP 0\n".encode())
                # отключаем ключи стенда

                # Отключение выхода питания датчиков
                self.ser_supply_sensor.write(f"VSET1:0\n".encode())
                # self.ser_supply_sensor.write(f"SOUR1:VOLT 0\n".encode())
                time.sleep(0.1)
                self.ser_supply_sensor.write("OUTP1:STAT OFF\n".encode())
                time.sleep(0.1)
                
                
            self.ser_supply_sensor.close()
            # self.ser_stand.close()
            self.ser_measure_supply.close()



            self.mysignal_status.emit("Запись протокола...")
            self.report_excel.doc_name =  self.doc_name
            self.report_excel.make_report_excel(self.measure_data_for_doc, self.doc_name)
            self.measure_data_for_doc = []
            self.mysignal_status.emit("Запись протокола завершена")
            # measure_data =  [№ датчика, статус, Uпит, Iпит,[Uизм(0А), Uизм(100А), Uизм(200А), Uизм(300А), Uизм(400А), Uизм(500А)]]]
        else:
            pass

