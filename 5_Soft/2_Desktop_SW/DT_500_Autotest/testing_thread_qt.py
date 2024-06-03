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

    def quit(self):
        self.running == False

    def init_instruments(self):
        # стенд
        self.ser_stand.write(bytes(0xFF))

        # Вольтметр
        # Измерение в В
        ident = self.visa_voltmeter.query("*IDN?")
        print(ident)
        temp_rx = self.visa_voltmeter.query("SENS:VOLT:DC")
        print(temp_rx)

        # # БП датчиков
        # # отключаем выход
        # self.ser_supply_sensor.write(":SYST:OUTP:STAT[1] OFF\n".encode())
        # time.sleep(0.1)
        # # ставим 27 В
        # # ser_stand.write(":SYST::SOURce2:VOLTage 27.000\n".encode())
        # self.ser_supply_sensor.write("VSET1:27.0\n".encode())
        #
        # # БП тока
        # # отключаем выход
        # self.ser_measure_supply.write("OUTPut:STATe OFF\n".encode())
        # time.sleep(0.1)
        # # Ставим ток в 0 А
        # self.ser_measure_supply.write("CURRent:LEVel:IMMediate:AMPLitude 0 \n".encode())


    # def start(self, dict_com_ports):
    #     self.com_ports = dict_com_ports


    def run(self):

        if self.running == True:
            # self.ser_supply_sensor = serial.Serial(self.com_ports["port_instek"][1].device,
            #                                        baudrate=115200,
            #                                        timeout=0)
            # self.ser_measure_supply = serial.Serial(self.com_ports["port_measure_supply"][1].device,
            #                                         baudrate=115200,
            #                                         timeout=0)
            # self.visa_voltmeter = pyvisa.ResourceManager().open_resource(self.com_ports["port_visa_voltmeter"][1])
            #
            # self.ser_stand = serial.Serial(self.com_ports["port_stend"][1].device,
            #                                baudrate=9600,
            #                                timeout=0)
            # self.init_instruments()
            self.mysignal_status.emit("Инициализация")
            time.sleep(1)

            self.mysignal_status.emit("Тестирование...")
            for num_sensor in range(1, 3):
                if self.running == False:
                    break

                measure_data = []
                for u_supply_sensor in [16.0, 27.0, 32.0]:
                    if self.running == False:
                        break
                    # 1. включаем датчик
                    # 1.1 включаем землю на стенде
                    # self.com_ports["stand"].write(bytes([num_sensor]))
                    measure_data = [num_sensor, None]
                    time.sleep(1)

                    # 1.2 устанавливаем и включаем питание датчика на 16 В
                    # ps_sensor.set_voltage(voltage)
                    # time.sleep(0.1)
                    # ps_sensor.set_state_output(1)
                    measure_data.append(u_supply_sensor)
                    # читаем значение тока датчика
                    measure_data.append(0.040) #i_supply_sensor

                    sensor_measure = []
                    for current_measure in [0.0, 100.0, 200.0, 300.0, 400.0, 500.0]:
                        if self.running == False:
                            break
                        # 3. Блок фомирования тока в отключенном состоянии
                        # ps_current.set_current(curent_measure)
                        time.sleep(0.1)
                        # ps_current.set_state_output(1)
                        time.sleep(0.1)

                        # 4. Меряем выдаваемое датчиком напряжение
                        # sensor_measure.append(volt_meter.get_data())
                        sensor_measure.append(0.4)

                    # формируем массив
                    measure_data.append(sensor_measure)

                    # выдаем весь сформирвованный массив
                    self.measure_data_for_doc.append(measure_data)
                    self.mysignal_measure.emit(measure_data)

            if self.running == True:
                self.mysignal_status.emit("Тестирование завершено")
            else:
                self.mysignal_status.emit("Тестирование прервано")

            self.mysignal_status.emit("Запись протокола...")

            self.report_excel.make_report_excel(self.measure_data_for_doc)
            self.mysignal_status.emit("Запись протокола завершена")
            # measure_data =  [№ датчика, статус, Uпит, Iпит,[Uизм(0А), Uизм(100А), Uизм(200А), Uизм(300А), Uизм(400А), Uизм(500А)]]]
        else:
            pass
        #     self.ser_stand.close()
        #     self.ser_supply_sensor.close()
        #     self.ser_measure_supply.close()

                # ****************************************
                # measure_data =  [№ датчика, статус, Uпит, Iпит,[Uизм(0А), Uизм(100А), Uизм(200А), Uизм(300А), Uизм(400А), Uизм(500А)]]]
        #     else:
        #         self.running = False
        #         break
        # while (self.running == True):
