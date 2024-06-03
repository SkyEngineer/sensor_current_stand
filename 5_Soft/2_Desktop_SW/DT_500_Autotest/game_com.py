import serial.tools.list_ports


def read_data_com(ser):
    data_in = []
    byte_in = None
    data_in_str = None

    while (byte_in != b'\n'):
        byte_in = ser.read(1)
        data_in.append(byte_in.decode())
    data_in_str = ''.join(data_in)

    print(data_in_str)
    return data_in_str

if __name__ == '__main__':
    out = []
    ports = serial.tools.list_ports.comports()

    ser_stand = serial.Serial("COM8",
                                baudrate=9600,
                                timeout=100)
    ser_supply_sensor = serial.Serial("COM6",
                                      baudrate=115200,
                                      timeout=100)
    ser_supply_current = serial.Serial("COM10",
                                      baudrate=115200,
                                      timeout=100)

    try:
        while True:
            data_rx_ser_stand = ser_stand.read(1)

            if (data_rx_ser_stand == b'\xaa'):
                ser_stand.write(bytes([0xBB]))
            print ("2222")
            data_rx_ser_supply_sensor = read_data_com(ser_supply_sensor)
            if "*IDN?" in data_rx_ser_supply_sensor:
                ser_stand.write("GW INSTEK,GPP-74323".encode())

            # read_data_com(ser_supply_current)


    except:
        print("End")

            # ser_stand.write(bytes([0xAA]))
            # byte_in = ser.read(1)
            # if byte_in == b'\xbb':
            #     out = ["port_stand", port]
