from PyQt6 import QtCore, QtWidgets, uic
import testing_thread_qt
import com_ports
import time

# класс отображения окна
class MyWindow (QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        Form, Base = uic.loadUiType("ui/DT_100_Autotest.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.measure_data_for_doc = []
        self.measure_data_for_doc_status = False
        self.doc_name = time.strftime("Протоколы\Протокол от %d.%m.%Y в %H_%M_%S.xlsx")

        # заливаем окна со значениями напряжения белым цветом и черным текстом
        self.set_measure_U_style()
        # по умолчанию делаем отчет
        # self.ui.get_doc.setChecked(1)

        self.ports = com_ports.Com_Ports()

        # кнопки
        self.ui.Connect_Button.clicked.connect(self.btn_connect_click)
        self.ui.Start_Button.clicked.connect(self.btn_start_click)

        # поток тестирования
        self.mythread = testing_thread_qt.MyThread()
        # self.mythread.started.connect(self.set_console_text)
        # self.mythread.finished.connect(self.set_console_text)
        self.mythread.mysignal_status.connect(self.set_console_text_thread)
        self.mythread.mysignal_status.connect(self.start_click_default)
        self.mythread.mysignal_measure.connect(self.work_with_measure)

        self.dict_com_ports = None
        self.num_of_sensors = None

    # заливаем окна со значениями напряжения белым цветом и черным текстом
    def set_measure_U_style(self):
        for item in self.ui.centralwidget.findChildren(QtWidgets.QLineEdit):
            if "U_" in item.objectName():
                item.setStyleSheet("color: black;  background-color: white")
                item.setText("-")
            if "u_supply_sens" in item.objectName():
                item.setStyleSheet("color: black;  background-color: white")
                item.setText("-")
            if "current_sens" in item.objectName():
                item.setStyleSheet("color: black;  background-color: white")
                item.setText("-")
            if "auto_tab_DT_num" in item.objectName():
                item.setStyleSheet("color: black;  background-color: white")
                item.setText("-")


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
            if "console" == item.objectName():
                item.setStyleSheet(f"color: black; background-color: white")
                item.append(time.strftime("[%H:%M:%S %x]") + "\n" + "   " + text_data)
                # item.append(text_data)

    def set_console_text_thread(self, text_data):
        for item in self.ui.centralwidget.findChildren(QtWidgets.QTextBrowser):
            if "console" == item.objectName():
                item.setStyleSheet(f"color: black; background-color: white")
                item.append(time.strftime("[%H:%M:%S %x]") + "\n" + "   " + text_data)

    # Подключение приборов
    def btn_connect_click(self):
        self.set_console_text("Поиск аппаратуры...")
        # port_stend = self.ports.search_stand()
        # if port_stend != []:
        #     print(port_stend[0], port_stend[1])
        # else:
        #     print("port_stend не найден")
        try:
            print("port_instek")
            port_instek = self.ports.search_instek()
        except:
            print("port_instek  не найден")


        try:
            print("port_measure_supply")
            port_measure_supply = self.ports.search_measure_supply()
        except:
            print("port_measure_supply не найден")

        try:
            print("port_visa_voltmeter")
            port_visa_voltmeter = self.ports.search_visa_voltmeter()
        except:
            print("port_visa_voltmeter не найден")

        # установить значения

        self.dict_com_ports = {"port_stend": [],
                               "port_instek": port_instek,
                               "port_measure_supply": port_measure_supply,
                               "port_visa_voltmeter": port_visa_voltmeter}
        #print(self.dict_com_ports["port_instek"])

        # self.set_measure_data("port_stand", port_stend[1].device)

        self.set_measure_data("port_supply_sensor", port_instek[1].device)

        self.set_measure_data("port_measure_supply", port_measure_supply[1].device)
        self.set_measure_data("port_voltmeter", port_visa_voltmeter[2])

        self.mythread.com_ports = self.dict_com_ports


        self.set_console_text("Поиск аппаратуры завершен")

        # self.mythread.start()


    # старт тестирования
    def btn_start_click(self):
        if self.ui.Start_Button.text() == "Старт":
            self.num_of_sensors = int(self.ui.num_of_sensor.text())
            self.set_console_text("Начало тестирования...")
            self.mythread.running = True
            self.mythread.num_of_sensors = self.num_of_sensors
            self.mythread.num_SN_sensor = self.ui.num_of_sensor.text()
            self.mythread.doc_name = self.doc_name
            self.mythread.start()
            time.sleep(2)
            self.ui.Start_Button.setText("Стоп")
            self.ui.Start_Button.setStyleSheet(f"color: black; background-color: red")
            self.set_measure_U_style()
        else:
            self.mythread.running = False
            self.mythread.quit()
            self.mythread.wait(500)

            self.ui.Start_Button.setStyleSheet("")
            # self.set_console_text("Остановка тестирования...")
            self.ui.Start_Button.setText("Старт")

    def start_click_default(self,data):
        if "Запись протокола завершена" in data:
            self.ui.Start_Button.setText("Старт")
            self.ui.Start_Button.setStyleSheet("")
            pass
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

        self.set_measure_data(f"U_{str(int(measure_data[2]))}_I_0_N_0",
                              str(measure_data[4][0]))

        self.set_measure_color_ext(f"U_{str(int(measure_data[2]))}_I_0_N_0",
                                   measure_data[5][0])

        self.set_measure_data(f"U_{str(int(measure_data[2]))}_I_100_N_0",
                              str(measure_data[4][1]))
        self.set_measure_color_ext(f"U_{str(int(measure_data[2]))}_I_100_N_0",
                                   measure_data[5][1])

        self.set_measure_data(f"U_{str(int(measure_data[2]))}_I_200_N_0",
                              str(measure_data[4][2]))
        self.set_measure_color_ext(f"U_{str(int(measure_data[2]))}_I_200_N_0",
                                   measure_data[5][2])

        self.set_measure_data(f"U_{str(int(measure_data[2]))}_I_300_N_0",
                              str(measure_data[4][3]))
        self.set_measure_color_ext(f"U_{str(int(measure_data[2]))}_I_300_N_0",
                                   measure_data[5][3])

        self.set_measure_data(f"U_{str(int(measure_data[2]))}_I_400_N_0",
                              str(measure_data[4][4]))
        self.set_measure_color_ext(f"U_{str(int(measure_data[2]))}_I_400_N_0",
                                   measure_data[5][4])

        self.set_measure_data(f"U_{str(int(measure_data[2]))}_I_500_N_0",
                              str(measure_data[4][5]))
        self.set_measure_color_ext(f"U_{str(int(measure_data[2]))}_I_500_N_0",
                                   measure_data[5][5])

        self.set_measure_data("auto_tab_DT_num", str(int(measure_data[0])))
        self.set_measure_data("u_supply_sens", str(float(measure_data[2])))
        self.set_measure_data("current_sens", str(float(measure_data[3])))



