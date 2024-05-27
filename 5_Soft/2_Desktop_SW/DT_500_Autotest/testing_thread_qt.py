import time
import power_supply_sensor
import power_supply_measure
import voltmeter

from PyQt6 import QtCore

# класс процесса тестирования
class MyThread(QtCore.QThread):
    mysignal_status = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.running = False
        # порты для общения с датчиками,это именно обекты
        self.com_ports = {"stand": None,
                          "power_sensor": None,
                          "power_current": None,
                          "voltmeter": None}

    def start(self, dict_com_ports):
        self.com_ports = dict_com_ports

    def run(self):
        self.running = True
        # создаем обеекты
        ps_sensor = power_supply_sensor.Power_Supply_Sensor(self.com_ports["power_sensor"])
        ps_current = power_supply_measure.Power_Supply_Measure(self.com_ports["power_current"])
        volt_meter = voltmeter.Voltmeter(self.com_ports["voltmeter"])

        for num_sensor in range(1, 33):
            if self.running == True:
                measure_data = []
                for voltage in [16.0, 27.0, 32.0]:
                    # 1. включаем датчик
                    # 1.1 включаем землю на стенде
                    self.com_ports["stand"].write(bytes([num_sensor]))
                    time.sleep(0.1)

                    # 1.2 устанавливаем и включаем питание датчика на 16 В
                    send_data = bytes([])
                    ps_sensor.set_voltage(voltage)
                    time.sleep(0.1)
                    ps_sensor.set_state_output(1)
                    # *********************
                    # проверяем нет ли КЗ по току, если есть - сразу отключаемся
                    ps_sensor.get_data()

                    sensor_measure = []
                    for curent_measure in [0.0, 100.0, 200.0, 300.0, 400.0, 500.0]:
                        # 3. Блок фомирования тока в отключенном состоянии
                        ps_current.set_current(curent_measure)
                        time.sleep(0.1)
                        ps_current.set_state_output(1)
                        time.sleep(0.1)

                        # 3. Меряем потребляемый датчиком ток
                        sensor_current = ps_sensor.get_current()

                        # 4. Меряем выдаваемое датчиком напряжение
                        sensor_measure.append(volt_meter.get_data())

                        # формируем массив
                        measure_data.append([num_sensor, None, voltage, sensor_current, sensor_measure])
                        self.mysignal_measure.emit()

                # выдаем весь массив на запись
                self.mysignal_measure_all_data.emit(self.mysignal_measure_all_data.emit)
                # [№ датчика, статус,[Uпит, Iпит,[Uизм(0А), Uизм(100А), Uизм(200А), Uизм(300А), Uизм(400А), Uизм(500А)]]]
            else:
                self.running = False
                break
        # while (self.running == True):
