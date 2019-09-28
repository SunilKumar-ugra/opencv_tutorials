from BotController import Bot
from BluetoothController import BluetoothController
import process
#while True:
Bot.traversePath(process.getThePath())
newPath = process.getThePath().reverse()
Bot.traversePath(newPath)
