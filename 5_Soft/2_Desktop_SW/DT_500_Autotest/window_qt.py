from PyQt6 import QtCore, QtWidgets, uic
import testing_thread_qt
import com_ports

# класс отображения окна
class MyWindow (QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        Form, Base = uic.loadUiType("ui/DT_500_Autotest.ui")
        self.ui = Form()
        self.ui.setupUi(self)

        # заливаем окна со значениями напряжения белым цветом и черным текстом
        self.set_measure_U_style()
        # по умолчанию делаем отчет
        self.ui.get_doc.setChecked(1)

        self.ports = com_ports.Com_Ports()

        # кнопки
        self.ui.Connect_Button.clicked.connect(self.btn_connect_click)
        self.ui.Start_Button.clicked.connect(self.btn_start_click)

        # поток тестирования


        self.dict_com_ports = None

    # заливаем окна со значениями напряжения белым цветом и черным текстом
    def set_measure_U_style(self):
        for item in self.ui.centralwidget.findChildren(QtWidgets.QLineEdit):
            if "U_" in item.objectName():
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

    def clear_measure_data(self):
        pass
        # for item in self.ui.centralwidget.findChildren(QtWidgets.QLineEdit):
        #     if name_widget == item.objectName():
        #         item.setText(str(data))

    def set_console_text(self, text_data):
        for item in self.ui.centralwidget.findChildren(QtWidgets.QTextBrowser):
            if "console" == item.objectName():
                item.setStyleSheet(f"color: black; background-color: white")
                # item.setText(text_data + "\n")
                item.append(text_data)

    # Подключение приборов
    def btn_connect_click(self):
        self.set_console_text("Поиск аппаратуры...")
        port_stend = self.ports.search_stand()
        print(port_stend[0], port_stend[1])

        port_instek = self.ports.search_instek(port_stend[1])
        print(port_instek[0], port_instek[1])

        port_measure_supply = self.ports.search_measure_supply(stand_port=port_stend[1],
                                                                instek_port= port_instek[1])
        print(port_measure_supply[0], port_measure_supply[1])

        port_visa_voltmeter = self.ports.search_visa_voltmeter()
        print(port_visa_voltmeter[0], port_visa_voltmeter[1], port_visa_voltmeter[2])

        self.dict_com_ports = {"port_stend": port_stend,
                               "port_instek": port_instek,
                               "port_measure_supply": port_measure_supply,
                               "port_visa_voltmeter": port_visa_voltmeter}


        # установить значения
        self.set_measure_data("port_stand", port_stend[1])
        self.set_measure_data("port_supply_sensor", port_instek[1])
        self.set_measure_data("port_measure_supply", port_measure_supply[1])
        self.set_measure_data("port_voltmeter", port_visa_voltmeter[2])

        self.set_console_text("Поиск аппаратуры завершен")

        self.mythread = testing_thread_qt.MyThread()
        # self.mythread.started.connect(self.set_console_text)
        # self.mythread.finished.connect(self.set_console_text)
        self.mythread.mysignal_status.connect(self.set_console_text, QtCore.Qt.ConnectionType.QueuedConnection)

    # старт тестирования
    def btn_start_click(self):
        if self.ui.Start_Button.text() == "Старт":
            self.set_console_text("Начало тестирования...")
            self.ui.Start_Button.setText("Стоп")
            self.ui.Start_Button.setStyleSheet(f"color: black; background-color: red")
            #     старт тестирования
            self.mythread.start(self.dict_com_ports)


        else:
            self.ui.Start_Button.setStyleSheet("")
            #     останов тестирования
            print(self.mythread.isRunning())
            self.mythread.running = False
            self.mythread.wait(500)
            self.set_console_text("Остановка тестирования...")
            self.ui.Start_Button.setText("Старт")
            print(self.mythread.isRunning())