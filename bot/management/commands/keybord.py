from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import ReplyKeyboardMarkup,KeyboardButton,InputMediaPhoto
from .uzbekiston import  *

from bot.models import Category, Product,Branche
def language_reply_markup():
    markup=ReplyKeyboardMarkup(
    [
        ["O'zbek 🇺🇿",'Русский 🇷🇺']
    ],
    resize_keyboard=True)
    return markup
def language_reply_markup_uz():
    markup=ReplyKeyboardMarkup(
    [
        ["O'zbek 🇺🇿",'Русский 🇷🇺'],
            ['Bosh Sahifa 🏠']

    ],
    resize_keyboard=True)
    return markup
def language_reply_markup_ru():
    markup=ReplyKeyboardMarkup(
    [
        ["O'zbek 🇺🇿",'Русский 🇷🇺'],
            ['Главное Меню 🏠']

    ],
    resize_keyboard=True)
    return markup

def contact_reply_markup_uz():
    keyboard = KeyboardButton("Raqamimni jo'natish 📲", request_contact=True)
    markup = ReplyKeyboardMarkup([[keyboard]],one_time_keyboard=True,resize_keyboard=True)
    return markup

def contact_reply_markup_ru():
    keyboard = KeyboardButton('Отправить мой номер 📲', request_contact=True)
    markup = ReplyKeyboardMarkup([[keyboard]],one_time_keyboard=True,resize_keyboard=True)
    return markup

def main_menu_reply_markup_uz():
    markup=ReplyKeyboardMarkup(
    [           ["🛍 Katalog 🛍"],
        ["Savatcha 🛒",'Aksiyalar 🎁'],
        ["Buyurtmalarim 📂",'Biz haqimizda ℹ️'],
              ["Mening Hamyonim 💰"],
        ['Sozlamalar ⚙️','Yordam ‼️']
    ],
    resize_keyboard=True)
    return markup

def main_menu_reply_markup_ru():
    markup=ReplyKeyboardMarkup(
    [         ["🛍 Каталог 🛍"],
        ["Корзина 🛒",'О нас ℹ️'],
      ["Мои заказы 📂",'Акции 🎁'],
              ["Мой Кошелёк 💰"],
       ['Настройки ⚙️','Помощь ‼️']
    ],
    resize_keyboard=True)
    return markup

def about_us_reply_markup_uz():
    keys=[[
        InlineKeyboardButton(text="Instagram 📸", url=f'''https://instagram.com/alsafia_uz?utm_medium=copy_link'''),
        InlineKeyboardButton(text="Kanal 💬", url=f'''https://t.me/alsafiauz''')
    ],
    [
        InlineKeyboardButton("Manzil 📍",url=f'''https://yandex.uz/maps/-/CCU5ZVu~~D'''),
        InlineKeyboardButton(text="Bog'lanish 👨🏻‍💻", url=f'''https://t.me/alsafia_manager''')
    ]]
    markup = InlineKeyboardMarkup(keys)
    return markup

def about_us_reply_markup_ru():
    keys=[[
        InlineKeyboardButton(text="Инстаграм 📸", url=f'''https://instagram.com/alsafia_uz?utm_medium=copy_link'''),
        InlineKeyboardButton(text="Канал 💬", url=f'''https://t.me/alsafiauz''')
    ],[
        InlineKeyboardButton("Адрес 📍",url=f'''https://yandex.uz/maps/-/CCU5ZVu~~D'''),
        InlineKeyboardButton(text="Связаться 👨🏻‍💻", url=f'''https://t.me/alsafia_manager''')
    ]]
    markup = InlineKeyboardMarkup(keys)
    return markup

def settings_reply_markup_uz():
    markup=ReplyKeyboardMarkup(
    [["Til 🌍","Bosh Sahifa 🏠"]],
    resize_keyboard=True)
    return markup
def settings_reply_markup_ru():
    markup=ReplyKeyboardMarkup(
    [["Язык 🌍","Главное Меню 🏠"]],
    resize_keyboard=True)
    return markup

