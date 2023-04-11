from django.shortcuts import render
from django.http import StreamingHttpResponse,HttpResponse
from easydict import EasyDict as edict
import os
import sys
import threading

import cv2


BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(BASE_DIR,'../ttnet/src'))

from config.config import parse_configs
from demo import demo


def run_demo(request):
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
   configs.video_path=os.path.join(BASE_DIR,'../videos/test_1.mp4') 
   configs.save_demo_output=True
   configs.show_image=True

   configs = parse_configs(configs)

   is_demo_running = True
   t = async_demo(configs,request)
   print('---------------demo_running--------------------')
   
   return HttpResponse('---------------demo_running--------------------')



def async_demo(configs,request):
   t = threading.Thread(target=demo,kwargs={'configs':configs})
   t.start()
   return t