# chat/consumers.py
import json
import os
import sys
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer

BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)
import ImgStream
import Thread_Contral
from Run_Demo import run_demo 

import threading
 
class ShowDemoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'aaa'
        self.room_group_name = 'video_%s' % self.room_name

        Thread_Contral.set_thread_running()
        Thread_Contral.get_thread_status()
        ImgStream.init_img_stream()
        print('connect') 
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()  

    async def disconnect(self, close_code):
        Thread_Contral.set_thread_break()
        Thread_Contral.get_thread_status()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('disconnect')  

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data['flag'] == 'START':
            print(data)
            run_demo(data['filename'])
            # self.async_sendImg()
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sendImg',
                'message': text_data,
            }
        )
        await self.send(text_data=json.dumps({"message": 'hello'}))


    def async_sendImg(self):
        t = threading.Thread(target=self.sendImg,)
        t.start()

    async def sendImg(self):
        while Thread_Contral.get_thread_status() == 'RUN':
            img = ImgStream.get_img_from_stream()
            if img is not None:
                print('@@@@@')
                await self.send(text_data=json.dumps({"message": 'hello'}))
