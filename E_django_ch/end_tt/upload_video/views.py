from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse,HttpResponse
import os

BASE_DIR = os.path.dirname(__file__)
CHUCK_DIR = os.path.join(BASE_DIR, '../videos/temporary')

@csrf_exempt
def upload(request):
   if request.method == 'POST':
      # file_name = request.POST.get('filename')
      file_name = 'user_video.mp4'
      _hash = request.POST.get('hash')
      chunk = request.FILES['chunk']

      chunk_path = os.path.join(CHUCK_DIR, str(_hash))
      if not os.path.exists(CHUCK_DIR):
         os.makedirs(CHUCK_DIR)
      with open(chunk_path, 'wb+') as destination:
         for chunk in chunk.chunks():
            destination.write(chunk)

      return HttpResponse('切片'+_hash+'上传成功')
   else: 
      return HttpResponse("error")


def merge(request):
   if request.method == 'GET':
      # filename = request.GET.get('filename')
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
      return HttpResponse('合并成功')
   else: 
      deldir(CHUCK_DIR)
      return HttpResponse("error")
   

def init(request):
   if request.method == 'GET':
      if os.path.exists(CHUCK_DIR):
         deldir(CHUCK_DIR)
      return HttpResponse("init success")
   else:
      return HttpResponse("error")


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
