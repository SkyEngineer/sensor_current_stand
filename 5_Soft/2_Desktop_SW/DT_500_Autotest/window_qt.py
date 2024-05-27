from PyQt6 import QtCore, QtWidgets, uic
import testing_thread_qt

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

        # кнопки
        self.ui.Connect_Button.clicked.connect(self.btn_connect_click)
        self.ui.Start_Button.clicked.connect(self.btn_start_click)

        # поток тестирования
        self.mythread = testing_thread_qt.MyThread()
        # self.mythread.started.connect(self.set_console_text)
        # self.mythread.finished.connect(self.set_console_text)
        self.mythread.mysignal_status.connect(self.set_console_text, QtCore.Qt.ConnectionType.QueuedConnection)

        self.dict_com_ports = {"stand": None,
                          "power_sensor": None,
                          "power_current": None,
                          "voltmeter": None,}

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
        # self.dict_com_ports = com_ports.Com_Ports.search_ports()

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