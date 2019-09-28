#first connect with given bt adress
#connect to slave in our case DK
#
import BluetoothController


class BluetoothController(object):
    target_name = "DK5031"
    target_address = "98:D3:32:11:82:5A"
    nearby_devices = None
    is_connected = False
    port = 1
    sock = None
    prevCommand = ""
    command = "s"

    @staticmethod
    def connect():
        print 'Bluetooth Controller Searching for devices... '
        nearby_devices = BluetoothController.discover_devices()
        print nearby_devices
        for bluetooth_address in nearby_devices:
            if BluetoothController.target_address == bluetooth_address:
                BluetoothController.is_connected = True
                BluetoothController.target_address = bluetooth_address
                if BluetoothController.target_address is not None:
                    print "Bluetooth Controller  found target with address ", BluetoothController.target_address
                    BluetoothController.connect_to_slave()

                else:
                    print "could not find target bluetooth device nearby"
                break

    @staticmethod
    def connect_to_slave():

        BluetoothController.sock = BluetoothController.BluetoothSocket(BluetoothController.RFCOMM)
        print "wait connecting...."
        BluetoothController.sock.connect((BluetoothController.target_address, BluetoothController.port))
        print"conneceted"

    @staticmethod
    def disconnect():
        BluetoothController.sock.close()

    @staticmethod
    def send_command(command, message=None):

        if message == None:
            print "Sent command " + command
        else:
            print message
        if BluetoothController.is_connected == True:
            BluetoothController.sock.send(command)
            BluetoothController.prevCommand = command
        return



if __name__ == '__main__':
    command = "s"
    BluetoothController.connect()

    while True:
        command = raw_input("Enter command: ")
        print " ..... " + command
        # BluetoothController.command = command
        if (command == "Q"):
            BluetoothController.send_command('S')
            BluetoothController.sock.close()
            break

        else:
            BluetoothController.send_command(command)
