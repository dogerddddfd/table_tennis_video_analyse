from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse

# Test类，类名要使用大驼峰方式书写
class Ping(APIView):
    # 该api接受GET方式的请求，如果需要接受POST方式的请求，则改为def post(self, request):
    def get(self, request):
        # 在python中定义一个变量的时候不需要任何类型前缀。这是python最直观的优点之一。
        # python变量名规则和大部分语言不同，它是有下划线连接的小写英文字母/单词组成，而不是其他语言比如C#和Java中使用的小驼峰规则。
        response_object = {
            'text': "ping",
            'content': "ping successfully"
        }
        # 返回一个Json格式的内容。JsonResponse会自动把各种类型的对象转化为Json格式，除非某种类型的对象本身在逻辑上就无法转换为Json格式。
        return JsonResponse(response_object, safe=False)