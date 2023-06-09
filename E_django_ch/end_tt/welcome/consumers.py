# chat/consumers.py
import json

from channels.generic.websocket import WebsocketConsumer


class PingConsumer(WebsocketConsumer):
    def connect(self):
        print('connect')
        self.accept()

    def disconnect(self, close_code):
         print('disconnect')

    def receive(self, text_data):
        # print('receive') 
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.send(text_data=json.dumps({"message": message}))