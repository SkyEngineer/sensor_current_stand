import time
import power_supply_sensor
import power_supply_measure
import voltmeter
import serial.tools.list_ports
import pyvisa
import json

from PyQt6 import QtCore
import doc_make

# класс процесса тестирования
class MyThread(QtCore.QThread):
    # сигнал статуса
    mysignal_status = QtCore.pyqtSignal(str)
    # сигналы с данными
    mysignal_measure = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        # параметры датчика проверяемого
        self.DT_num_manual = None
        self.DT_num_group = None
        self.DT_type_manual = None
        self.DT_SN_manual = None
        self.Temperature_manual = "+25"

        # подгружаем данные по точности
        self.norm_table = self.load_norm_file(self.DT_type_manual)

        # данные о портах
        self.port_instek = None
        self.port_measure_supply = None
        self.port_visa_voltmeter = None

        # данные об измерениях - общий список
        # self.measure_data =  [№ датчика, статус, Uпит, Iпит,[Uизм(0/0А), Uизм(100/20А), Uизм(200/40А), Uизм(300/60А), Uизм(400/80А), Uизм(500/100А)]]]
        # self.measure_data =  [тип датика, self.DT_SN_manual, статус, Uпит, Iпит, Uизм(0/0А), Uизм(100/20А), Uизм(200/40А), Uизм(300/60А), Uизм(400/80А), Uизм(500/100А)]
        self.measure_data_all = []

    def load_norm_file(self, type_in):
        out = []
        temp = abs(int(self.Temperature_manual))
        if type_in is not None:
            with open(f'norm_{temp}_{type_in}.txt', 'r') as f:
                a = f.readlines()

            for i in a:
                if "\n" in i:
                    out.append(i[:-1].split("\t"))
                else:
                    out.append(i.split("\t"))
            return out

    def run(self):
        self.mysignal_status.emit("Инициализация оборудования...")
        self.init_instruments()
        self.mysignal_status.emit("Инициализация оборудования выполнена")

        self.measure_data_all = [self.DT_type_manual, self.DT_SN_manual, None]
        self.mysignal_status.emit("Тестирование...")

        # перебираем напряжения
        # включаем выход блока питания датчиков, там 0 вольт
        self.port_instek.write("OUTP1:STAT ON\n".encode())
        time.sleep(0.1)

        for u_supply_sensor in [16, 27, 32]:
            # выставляем напряжение
            self.mysignal_status.emit(f"Установка напряжение питания {u_supply_sensor}...")
            self.port_instek.write(f"VSET1:{u_supply_sensor}\n".encode())
            time.sleep(0.1)
            #     проверяем выставленное напряжение
            self.port_instek.write("VOUT1?\n".encode())
            sensor_voltage = float(self.read_data_com(self.port_instek).split("V")[0])
            time.sleep(0.1)
            self.mysignal_measure.emit(["sensor_voltage", sensor_voltage])
            self.measure_data_all.append(u_supply_sensor)

            # измеряем ток потребления
            self.mysignal_status.emit(f"Проверка тока потребления...")
            self.port_instek.write("IOUT1?\n".encode())
            sensor_current = float(self.read_data_com(self.port_instek).split("A")[0])
            self.mysignal_measure.emit(["sensor_current", sensor_current])
            self.measure_data_all.append(sensor_current)

            for current_measure in [int(i[0]) for i in self.norm_table]:
                # Блок фомирования тока
                # отключаем выход
                self.port_measure_supply.write(f"OUTP 0\n".encode())
                time.sleep(0.1)

                # задаем ток
                self.mysignal_status.emit(f"Установка тока {current_measure}...")
                self.port_measure_supply.write(f"CURR {str(current_measure)}\n".encode())
                self.mysignal_measure.emit(["current_measure", current_measure])
                time.sleep(0.1)

                # включаем выход
                self.port_measure_supply.write(f"OUTP 1\n".encode())
                time.sleep(1)

                # меряем напряжение с датчика
                self.mysignal_status.emit(f"Измерение напряжения датчика тока...")
                temp_rx = self.visa_voltmeter.query("MEAS:VOLT:DC?")
                sensor_measure = round(float(temp_rx), 2)
                self.mysignal_measure.emit(["sensor_measure", sensor_measure])
                self.measure_data_all.append(sensor_measure)

                # отключаем выход
                self.port_measure_supply.write(f"OUTP 0\n".encode())
                time.sleep(0.1)

        # завершли работу с током
        self.init_instruments()

        # закрываем порты
        self.port_instek.close()
        self.port_measure_supply.close()

        # оценка исправности датчика
        high_grenze = [float(i[1]) for i in self.norm_table]
        low_grenze = [float(i[2]) for i in self.norm_table]
        norm_temp = []

        for cnt, i in enumerate(self.measure_data_all[-6:]):
            if low_grenze[cnt] <= i <= high_grenze[cnt]:
                norm_temp.append(0)
            else:
                norm_temp.append(1)

        if 1 in norm_temp:
            self.measure_data_all[2] = "НЕ ГОДЕН"
        else:
            self.measure_data_all[2] = "ГОДЕН"

        self.mysignal_measure.emit(["NORM", self.measure_data_all[2]])

        # запускаем формирование отчета
        self.mysignal_status.emit(f"Формирование отчета...")
        self.report_excel.make_report_excel(self.measure_data_for_doc)
        self.mysignal_status.emit("Запись протокола завершена")
        self.mysignal_status.emit("Закрыть поток")


    def isFinished(self):
        self.mysignal_status.emit(f"Тестирование завершено...")

    # def quit(self):
    #     self.running == False

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
        # Вольтметр
        # Измерение в В, Вольтметр изначально при включении в таком режиме
        #temp_rx = self.visa_voltmeter.query("SENS:VOLT:DC")
        #temp_rx = self.visa_voltmeter.query("CONF:VOLT:DC")
        #print(temp_rx)

        # БП датчиков
        self.ser_supply_sensor.write(f"VSET1:0\n".encode())
        time.sleep(0.1)
        self.ser_supply_sensor.write("OUTP1:STAT OFF\n".encode())
        time.sleep(0.1)

        # БП тока
        # отключаем выход
        self.ser_measure_supply.write("OUTP:STAT OFF\n".encode())
        time.sleep(0.1)
        # Ставим ток в 0 А
        self.ser_measure_supply.write("CURR 0\n".encode())
        time.sleep(0.1)
        # Ставим напряжение в 10 В
        self.ser_measure_supply.write("VOLT 10\n".encode())

        return 0
