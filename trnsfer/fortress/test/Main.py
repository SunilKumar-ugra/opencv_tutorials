from BotController import Bot
from BluetoothController import BluetoothController
import Process

#while True:
Bot.traversePath(Process.getThePath())
newPath = Process.getThePath().reverse()
Bot.traversePath(newPath)