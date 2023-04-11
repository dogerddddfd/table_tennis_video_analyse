from django.urls import path
from . import views

# 路由列表
urlpatterns = [ 
    # Test接口地址，注意第一个参数，即url地址，是区分大小写的
    path('ping/', views.Ping.as_view(), name='Test'),
]