
from django.shortcuts import render
from django.http import StreamingHttpResponse,HttpResponse
import os
import sys
import cv2


BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)
import ImgStream 
import Thread_Contral
from Run_Demo import run_demo

DEMO_DIR = os.path.join(BASE_DIR, '../ttnet/src/results/demo/ttnet/frame')


def show_demo(request):
    ImgStream.init_img_stream()  
    return StreamingHttpResponse(gen_display(), content_type='multipart/x-mixed-replace; boundary=frame')
 

def gen_display_test(): 
    print('data null')
    data = cv2.imread(os.path.join(BASE_DIR,'./waiting.jpg'))
    data = cv2.imencode('.jpg', data)[1]
    yield (b'--frame\r\n'
            b'Content-Type: image/jpg\r\n\r\n' + data.tobytes() + b'\r\n'
            # b'--frame\r\n'
            # b'Content-Type: application/json\r\n\r\n' + b'hello' + b'\r\n'
        )
    
def gen_display_test2(): 
    while True:
        print('data null')
        data = cv2.imread(os.path.join(BASE_DIR,'./waiting.jpg'))
        data = cv2.imencode('.jpg', data)[1]
        yield (b'--frame\r\n'
                b'Content-Type: image/jpg\r\n\r\n' + data.tobytes() + b'\r\n'
                # b'--frame\r\n'
                # b'Content-Type: application/json\r\n\r\n' + b'hello' + b'\r\n'
        )
 
def gen_display(): 
    while True:
        data = ImgStream.get_img_from_stream()
        if data is not None:
            data = cv2.imencode('.jpg', data)[1] 
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpg\r\n\r\n' + data.tobytes() + b'\r\n')
        else:
            print('data null')
            data = cv2.imread('./waiting.jpg').imencode('.jpg', data)[1]
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpg\r\n\r\n' + data.tobytes() + b'\r\n')
            

def init(request):
    if request.method == 'GET':
        Thread_Contral.set_thread_break()
        return HttpResponse("init successfully")
    else:
        return HttpResponse("error")

def control(request):
    if request.method == 'GET':
        Thread_Contral.set_thread_control()
        return HttpResponse("init successfully")
    else:
        return HttpResponse("error")