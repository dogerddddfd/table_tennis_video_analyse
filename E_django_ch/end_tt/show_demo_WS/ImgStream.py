import queue
import threading
import os
import numpy as np

import cv2

BASE_DIR = os.path.dirname(__file__)
DEMO_DIR = os.path.join(BASE_DIR, '../ttnet/src/results/demo/ttnet/frame')


class ImgStream:
    queue_image = queue.Queue(maxsize=3)

    def __init__(self):
        pass

    def get_img(self, img):
        if self.queue_image.full():
            # 队列满，队头出队
            self.queue_image.get()
            # 队尾添加数据
            self.queue_image.put(img)
        else:
            # 队尾添加数据 
            self.queue_image.put(img)

    def send_img(self):
        return self.queue_image.get()


def init_img_stream():
   global img_stream
   img_stream = None
   img_stream = ImgStream()


def send_img_to_stream(img):
    print('send img to stream')
    img_stream.get_img(img)
    


def get_img_from_stream():
    return img_stream.send_img()

