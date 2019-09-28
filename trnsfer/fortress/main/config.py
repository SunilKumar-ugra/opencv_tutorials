import cv2
class Config(object):
    cam=0
    status="demo" #demo/cam
    input_image=cv2.imread("demo_input.png")
    demo_arena=cv2.imread("arena.png")
