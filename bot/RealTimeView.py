from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from threading import Timer
import json 
import time
import threading

from bot.models import *

key = 0 
class RTWieW(WebsocketConsumer):
    def get_order(self):
        return Order.objects.all()
    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name
        self.room_name = 'event'
        self.room_group_name = self.room_name+"_sharif"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.timer = Timer(1, self.receive)
        self.timer.start()
        print("#######CONNECTED############")

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("DISCONNECED CODE: ",code)

    def receive(self):
        for i in range(10000000000000000):
            orders=Order.objects.all()
            orders=orders.order_by('-date')
            orders=orders.filter(status=True,disable=False)
            d=[]
            for i in orders:
                ordd=OrderDetail.objects.filter(order=i)
                summ=0
                for j in ordd:
                    summ+=j.totalprice
                d.append({
                        "id":i.id,
                        "phone":str(i.phone),
                        "name":i.name,
                        "username":i.username,
                        "day":str(i.day),
                        "time":str(i.time),
                        "status":i.order_status,
                        "sum":summ,
                        "region":i.region,
                        "district":i.district,
                        "payment_made":i.payment_made,
                        "payment_type":str(i.payment_type)
                })
            data=json.dumps(d)
            self.send(data)
            time.sleep(5)






        