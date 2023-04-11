from django.shortcuts import render
from django.http import StreamingHttpResponse
import os
# import cv2

BASE_DIR = os.path.dirname(__file__)

def get_video_stream(request):
    file_name = request.GET.get('video')
    response = StreamingHttpResponse(file_itrator(file_name))
    response['content_type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
    return response


def file_itrator(file_name):
    file_path = os.path.join(BASE_DIR, '../videos/',file_name)

    chunk_size = 8192  # 每次读取的片大小
    with open(file_path, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


