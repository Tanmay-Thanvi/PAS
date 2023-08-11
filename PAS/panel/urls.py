from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('select_batch/',select_batch_fn,name="select_batch"),
    path('assesment/<str:pk>/<str:pk_1>/',assesment,name="assesment"),
    path('get_info/',get_info,name='get_info'),
]
