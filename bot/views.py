from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from telegram import Bot
from django.conf import settings
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from .decorator import *
from .models import *
import json
@authenticated
def log_in(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request=request,username=username,password=password)
    if user:
        login(request,user)
        return redirect('index')
    context = {}
    return render(request,'authentication-signin.html',context)
def log_out(request):
    user=request.user
    if user:
        logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    return render(request,'index.html',{})


@login_required(login_url='login')
def alternate(request):
    return render(request,'alternate.html',{})

@login_required(login_url='login')
def orders(request):
    orders=Order.objects.all()
    orders=orders.order_by('-date')
    orders=orders.filter(status=True,disable=False)

    d=[]
    for i in orders:
        ordd=OrderDetail.objects.filter(order=i)
        summ=0
        for j in ordd:
            summ+=j.totalprice
        k={
            "id":i.id,
            "phone":i.phone,
            "name":i.name,
            "username":i.username,
            "day":i.day,
            "time":i.time,
            "status":i.order_status,
            "sum":summ,
            "region":i.region,
            "district":i.district,
            "payment_made":i.payment_made,
            "payment_type":str(i.payment_type)
        }
        d.append(k)
    context = {
        'orders': d,
    }
    print(orders)
    return render(request,'ecommerce-orders.html',context)



def sendmessage(request):
    data = json.loads(request.body)
    print(data)
    ordd = OrderDetail.objects.filter(order=int(data['id']))
    d=[]
    for i in ordd:
        k={
            "id":i.id,
            "name_uz":i.name_uz,
            "name_ru":i.name_ru,
            "quantity":i.quantity,
            "price":i.price,
            "totalprice":i.totalprice,
        }
        d.append(k)
    return JsonResponse({'ordds':d})
    

@login_required(login_url='login')
def widgets(request):
    return render(request,'widgets.html',{})

@login_required(login_url='login')
def products(request):
    return render(request,'ecommerce-products.html',{})

@login_required(login_url='login')
def productdetail(request):
    return render(request,'ecommerce-products-details.html',{})


@login_required(login_url='login')
def addproducts(request):
    return render(request,'ecommerce-add-new-products.html',{})


def getorderstatus(request):
    data = json.loads(request.body)
    ord = Order.objects.get(id=int(data['id']))
    return JsonResponse({'status':ord.order_status})

def disableorder(request):
    data = json.loads(request.body)
    ord = Order.objects.get(id=int(data['id']))
    ord.disable=True
    ord.save()
    return JsonResponse({})




def changeorderstatus(request):
    data = json.loads(request.body)
    print(data)
    ord=Order.objects.get(id=int(data['id']))
    ord.order_status=data['status']
    ord.save()
    bot = Bot(token=settings.TOKEN)
    if data['status']=="REFUSAL":
        if ord.user.lang=='uz':
            text = "Buyutma bekor qilindi😔"
        else:
            text = 'Заказ был отменен😔'
        bot.sendMessage(chat_id=ord.user.chat_id, text=text ) 
    if data['status']=="PARTIALLY SHIPPED":
        if ord.user.lang=='uz':
            text = f'''Buyurtma jo'natildi🚚'''
        else:
            text = f'''Заказ был отправлен🚚'''
        bot.sendMessage(chat_id=ord.user.chat_id, text=text ) 
    if data['status']=="FULFILLED":
        if ord.hatchback==False:
            ord.hatchback=True
            ord.save()
            ordd=OrderDetail.objects.filter(order=ord)
            summ=0
            for i in ordd:
                summ+=i.totalprice
            user=TelegramUser.objects.get(id=ord.user.id)
            user.wallet+=summ*0.03
            user.save()
            if user.suggested!=0:
                freind=TelegramUser.objects.get(id=user.suggested)
                freind.wallet+=summ*0.01
                freind.save()
            
        if ord.user.lang=='uz':
            text = f'''№:{ord.id}
Bizning xizmatimizga baho bering🤩'''
        else:
            text = f'''№:{ord.id}
Оцените наш сервис🤩'''
        keys=[
        [InlineKeyboardButton("⭐️⭐️⭐️⭐️⭐️",callback_data=str("evaluation_5"))],
        [InlineKeyboardButton("⭐️⭐️⭐️⭐️",callback_data=str("evaluation_4"))],
        [InlineKeyboardButton("⭐️⭐️⭐️",callback_data=str("evaluation_3"))],
        [InlineKeyboardButton("⭐️⭐️",callback_data=str("evaluation_2"))],
        [InlineKeyboardButton("⭐️",callback_data=str("evaluation_1"))],
        ]
        markup = InlineKeyboardMarkup(keys)
        bot.sendMessage(chat_id=ord.user.chat_id, text=text,reply_markup=markup ) 
    return JsonResponse({})








