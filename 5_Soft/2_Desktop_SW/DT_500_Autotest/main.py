import com_ports
from PyQt6 import QtWidgets

import doc_make
import window_qt


if __name__ == '__main__':
    import sys
    # запуск приложения оконного
    app = QtWidgets.QApplication(sys.argv)
    window = window_qt.MyWindow()
    # объект файла дял создания отчёта
    report_excel = doc_make.Doc_Report()

    # эксперименты
    window.set_measure_data("U_27_I_200_N_1", 12.3)
    window.set_measure_color("U_27_I_200_N_1", "red")
    window.set_measure_color("U_16_I_0_N_1", "green")

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

