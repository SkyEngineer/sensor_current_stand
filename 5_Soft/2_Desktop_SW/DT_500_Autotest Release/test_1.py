import serial.tools.list_ports
import time
import pyvisa
import doc_make

if __name__ == '__main__':
    rep = doc_make.Doc_Report()

    measure_data = ["010", "статус", "Uпит", "Iпит",
                    ["Uизм(0А)", "Uизм(100А)", "Uизм(200А)", "Uизм(300А)", "Uизм(400А)", "Uизм(500А)"]]

    # rep.make_report_excel(measure_data, time.strftime("Протоколы\Протокол от %d.%m.%Y в %H_%M_%S.xlsx"))
    rep.make_report_excel(measure_data, time.strftime("Протоколы\Протокол от 24.06.2024 в 13_52_07.xlsx"))



