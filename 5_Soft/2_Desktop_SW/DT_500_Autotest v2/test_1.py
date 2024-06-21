import serial.tools.list_ports
import time
import pyvisa

if __name__ == '__main__':
    ser_supply_sensor = serial.Serial("COM4",
                                           baudrate=115200,
                                           timeout=100)
    ser_measure_supply = serial.Serial("COM6",
                                            baudrate=115200,
                                            timeout=100)
    visa_voltmeter = pyvisa.ResourceManager().open_resource("USB0::0xF4EC::0x1201::SDM35HBQ7R1075::INSTR AKIP-2101")

    ser_stand = serial.Serial("COM3",
                                   baudrate=9600,
                                   timeout=100)

    ser_stand.write(bytes([0xFF]))
    time.sleep(0.1)
    ser_stand.write(bytes([9]))
    time.sleep(0.1)

    ser_supply_sensor.write(f"VSET1:0\n".encode())
    time.sleep(0.1)

    ser_supply_sensor.write("OUTP1:STAT ON\n".encode())
    time.sleep(0.1)



