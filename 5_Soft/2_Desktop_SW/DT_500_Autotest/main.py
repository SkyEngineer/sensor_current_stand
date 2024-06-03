import com_ports
from PyQt6 import QtWidgets


import window_qt


if __name__ == '__main__':
    import sys
    # запуск приложения оконного
    app = QtWidgets.QApplication(sys.argv)
    window = window_qt.MyWindow()

    window.show()
    sys.exit(app.exec())