def newfunction(data):
        k=[]
        for i in range(len(data)//2):
                k.append(data[i*2 : (i+1)*2])
        if len(data)%2==1:
                k.append([data[len(data)-1]])
        return k

def category_menu_reply_markup_uz():
    keys=[["ORQAGA ↩️","Savatcha 🛒"]]
    cat=Category.objects.filter(disable=False)
    cats=[]
    for i in cat:
        cats.append(i.name_uz)
    cats=newfunction(cats)
    if cats!=[]:
        keys.extend(cats)
    keys.append(['Bosh Sahifa 🏠'])
    markup=ReplyKeyboardMarkup(
    keys,
    resize_keyboard=True)
    return markup

def category_menu_reply_markup_ru():
    keys=[["НАЗАД ↩️","Корзина 🛒"]]
    cat=Category.objects.filter(disable=False)
    cats=[]
    for i in cat:
        cats.append(i.name_ru)
    cats=newfunction(cats)
    if cats!=[]:
        keys.extend(cats)
    keys.append(['Главное Меню 🏠'])
    markup=ReplyKeyboardMarkup(
    keys,
    resize_keyboard=True)
    return markup



def product_reply_markup_uz(id):
    products=id
    if len(products)==10:
        keys = []
        k=0
        l=[]
        for i in products:
            k+=1
            if k%5==0:
                l.append(InlineKeyboardButton(f'''{k}''',callback_data=str(i.id)))
                keys.append(l)
                l=[]
            else:
                l.append(InlineKeyboardButton(f'''{k}''',callback_data=str(i.id)))
    elif len(products)<6:
        keys = []
        l=[]
        k=0
        for i in products:
            k+=1
            l.append(InlineKeyboardButton(f'''{k}''',callback_data=str(i.id)))
        keys.append(l)
    elif len(products)<10: 
        keys = []
        k=0
        l=[]
        for i in products:
            k+=1
            if k%(len(products)//2)==0:
                l.append(InlineKeyboardButton(f'''{k}''',callback_data=str(i.id)))
                keys.extend(l)
                l=[]
            else: 
                l.append(InlineKeyboardButton(f'''{k}''',callback_data=str(i.id)))
        pass
    keys.append([InlineKeyboardButton("⬅️",callback_data=str("⬅️")),InlineKeyboardButton("❌",callback_data=str("❌")),InlineKeyboardButton("➡️",callback_data=str("➡️"))])


    murkup = InlineKeyboardMarkup(keys)
    return murkup



def product_quantity_reply_markup_uz(n):
    keys = []
    keys.append([InlineKeyboardButton(f'''-''',callback_data='-'),InlineKeyboardButton(f'''{n}''',callback_data=str(n)),InlineKeyboardButton(f'''+''',callback_data='+')])
    keys.append([InlineKeyboardButton("🔙 Ortga",callback_data=str("🔙 Ortga"))])
    keys.append([InlineKeyboardButton("🛒 Savatchaga qo'shish",callback_data=str("🛒 Savatchaga qo'shish"))])
    murkup = InlineKeyboardMarkup(keys)
    return murkup


def product_quantity_reply_markup_ru(n):
    keys = []
    keys.append([InlineKeyboardButton(f'''-''',callback_data='-'),InlineKeyboardButton(f'''{n}''',callback_data=str(n)),InlineKeyboardButton(f'''+''',callback_data='+')])
    keys.append([InlineKeyboardButton("🔙 Назад",callback_data=str("🔙 Назад"))])
    keys.append([InlineKeyboardButton("🛒 Добавить в корзину",callback_data=str("🛒 Добавить в корзину"))])
    murkup = InlineKeyboardMarkup(keys)
    return murkup

def branche_quantity_reply_markup_uz():
    keys = []
    branches=Branche.objects.all()
    for i in branches:
        keys.append([InlineKeyboardButton(f'''{i.name}''',callback_data=f'''branche_{i.id}''')])
    keys.append([InlineKeyboardButton("Orqaga 👈🏻",callback_data=str("Orqaga 👈🏻"))])
    murkup = InlineKeyboardMarkup(keys)
    return murkup

def branche_quantity_reply_markup_ru():
    keys = []
    branches=Branche.objects.all()
    for i in branches:
        keys.append([InlineKeyboardButton(f'''{i.name}''',callback_data=f'''branche_{i.id}''')])
    keys.append([InlineKeyboardButton("Назад 👈🏻",callback_data=str("Назад 👈🏻"))])
    murkup = InlineKeyboardMarkup(keys)
    return murkup

def cart_menu_reply_markup_uz(ordd):
    keys=[["Buyurtma berish 🚚"]]
    for i in ordd:
        keys.append([f'''❌{i.name_uz}❌'''])
    keys.append(['ORQAGA ↩️',"Bo'shatish 🗑"])
    markup=ReplyKeyboardMarkup(
    keys,
    resize_keyboard=True)
    return markup
def cart_menu_reply_markup_ru(ordd):
    keys=[["Оформить заказ 🚚"]]
    for i in ordd:
        keys.append([f'''❌{i.name_ru}❌'''])
    keys.append(['НАЗАД ↩️',"Очистить 🗑"])
    markup=ReplyKeyboardMarkup(
    keys,
    resize_keyboard=True)
    return markup

def my_order_menu_reply_markup_uz(ord):
    keys=[["ORQAGA ↩️","Savatcha 🛒"]]
    for i in ord:
        keys.append([f'''{i.day} {i.time}'''])
    keys.append(['Bosh Sahifa 🏠'])
    markup=ReplyKeyboardMarkup(
    keys,
    resize_keyboard=True)
    return markup

def my_order_menu_reply_markup_ru(ord):
    keys=[["НАЗАД ↩️","Корзина 🛒"]]
    for i in ord:
        keys.append([f'''{i.day} {i.time}'''])
    keys.append(['Главное Меню 🏠'])
    markup=ReplyKeyboardMarkup(
    keys,
    resize_keyboard=True)
    return markup



def wallet_reply_markup_uz():
    keys=[[
        InlineKeyboardButton("Bu qanday ishlaydi ❓",callback_data=str("Bu qanday ishlaydi ❓")),
        InlineKeyboardButton("Bu nima ❓",callback_data=str("Bu nima ❓"))
    ],
    [
        InlineKeyboardButton("Taklif qilish va bonus olish ❓",callback_data=str("Taklif qilish va bonus olish ❓"))
    ],[
        InlineKeyboardButton("Daromad 💰",callback_data=str("Daromad 💰")),
        InlineKeyboardButton("Xarajat 💶",callback_data=str("Xarajat 💶"))
    ]]
    markup = InlineKeyboardMarkup(keys)
    return markup

def wallet_reply_markup_ru():
    keys=[[
        InlineKeyboardButton("Как это работает ❓",callback_data=str("Bu qanday ishlaydi ❓")),
        InlineKeyboardButton("Что это такое ❓",callback_data=str("Bu nima ❓"))
    ],
    [
        InlineKeyboardButton("Как пригласить и получить Бонус ❓",callback_data=str("Taklif qilish va bonus olish ❓"))
    ],[
        InlineKeyboardButton("Доход  💰",callback_data=str("Daromad 💰")),
        InlineKeyboardButton("Расходы 💶",callback_data=str("Xarajat 💶"))
    ]]
    markup = InlineKeyboardMarkup(keys)
    return markup




def back_menu_reply_markup_uz():
    keys=[['Bosh Sahifa 🏠']]
    markup=ReplyKeyboardMarkup(keys,resize_keyboard=True)
    return markup

def back_menu_reply_markup_ru():
    keys=[['Главное Меню 🏠']]
    markup=ReplyKeyboardMarkup(keys,resize_keyboard=True)
    return markup


   
def promo_reply_markup_uz(pr):
    keys=[]
    for i in pr:
        keys.append([InlineKeyboardButton(f'''{i.name_uz}''',callback_data=f'''promo_{i.id}''')])
    murkup = InlineKeyboardMarkup(keys)
    return murkup

def promo_reply_markup_ru(pr):
    keys = []
    for i in pr:
        keys.append([InlineKeyboardButton(f'''{i.name_ru}''',callback_data=f'''promo_{i.id}''')])
    murkup = InlineKeyboardMarkup(keys)
    return murkup



def region_reply_markup_uz():
    keys=[]
    for i in region_uz:
        keys.append([i])
    keys.append(["ORQAGA ↩️",'Bosh Sahifa 🏠'])
    markup=ReplyKeyboardMarkup(keys,resize_keyboard=True)
    return markup

def region_reply_markup_ru():
    keys=[]
    for i in region_ru:
        keys.append([i])
    keys.append(["НАЗАД ↩️",'Главное Меню 🏠'])
    markup=ReplyKeyboardMarkup(keys,resize_keyboard=True)
    return markup


def district_reply_markup(lang,region):
    list=dict[lang][region]
    keys=[]
    for i in list:
        keys.append([i])
    keys.append(["ORQAGA ↩️",'Bosh Sahifa 🏠'])
    markup=ReplyKeyboardMarkup(keys,resize_keyboard=True)
    return markup

def payment_reply_markup(lang,status):
    keys=[]
    if lang=="uz":
        keys.append(["Click",'Payme'])
        if status==True:
            keys.append(["Naqt",'Hamyon'])
        else:
            keys.append(["Naqt"])
    else:
        keys.append(["Click",'Payme'])
        if status==True:
            keys.append(["Наличные",'Кошелёк'])
        else:
            keys.append(["Наличные"])
    markup=ReplyKeyboardMarkup(keys,resize_keyboard=True)
    return markup