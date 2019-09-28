import numpy as np
import cv2
import ImageProcess
from ImageProcess import Frame
from time import sleep

import bluetooth

target_name = "HC-06"
target_address = "20:16:08:17:06:73"

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print "found target bluetooth device with address ", target_address
else:
    print "could not find target bluetooth device nearby"

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print "Bluetooth Controller  >> Connecting to Slave...."
sock.connect((target_address, 1))

while True:
    command = raw_input("Enter command: ")
    print " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + command
    sock.send(command)
    sleep(1)
