from django.shortcuts import render
from django.http import StreamingHttpResponse,HttpResponse
from easydict import EasyDict as edict
import os
import sys
import threading
import cv2
import time 

import Thread_Contral

BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(BASE_DIR,'../ttnet/src'))

from config.config import parse_configs
from demo import demo
import ImgStream

def run_demo(request):
   if request.method == 'GET':
      ImgStream.init_img_stream()
      file_name = request.GET.get('filename')
      print(file_name)
      ttnet_src_path=os.path.join(BASE_DIR,'../ttnet/src')
      configs = edict()
      configs.gpu_idx=0
      configs.working_dir=ttnet_src_path
      configs.arch='ttnet' 
      configs.pretrained_path=ttnet_src_path
      configs.pretrained_path=os.path.join(ttnet_src_path,'../checkpoints/ttnet/ttnet_best.pth')
      configs.seg_thresh=0.5 
      configs.event_thresh=0.5
      configs.thresh_ball_pos_mask=0.05
      configs.video_path=os.path.join(BASE_DIR,'../videos',file_name) 
      configs.save_demo_output=True
      configs.show_image=True

      configs = parse_configs(configs)

      
      Thread_Contral.set_thread_running()
      print('---------------demo before run--------------------')
      async_run_demo(configs)
      print('---------------demo running--------------------')
      # time.sleep(10)
      # Thread_Contral.set_thread_stop()
      print('---------------http send--------------------')

      return HttpResponse("runing demo")
   else:
      return HttpResponse("error")


def async_run_demo(configs):
   t = threading.Thread(target=demo,kwargs={'configs':configs})
   t.start()


