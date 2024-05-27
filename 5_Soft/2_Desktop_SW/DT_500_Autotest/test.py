import serial.tools.list_ports
import time
import doc_make

if __name__ == '__main__':
    ports = serial.tools.list_ports.comports()
    ser = serial.Serial(ports[0].device,
                        baudrate=9600,
                        timeout=100)
    ser.write(bytes([0xAA]))
    data_in = ser.read(2)
    print(hex(data_in[0]),hex(data_in[1]))

    time.sleep(0.1)

    # ser.write(bytes([0xFF]))
    # print(ser.read(2)[0])

    for i in range(1,33):
        ser.write(bytes([i]))

        if ser.read(2)[0] == 0xcc:
            time.sleep(0.5)

    ser.write(bytes([0xFF]))

    ser.close()

    # report_excel = doc_make.Doc_Report()
    # report_excel.make_report_excel()
