from django.urls import path
from . import views
from . import Run_Demo

urlpatterns = [
    # Test接口地址，注意第一个参数，即url地址，是区分大小写的
    path('img', views.show_demo),
    path('init/', views.init),
    path('control/', views.control),
    path('run_demo/', Run_Demo.run_demo),
]