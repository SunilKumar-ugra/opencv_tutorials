import ast
from BotController import Bot
from BluetoothController import BluetoothController
from Frame import Frame
while BluetoothController.is_connected == False:
    BluetoothController.connect()
Frame.connect(1)
fil=open("path.txt","r")
dat=ast.literal_eval(fil.read())
res=dat[0]

path=dat[1]
print path
path.append(path[0])
cleared_path=[]
for i,point in enumerate(path):
    if i <len(path)-1:
        if path[i]==path[i+1]:
            continue
        else:
            cleared_path.append(point)

cleared_path.append(cleared_path[0])

fil.close()

print cleared_path
print res
Bot.traverse_new(res,cleared_path)














