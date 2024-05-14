import com_ports
from PyQt6 import QtWidgets, uic
import power_supply_sensor
import power_supply_measure
import voltmeter

# info
# Питание датчиков тока     GPP-74323           Источник питания
# Измерение показаний       АКИП-2101/1         Вольтметр
# АКИП 1162-10-1020	Источник постоянного тока
# АКИП-1162-10-510	Источник постоянного тока

# питание датчика 16...32 В
# Диапазон тока измеряемого: 0...500 А
# Номинальное выходное напряжение: 4 В

# Напряжение питания, В	27
# Ток потребления,  мА, не более	40
# Выходное напряжение покоя, В, не более	0,1
# Выходное напряжение при номинальном входном токе, В	от 3,6 до 4,1

class MyWindow (QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        Form, Base = uic.loadUiType("ui/DT_500_Autotest.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        # заливаем окна со значениями напряжения белым цветом и черным текстом
        self.set_measure_U_syle()

        # по умолчанию делаем отчет
        self.ui.get_doc.setChecked(1)

    # заливаем окна со значениями напряжения белым цветом и черным текстом
    def set_measure_U_syle(self):
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

    def set_console_text(self):
        for item in self.ui.centralwidget.findChildren(QtWidgets.QTextBrowser):
            if "console" == item.objectName():
                item.setStyleSheet(f"color: black; background-color: white")
                item.setText("Test")

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow(None)

    # эксперименты
    # поиск нужного виджета!!!!
    window.set_measure_data("U_27_I_200_N_1", 12.3)
    window.set_measure_color("U_27_I_200_N_1", "red")
    window.set_measure_color("U_16_I_0_N_1", "green")
    window.set_console_text()

    print("dfgdfg")
    # for forms in list(window.ui):
    #     if "U_16_I_0_N_1" in forms:
    #         print("sdf")
    #         # window.ui + forms.setText(str(12))


    window.show()
    sys.exit(app.exec())


    # coms = com_ports.Com_Ports()
    # coms.search_ports()

    # алгоритм включения
    # 1. при нажатии на кнопку "Поиск и подключение" ищем порты, подключаемся настраиваем аппаратуру. Для этого  class Com_Ports(object):
    # 2. при нажатии на кнопку "Запуск теста" выполняем тестирование последовательное
    # 3. при нажатии на кнопку "Остановка теста" выполняем полную остановку тестирования последовательное
    # 4. если галочка сформировать отчет стоит -формируем




