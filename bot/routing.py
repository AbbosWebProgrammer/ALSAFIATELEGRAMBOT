from asyncio import windows_utils
from django.urls import path
from .RealTimeView import RTWieW
ws_urlpatterns=[
path('ws/real_data/',RTWieW.as_asgi())
]