# chat/consumers.py
import json
import os
import json

from channels.generic.websocket import AsyncWebsocketConsumer

BASE_DIR = os.path.dirname(__file__)
CHUCK_DIR = os.path.join(BASE_DIR, '../videos/temporary')

class UploadConsumer(AsyncWebsocketConsumer):
    def __init__(self) -> None:
        super().__init__()
        self.hash = None
        self.chunks_length = None
        self.chunk_count = 0

    async def connect(self):
        init()
        print('connect')
        await self.accept()

    async def disconnect(self, close_code):
        print('disconnect')
        init()

    async def receive(self,text_data=None, bytes_data=None):
        if text_data is not None:
            print(text_data)
            data = json.loads(text_data)
            self.hash = data['hash']
            if self.chunks_length is None:
                self.chunks_length = data['length']

        if(bytes_data is not None):
            chunk_path = os.path.join(CHUCK_DIR, str(self.hash))
            if not os.path.exists(CHUCK_DIR):
                os.makedirs(CHUCK_DIR)
            with open(chunk_path, 'wb+') as destination:
                destination.write(bytes_data)
            self.chunk_count += 1
            print('@@@@@@@@@@@@@')

        if(self.chunks_length == self.chunk_count):
            file_name = 'user_video.mp4'
            all_chunk = os.listdir(CHUCK_DIR)
            all_chunk.sort(key=lambda x: int(x))
            target_file_path = os.path.join(BASE_DIR, '../videos/'+file_name)
            with open(target_file_path, "wb+") as f:
                for chunk in all_chunk:
                    chunk_path = os.path.join(CHUCK_DIR, chunk)
                    with open(chunk_path, "rb") as g:
                        data = g.read()
                        f.write(data)
            deldir(CHUCK_DIR)
            await self.close()


def deldir(dir):
    if not os.path.exists(dir):
        return False
    if os.path.isfile(dir):
        os.remove(dir)
        return
    for i in os.listdir(dir):
        t = os.path.join(dir, i)
        if os.path.isdir(t):
            deldir(t)#重新调用次方法
        else:
            os.unlink(t)
    os.removedirs(dir)#递归删除目录下面的空文件夹

def init():
    if os.path.exists(CHUCK_DIR):
        deldir(CHUCK_DIR)