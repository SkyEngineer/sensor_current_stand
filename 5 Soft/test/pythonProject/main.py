import usb.core
from usb.backend import libusb1

# it should find libusb-1.0.dll at our path variable
back = libusb1.get_backend()
print(type(back))  # return: <class 'usb.backend.libusb1._LibUSB'>

dev = usb.core.find(backend=back)
print(type(dev))  # return: <class 'usb.core.Device'>

# flag 'find_all=True' would return generator
# reprecent connected usb devices

# dev_list = usb.core.find(find_all=True, backend=back)
dev_list = usb.core.find(idVendor=0x046d, backend=back)
print(type(dev_list)) # return: <class 'generator'>

for i, data in enumerate(dev_list):
    print(str(i) + "\n")
    print(data)

#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     # находим наше устройство
#     dev = usb.core.find(idVendor=0xfffe, idProduct=0x0001)
#
#     # оно было найдено?
#     if dev is None:
#         raise ValueError('Device not found')