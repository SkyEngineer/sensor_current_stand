from PyQt6 import QtCore, QtWidgets, uic
import testing_thread_qt
import com_ports
import time

# класс отображения окна
class MyWindow (QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        Form, Base = uic.loadUiType("ui/DT_500_Autotest.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.measure_data = []

        # параметры, вводимые вручную
        self.DT_num_manual = 1
        self.DT_num_group = 1
        self.DT_type_manual = "DT-100"
        self.DT_SN_manual = "000"
        self.Temperature_manual = "+25"

        # заливаем окна со значениями напряжения белым цветом и черным текстом
        self.set_QLineEdit_style()

        # кнопки
        self.ui.Connect_Button.clicked.connect(self.btn_connect_click)
        self.ui.Start_Button.clicked.connect(self.btn_start_click)

        # поток тестирования
        self.mythread = testing_thread_qt.MyThread()
        self.mythread.mysignal_status.connect(self.set_console_test)

        # self.mythread.started.connect(self.set_console_text)
        # self.mythread.finished.connect(self.set_console_text)

        # self.mythread.mysignal_status.connect(self.start_click_default)
        # self.mythread.mysignal_measure.connect(self.work_with_measure)

        self.dict_com_ports = None
        self.num_of_sensors = None

    # заливаем окна со значениями напряжения белым цветом и черным текстом
    def set_QLineEdit_style(self):
        for item in self.ui.centralwidget.findChildren(QtWidgets.QLineEdit):
            item.setStyleSheet("color: black;  background-color: white")
            # item.setText("-")
            # if "auto_tab_DT_num" in item.objectName():

    # устаналиваем измеренное значение
    def set_measure_data(self, name_widget, data):
        """data is float XX.x"""
        for item in self.ui.centralwidget.findChildren(QtWidgets.QLineEdit):
            if name_widget == item.objectName():
                item.setText(str(data))

    def set_measure_color(self,name_widget, color):
        for item in self.ui.centralwidget.findChildren(QtWidgets.QLineEdit):
            if name_widget == item.objectName():
                item.setStyleSheet(f"color: black; background-color: {color}")

    def set_measure_color_ext(self,name_widget, status):
        for item in self.ui.centralwidget.findChildren(QtWidgets.QLineEdit):
            if name_widget == item.objectName():
                if status == 1:
                    item.setStyleSheet(f"color: black; background-color: rgb(255, 71, 71);")
                if status == 0:
                    item.setStyleSheet(f"color: black; background-color: rgb(27, 189, 9);")

    def clear_measure_data(self):
        pass
        # for item in self.ui.centralwidget.findChildren(QtWidgets.QLineEdit):
        #     if name_widget == item.objectName():
        #         item.setText(str(data))

    def set_console_text(self, text_data):
        for item in self.ui.centralwidget.findChildren(QtWidgets.QTextBrowser):
            if "console_all" == item.objectName():
                item.setStyleSheet(f"color: black; background-color: white")
                item.append(time.strftime("[%H:%M:%S]") + "\n" + "   " + text_data)

    def set_console_test(self, text_data):
        for item in self.ui.centralwidget.findChildren(QtWidgets.QTextBrowser):
            if "console_testing" == item.objectName():
                item.setStyleSheet(f"color: black; background-color: white")
                item.append(time.strftime("[%H:%M:%S]") + "   " + text_data)


    def set_console_text_thread(self, text_data):
        for item in self.ui.centralwidget.findChildren(QtWidgets.QTextBrowser):
            if "console" == item.objectName():
                item.setStyleSheet(f"color: black; background-color: white")
                item.append(time.strftime("[%H:%M:%S %x]") + "\n" + "   " + text_data)

    # Подключение приборов
    def btn_connect_click(self):
        self.set_console_text("Поиск аппаратуры...")

        port_instek = self.ports.search_instek()
        if port_instek != []:
            print(port_instek)
        else:
            self.set_console_text("БП датчиков не найден")

        port_measure_supply = self.ports.search_measure_supply()
        if port_measure_supply != []:
            print(port_measure_supply)
        else:
            self.set_console_text("БП изм. тока не найден")

        port_visa_voltmeter = self.ports.search_visa_voltmeter()
        if port_visa_voltmeter != []:
            print(port_visa_voltmeter)
        else:
            self.set_console_text("Вольтметр не найден")

        self.dict_com_ports = {"port_instek": port_instek,
                               "port_measure_supply": port_measure_supply,
                               "port_visa_voltmeter": port_visa_voltmeter}

        self.set_measure_data("port_supply_sensor", port_instek.device)
        self.set_measure_data("port_measure_supply", port_measure_supply.device)
        self.set_measure_data("port_voltmeter", port_visa_voltmeter)

        self.mythread.com_ports = self.dict_com_ports

        self.set_console_text("Поиск аппаратуры завершен")


    # старт тестирования
    def btn_start_click(self):
        # читаем данные заданные вручную
        self.DT_type_manual = self.ui.DT_type_manual.currentText()
        self.Temperature_manual = self.ui.Temperature_manual.currentText()

        # проверяем
        if 0 < int(self.ui.DT_num_manual.text()) <= 72:
            self.DT_num_manual = int(self.ui.DT_num_manual.text())
            for i in range(1,5):
                if self.DT_num_manual in range(18 * i - 17, 18 * i + 1):
                    self.DT_num_group = i
                    break

        else:
            self.DT_num_manual = None
            self.DT_num_group = None
            self.set_console_test("Неверно задан номер датчика на стенде")

        if (len(self.ui.DT_SN_manual.text()) == 3) and (0 <= int(self.ui.DT_SN_manual.text()) < 999):
            self.DT_SN_manual = self.ui.DT_SN_manual.text()
        else:
            self.DT_SN_manual = None
            self.set_console_test("Неверно задан заводской. номер датчика")

        # count = [self.DT_num_manual, self.DT_SN_manual] + list(self.dict_com_ports.values())

        count = [self.DT_num_manual, self.DT_SN_manual]
        if None not in count:
            self.set_console_test(f"Проверяется датчик {self.DT_type_manual} №{str(self.DT_num_manual)}(Зав.№ {self.DT_SN_manual}) из группы "
                                  f"{str(self.DT_num_group)} при {str(self.Temperature_manual)} градусах")

            # устанавливаем значения
            self.ui.DT_num.setText(str(self.DT_num_manual))
            self.ui.DT_num_group.setText(str(self.DT_num_group))

            # передаем данные в поток тестирования
            self.DT_num_manual
            self.DT_num_group
            self.DT_type_manual
            self.DT_SN_manual
            self.Temperature_manual

            # запускаем поток тестирования
        else:
            pass
    #
    #
    #     # проверяем введенные данные
    #
    #
    #
    #
    #     if self.ui.Start_Button.text() == "Старт":
    #         self.num_of_sensors = int(self.ui.num_of_sensor.text())
    #         self.set_console_text("Начало тестирования...")
    #         self.mythread.running = True
    #         self.mythread.num_of_sensors = self.num_of_sensors
    #         self.mythread.start()
    #         time.sleep(2)
    #         self.ui.Start_Button.setText("Стоп")
    #         self.ui.Start_Button.setStyleSheet(f"color: black; background-color: red")
    #         self.set_QLineEdit_style()
    #     else:
    #         self.mythread.running = False
    #         self.mythread.quit()
    #         self.mythread.wait(500)
    #
    #         self.ui.Start_Button.setStyleSheet("")
    #         # self.set_console_text("Остановка тестирования...")
    #         self.ui.Start_Button.setText("Старт")
    #
    # def start_click_default(self,data):
    #     if "Запись протокола завершена" in data:
    #         self.ui.Start_Button.setText("Старт")
    #         self.ui.Start_Button.setStyleSheet("")
    #         pass



        # if self.ui.Start_Button.text() == "Старт":
        #     #     старт тестирования
        #     # self.mythread.start(self.dict_com_ports)
        #
        #     # self.ui.Start_Button.setText("Стоп")
        #     # self.ui.Start_Button.setStyleSheet(f"color: black; background-color: red")
        #
        #     # self.mythread.start()
        #     # time.sleep(1)
        # if self.ui.Start_Button.text() == "Стоп":
        #     self.mythread.running = False
        #     self.mythread.wait(500)

    def work_with_measure(self, measure_data):
        self.measure_data_for_doc.append(measure_data)
        # measure_data =  [№ датчика, статус, Uпит, Iпит,
        #                 [Uизм(0А), Uизм(100А), Uизм(200А), Uизм(300А), Uизм(400А), Uизм(500А)],
        #                 [Uизм(0А)_norm, Uизм(100А)_norm, Uизм(200А)_norm, Uизм(300А)_norm, Uизм(400А)_norm, Uизм(500А)_norm]]

        self.set_measure_data(f"U_{str(int(measure_data[2]))}_I_0_N_{str(int(measure_data[0]))}",
                              str(measure_data[4][0]))
        self.set_measure_color_ext(f"U_{str(int(measure_data[2]))}_I_0_N_{str(int(measure_data[0]))}",
                                   measure_data[5][0])

        self.set_measure_data(f"U_{str(int(measure_data[2]))}_I_100_N_{str(int(measure_data[0]))}",
                              str(measure_data[4][1]))
        self.set_measure_color_ext(f"U_{str(int(measure_data[2]))}_I_100_N_{str(int(measure_data[0]))}",
                                   measure_data[5][1])

        self.set_measure_data(f"U_{str(int(measure_data[2]))}_I_200_N_{str(int(measure_data[0]))}",
                              str(measure_data[4][2]))
        self.set_measure_color_ext(f"U_{str(int(measure_data[2]))}_I_200_N_{str(int(measure_data[0]))}",
                                   measure_data[5][2])

        self.set_measure_data(f"U_{str(int(measure_data[2]))}_I_300_N_{str(int(measure_data[0]))}",
                              str(measure_data[4][3]))
        self.set_measure_color_ext(f"U_{str(int(measure_data[2]))}_I_300_N_{str(int(measure_data[0]))}",
                                   measure_data[5][3])

        self.set_measure_data(f"U_{str(int(measure_data[2]))}_I_400_N_{str(int(measure_data[0]))}",
                              str(measure_data[4][4]))
        self.set_measure_color_ext(f"U_{str(int(measure_data[2]))}_I_400_N_{str(int(measure_data[0]))}",
                                   measure_data[5][4])

        self.set_measure_data(f"U_{str(int(measure_data[2]))}_I_500_N_{str(int(measure_data[0]))}",
                              str(measure_data[4][5]))
        self.set_measure_color_ext(f"U_{str(int(measure_data[2]))}_I_500_N_{str(int(measure_data[0]))}",
                                   measure_data[5][5])

        self.set_measure_data("auto_tab_DT_num", str(int(measure_data[0])))
        self.set_measure_data("u_supply_sens", str(float(measure_data[2])))
        self.set_measure_data("current_sens", str(float(measure_data[3])))



