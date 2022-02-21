from bot.models import *
from .keybord import *
from .connectbase import *
from .texts import *
from telegram.ext import CallbackContext
from django.conf import settings
from django.db.models import Q
from telegram import ParseMode, Update
from telegram import ParseMode
from .adminpage import *
from .smsphonenumber import *
import datetime
from telegram import LabeledPrice, ShippingOption, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    CallbackContext,
)
product_id=0
reply_markup_delete_id=0
category_id=0
allproducts=[]
selectproducts=[]
def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'''Error: {e}'''
            print(error_message)
            raise e
    return inner

@log_errors
def start(update: Update, context: CallbackContext):
    id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    username = f"@{update.message.from_user.username}"
    if len(update.message.text)>7 and update.message.text[7:].isnumeric():
        users_list=list(TelegramUser.objects.values_list('chat_id', flat=True))
        suggested=int(update.message.text[7:])
        if int(suggested) in users_list:
            user=TelegramUser.objects.get(chat_id=suggested)
            user.invitedfriends+=1
            user.save()
            userid(id,first_name,username,suggested)
        else:
            userid(id,first_name,username,0)
    else:
        userid(id,first_name,username,0)


    if update.effective_chat.type=="private":
        if usergetlanguage(id)=="":
            context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=start_text,
            reply_markup=language_reply_markup(),
            parse_mode=ParseMode.HTML
            )
            return 'language'
        elif check_approved(id)!=True:
            if usergetlanguage(id)=='uz':
                text = get_tel_number_uz
                reply_markup=contact_reply_markup_uz()
            else:
                text = get_tel_number_ru
                reply_markup=contact_reply_markup_ru()

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup
                )
            return 'contact_callback'
        else:
            if usergetlanguage(id)=='uz':
                text = shall_we_start_uz
                reply_markup=main_menu_reply_markup_uz()
            else:
                text = shall_we_start_ru
                reply_markup=main_menu_reply_markup_ru()

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup
                )
            return 'menu'

@log_errors
def language(update: Update, context: CallbackContext):
    id=update.effective_chat.id
    message = update.message.text
    if message=="/start":
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=start_text,
            reply_markup=language_reply_markup(),
            parse_mode=ParseMode.HTML
            )
        return 'language'
    if message=="O'zbek 🇺🇿":
        useraddlanguage(id,'uz')
        text=get_tel_number_uz
        reply_markup=contact_reply_markup_uz()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup
            )
        return 'contact_callback'
    if message=="Русский 🇷🇺":
        useraddlanguage(id,'ru')
        text=get_tel_number_ru 
        reply_markup=contact_reply_markup_ru()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup
            )
        return 'contact_callback'
def generate_code():
  numbers=list('1234567890')
  password=''
  for i in range(4):
      password+=choice(numbers)
  return password
@log_errors 
def contact_callback(update: Update, context: CallbackContext):
    contact = update.effective_message.contact
    phone = contact.phone_number
    print(phone)
    password=generate_code()
    useraddphone(update.effective_chat.id,phone,password)
    sendphonepassword(phone,password)
    if usergetlanguage(update.effective_chat.id)=='uz':
        text = "Telefoningizga SMS yuborildi. SMS kodini kiriting.📲"
        reply_markup=ReplyKeyboardMarkup([["Kod kelmadi🔄"],["Raqamimni almashtiring 📲"]],resize_keyboard=True)
    else:
        text = "На ваш телефон отправлено SMS. Введите смс-код.📲"
        reply_markup=ReplyKeyboardMarkup([["Код не пришел🔄"],["Изменить мой номер 📲"]],resize_keyboard=True)
    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
            )
    return "check_contact_number"

@log_errors 
def check_contact_number(update: Update, context: CallbackContext):
    id=update.effective_chat.id
    user=TelegramUser.objects.get(chat_id=update.effective_chat.id)
    message = update.message.text
    if user.smscode==message:
        user.approved=True
        user.save()
        if usergetlanguage(update.effective_chat.id)=='uz':
            help_text = help_text_uz
            delivery_text=delivery_text_uz
            reply_markup=main_menu_reply_markup_uz()
        else:
            help_text = help_text_ru
            delivery_text=delivery_text_ru
            reply_markup=main_menu_reply_markup_ru()
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='🥳'
                )
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=help_text
                )
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=delivery_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
                )
        return "menu"
    elif message in ["Kod kelmadi🔄","Код не пришел🔄"]:
        password=generate_code()
        userchangepassword(id,password)
        sendphonepassword(str(user.phone),password)
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = "Telefoningizga SMS yuborildi. SMS kodini kiriting.📲"
            reply_markup=ReplyKeyboardMarkup([["Kod kelmadi🔄"],["Raqamimni almashtiring 📲"]],resize_keyboard=True)
        else:
            text = "На ваш телефон отправлено SMS. Введите смс-код.📲"
            reply_markup=ReplyKeyboardMarkup([["Код не пришел🔄"],["Изменить мой номер 📲"]],resize_keyboard=True)
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
                )
        return "check_contact_number"
    elif message in ["Raqamimni almashtiring 📲","Изменить мой номер 📲"]:
        if usergetlanguage(id)=='uz':
            text = get_tel_number_uz
            reply_markup=contact_reply_markup_uz()
        else:
            text = get_tel_number_ru
            reply_markup=contact_reply_markup_ru()

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup
            )
        return 'contact_callback'

    else:
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = "Kod xato kitritildi, qayta urunib ko'ring."
        else:
            text = "Код неверный, попробуйте еще раз."

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            )
        return 'check_contact_number'



@log_errors
def menu(update: Update, context: CallbackContext):
    message = update.message.text
    if message=="/start":
        return start(update,context)
    if message=="/admin":
        return admin(update,context)
    if message == '🛍 Katalog 🛍' or message == '🛍 Каталог 🛍' :
        if usergetlanguage(update.effective_chat.id)=='uz':
            text1 = categorymenu_text_1_uz
            text2 = categorymenu_text_2_uz
            reply_markup=category_menu_reply_markup_uz()
        else:
            text1 = categorymenu_text_1_ru
            text2 = categorymenu_text_2_ru
            reply_markup=category_menu_reply_markup_ru() 
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text1,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text2,
            reply_markup=reply_markup
        )
        return 'categorymenu'
    if message == 'Savatcha 🛒' or message == 'Корзина 🛒' :
        return back_basked(update,context)
    if message == 'Biz haqimizda ℹ️' or message == 'О нас ℹ️':
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = about_us_uz
            reply_markup=about_us_reply_markup_uz()
        else:
            text = about_us_ru
            reply_markup=about_us_reply_markup_ru()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup
        )
        return 'callbackquery'
    if message == 'Buyurtmalarim 📂' or message == 'Мои заказы 📂' :
        id=update.effective_chat.id
        user=TelegramUser.objects.get(chat_id=id)
        order=Order.objects.filter(user=user,status=True)
        if len(order)==0:
            if usergetlanguage(update.effective_chat.id)=='uz':
                text = "Siz hali bizdan buyurtma bermadingiz, keling, bu tushunmovchilikni to'g'irlaylik."
                reply_markup=main_menu_reply_markup_uz()
            else:
                text = "Вы еще не заказывали у нас, давайте исправим это недоразумение."
                reply_markup=main_menu_reply_markup_ru()
            text = "Siz hali bizdan buyurtma bermadingiz, keling, bu tushunmovchilikni to'g'irlaylik."
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup)
            return 'menu'
        else:
            
            if usergetlanguage(update.effective_chat.id)=='uz':
                text=your_order_list_uz
                reply_markup=my_order_menu_reply_markup_uz(order)
            else:
                reply_markup=my_order_menu_reply_markup_ru(order)
                text=your_order_list_ru
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup)
            return 'myordermenu'
    if message == 'Mening Hamyonim 💰' or message == 'Мой Кошелёк 💰' :
        id=update.effective_chat.id
        user=TelegramUser.objects.get(chat_id=id)
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = wallet_text_uz(user)
            reply_markup=wallet_reply_markup_uz()
        else:
            text = wallet_text_ru(user)
            reply_markup=wallet_reply_markup_ru()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        return 'menu'
    if message == 'Aksiyalar 🎁' or message == 'Акции 🎁' :
        promos=Promotion.objects.filter(disable=False)
        if len(promos)==0:
            if usergetlanguage(update.effective_chat.id)=='uz':
                text = shares_uz
                reply_markup=main_menu_reply_markup_uz()
            else:
                text = shares_ru
                reply_markup=main_menu_reply_markup_ru()
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup
            )
            return 'menu'
        else:
            if usergetlanguage(update.effective_chat.id)=='uz':
                text = about_promo_text_uz
                reply_markup=promo_reply_markup_uz(promos)
            else:
                text = about_promo_text_ru
                reply_markup=promo_reply_markup_ru(promos)
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo = open('images/aksiya.jpg','rb'),
                caption=text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
                )
            return 'menu'

    if message == 'Sozlamalar ⚙️' or message == 'Настройки ⚙️' :
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = settings_text_uz
            reply_markup=settings_reply_markup_uz()
        else:
            text = settings_text_ru
            reply_markup=settings_reply_markup_ru()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup
        )
        return 'botsettings'
    if message == 'Yordam ‼️' or message == 'Помощь ‼️' :
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = help_text_uz
            reply_markup=main_menu_reply_markup_uz()
        else:
            text = help_text_ru
            reply_markup=main_menu_reply_markup_ru()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup
        )
        return 'menu'
    if message == 'Bosh Sahifa 🏠' or message == 'Главное Меню 🏠' :
        return back_home(update,context)
    
@log_errors
def botsettings(update: Update, context: CallbackContext):
    message = update.message.text
    if message=="/start":
       return start(update,context)
    if message == 'Язык 🌍' or message == 'Til 🌍' :
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = change_language_text_uz
        else:
            text = change_language_text_ru
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=language_reply_markup()
        )
        return 'botchangelanguagesettings'
    if message == 'Bosh Sahifa 🏠' or message == 'Главное Меню 🏠' :
        return back_home(update,context)

@log_errors
def botchangelanguagesettings(update: Update, context: CallbackContext):
    id=update.effective_chat.id
    message = update.message.text
    if message=="/start":
        return start(update,context)
    if message=="/admin":
        return admin(update,context)
    if message=="O'zbek 🇺🇿":
        useraddlanguage(id,'uz')
        text=changed_language_text_uz
        reply_markup=main_menu_reply_markup_uz()
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup
        )
        return 'menu'
    if message=="Русский 🇷🇺":
        useraddlanguage(id,'ru')
        text=changed_language_text_ru 
        reply_markup=main_menu_reply_markup_ru()
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup
        )
        return 'menu'
    
@log_errors
def categorymenu(update: Update, context: CallbackContext):
    global category_id, allproducts, selectproducts,reply_markup_delete_id
    message = update.message.text
    category=Category.objects.filter(Q(name_uz=message) | Q(name_ru=message),disable=False)
    if message=="/start":
        return start(update,context)
    if message=="/admin":
        return admin(update,context)
    if message == 'Bosh Sahifa 🏠' or message == 'Главное Меню 🏠' :
        return back_home(update,context)
    if message == 'ORQAGA ↩️' or message == 'НАЗАД ↩️':
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = back_text_uz
            reply_markup=main_menu_reply_markup_uz()
        else:
            text = back_text_ru
            reply_markup=main_menu_reply_markup_ru()
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup
                )
        return 'menu'
    if message == 'Savatcha 🛒' or message == 'Корзина 🛒' :
       return back_basked(update,context)
    if len(category)!=0:
        category=category[0].id
        category_id=category
        allproducts=Product.objects.filter(category=category,disable=False)
        if len(allproducts)>10:
            selectproducts=allproducts[0:10]
        else:
            selectproducts=allproducts[0:]
        if usergetlanguage(update.effective_chat.id)=='uz':     
            text = productmenu_text_uz(0,selectproducts,len(allproducts))
            reply_markup=product_reply_markup_uz(selectproducts)
            reply_markup2=back_menu_reply_markup_uz()
        else:
            text = productmenu_text_ru(0,selectproducts,len(allproducts))
            reply_markup=product_reply_markup_uz(selectproducts)
            reply_markup2=back_menu_reply_markup_ru()

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup2,
            )
        k=context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
            )
        reply_markup_delete_id=k.message_id
        
        return 'callbackquery'

@log_errors
def myordermenu(update: Update, context: CallbackContext):
    global category_id
    message = update.message.text
    if message=="/start":
        return start(update,context)
    if message=="/admin":
        return admin(update,context)
    if message == 'Bosh Sahifa 🏠' or message == 'Главное Меню 🏠' :
        return back_home(update,context)
    if message == 'ORQAGA ↩️' or message == 'НАЗАД ↩️':
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = order_start_uz
            reply_markup=main_menu_reply_markup_uz()
        else:
            text = order_start_ru
            reply_markup=main_menu_reply_markup_ru()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup
            )
        return 'menu'
    if message == 'Savatcha 🛒' or message == 'Корзина 🛒' :
        return back_basked(update,context)
    user=TelegramUser.objects.get(chat_id=update.effective_chat.id)
    order=Order.objects.filter(user=user,status=True)
    day_time=message.split(' ')
    day=''
    time=''
    order_id=''
 
    if len(day_time)==2: 
        for i in order:
            if str(i.day)==day_time[0] and str(i.time)==day_time[1]:
                day=day_time[0]
                time=day_time[1]
                order_id=i.id

    if day!='' and time!='':
        ordd=OrderDetail.objects.filter(order=Order.objects.get(id=order_id))

        if usergetlanguage(update.effective_chat.id)=='uz':
            text=my_order_products_uz(ordd)
            reply_markup=my_order_menu_reply_markup_uz(order)
        else:
            text=my_order_products_uz(ordd)
            reply_markup=my_order_menu_reply_markup_uz(order)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        return 'myordermenu'
   

@log_errors
def callbackquery(update: Update, context: CallbackContext):
    global product_id, reply_markup_delete_id,allproducts,selectproducts
    if update.message is None:
        query = update.callback_query
        if query.data =='⬅️':
            text=update.callback_query.message.text
            start=int(text[text.index('(')+1:text.index("-")])
            end=int(text[text.index('-')+1:text.index(")")])
            length=int(text[text.index(':')+1:][:text[text.index(':')+1:].index(' ')])
            if allproducts==selectproducts or start==0:
                if usergetlanguage(update.effective_chat.id)=='uz':
                    context.bot.answer_callback_query(update.callback_query.id, text="bu boshlanishi")
                else:
                    context.bot.answer_callback_query(update.callback_query.id, text="это начало")
                return 'callbackquery'
                
            else:
                start=start-10
                selectproducts=allproducts[start:start+10]

                if usergetlanguage(update.effective_chat.id)=='uz':     
                    text = productmenu_text_uz(start,selectproducts,len(allproducts))
                    reply_markup=product_reply_markup_uz(selectproducts)
                else:
                    text = productmenu_text_ru(start,selectproducts,len(allproducts))
                    reply_markup=product_reply_markup_uz(selectproducts)
                
                context.bot.editMessageText(chat_id = update.effective_chat.id,
                                        message_id=update.callback_query.message.message_id,
                                        text=text,
                                        reply_markup=reply_markup,
                                        parse_mode=ParseMode.HTML

                                        )
                return 'callbackquery'   
        elif query.data == '➡️':
            text=update.callback_query.message.text
            start=int(text[text.index('(')+1:text.index("-")])
            end=int(text[text.index('-')+1:text.index(")")])
            length=int(text[text.index(':')+1:][:text[text.index(':')+1:].index(' ')])
           
            if allproducts==selectproducts or length==end:
                if usergetlanguage(update.effective_chat.id)=='uz':
                    context.bot.answer_callback_query(update.callback_query.id, text="bu ohiri")
                else:
                    context.bot.answer_callback_query(update.callback_query.id, text="это конец")
                return 'callbackquery'
            else:
                if length-end<=10:
                    start=end
                    selectproducts=allproducts[start:]
                else:
                    start=end
                    selectproducts=allproducts[ start:start+10]

                    

                if usergetlanguage(update.effective_chat.id)=='uz':     
                    text = productmenu_text_uz(start,selectproducts,len(allproducts))
                    reply_markup=product_reply_markup_uz(selectproducts)
                else:
                    text = productmenu_text_ru(start,selectproducts,len(allproducts))
                    reply_markup=product_reply_markup_uz(selectproducts)
                
                context.bot.editMessageText(chat_id = update.effective_chat.id,
                                        message_id=update.callback_query.message.message_id,
                                        text=text,
                                        reply_markup=reply_markup,
                                        parse_mode=ParseMode.HTML

                                        )
                return 'callbackquery'
        elif query.data == '❌':
            context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id=update.callback_query.message.message_id,reply_markup=None)
            reply_markup_delete_id=0
            return 'callbackquery'
        elif query.data.isnumeric():
            product_id=int(query.data)
            product=Product.objects.get(id=product_id)
            if product.disable==False:
                if usergetlanguage(update.effective_chat.id)=='uz':
                    text=about_product_id_uz(product,1)
                    reply_markup=product_quantity_reply_markup_uz(1)
                else:
                    text=about_product_id_ru(product,1)
                    reply_markup=product_quantity_reply_markup_ru(1)
                context.bot.deleteMessage(chat_id = update.effective_chat.id,
                                        message_id=update.callback_query.message.message_id,
                                        )
                k=context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo = open(product.imageURL[1:],'rb'),
                caption=text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
                )
                reply_markup_delete_id=k.message_id
                return 'callbackquery'
        elif query.data in ['🔙 Ortga','🔙 Назад']:
            context.bot.delete_message(chat_id=update.effective_chat.id,
                                            message_id=update.callback_query.message.message_id)
            product=Product.objects.get(id=product_id)
            category=Category.objects.get(id=product.category.id)
            allproducts=Product.objects.filter(category=category,disable=False)
            if len(allproducts)>10:
                selectproducts=allproducts[0:10]
            else:
                selectproducts=allproducts[0:]
            if usergetlanguage(update.effective_chat.id)=='uz':     
                text = productmenu_text_uz(0,selectproducts,len(allproducts))
                reply_markup=product_reply_markup_uz(selectproducts)
                reply_markup2=back_menu_reply_markup_uz()
            else:
                text = productmenu_text_ru(0,selectproducts,len(allproducts))
                reply_markup=product_reply_markup_uz(selectproducts)
                reply_markup2=back_menu_reply_markup_ru()

            k=context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
                )
            reply_markup_delete_id=k.message_id
            return 'callbackquery'
        elif query.data == '+':
            product=Product.objects.get(id=product_id)
            count=int(query.message.reply_markup.inline_keyboard[0][1].callback_data)
            if usergetlanguage(update.effective_chat.id)=='uz':
                text=about_product_id_uz(product,count+1)
                reply_markup=product_quantity_reply_markup_uz(count+1)
            else:
                text=about_product_id_uz(product,count+1)
                reply_markup=product_quantity_reply_markup_ru(count+1)
            context.bot.edit_message_media(
                    chat_id=update.effective_chat.id,
                    message_id=update.callback_query.message.message_id, 
                    media=InputMediaPhoto(
                        media=open(product.imageURL[1:], 'rb'),
                        caption=text,
                        parse_mode=ParseMode.HTML
                    ),
                    reply_markup=reply_markup,
                )
            return 'callbackquery'
        elif query.data == '-':
            product=Product.objects.get(id=product_id)
            count=int(query.message.reply_markup.inline_keyboard[0][1].callback_data)
            if count==1:
                count=2
            if usergetlanguage(update.effective_chat.id)=='uz':
                text=about_product_id_uz(product,count-1)
                reply_markup=product_quantity_reply_markup_uz(count-1)
            else:
                text=about_product_id_uz(product,count-1)
                reply_markup=product_quantity_reply_markup_uz(count-1)
            context.bot.edit_message_media(
                    chat_id=update.effective_chat.id,
                    message_id=update.callback_query.message.message_id, 
                    media=InputMediaPhoto(
                        media=open(product.imageURL[1:], 'rb'),
                        caption=text,
                        parse_mode=ParseMode.HTML

                    ),
                    reply_markup=reply_markup
                )
            return 'callbackquery'
        elif query.data == "🛒 Savatchaga qo'shish" or  query.data == '🛒 Добавить в корзину':
            product=Product.objects.get(id=product_id)
            count=int(query.message.reply_markup.inline_keyboard[0][1].callback_data)
            context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id=update.callback_query.message.message_id, reply_markup=None)
            id=update.effective_chat.id
            pd=product
            user=TelegramUser.objects.get(chat_id=id)
            order=Order.objects.filter(user=user,status=False)
            if len(order)==0:
                order=Order.objects.create(
                    user=user,
                    phone=user.phone,
                    name=user.name,
                    username=user.username
                )
                order.save()
                ordd=OrderDetail.objects.create(
                        order=order,
                        product=pd,
                        quantity=count
                    )
                ordd.save()
            else:
                order=order[0]
                ordds=OrderDetail.objects.filter(order=order)
                if len(ordds)==0:
                    ordd=OrderDetail.objects.create(
                        order=order,
                        product=pd,
                        quantity=count
                    )
                    ordd.save()
                else:
                    ordds=OrderDetail.objects.filter(order=order,product=pd)
                    if len(ordds)==0:
                        ordd=OrderDetail.objects.create(
                        order=order,
                        product=pd,
                        quantity=count
                        )
                        ordd.save()
                    else:
                        ordd=ordds[0]
                        ordd.quantity=ordd.quantity+count
                        ordd.save()
            if usergetlanguage(update.effective_chat.id)=='uz':
                text1 =f'''<b>{pd.name_uz}</b> {Added_product_to_cart_uz}'''
                text2 =do_we_continue_uz
                reply_markup=category_menu_reply_markup_uz()
            else:
                text1 =f'''<b>{pd.name_ru}</b> {Added_product_to_cart_uz}'''
                text2 =do_we_continue_ru
                reply_markup=category_menu_reply_markup_ru() 
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text1,
                parse_mode=ParseMode.HTML
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text2,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            return 'categorymenu'

    elif update.callback_query is None:
        message = update.message.text
        if message == 'Bosh Sahifa 🏠' or message == 'Главное Меню 🏠' :
            if reply_markup_delete_id!=0:
                context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id=reply_markup_delete_id,reply_markup=None)
                reply_markup_delete_id=0
            return back_home(update,context)
        if message=="/start":
            if reply_markup_delete_id!=0:
                try:
                    context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id=reply_markup_delete_id,reply_markup=None)
                except Exception as e:
                    print(e)
                reply_markup_delete_id=0
            return start(update,context)
        l = menu(update, context)
        if l!=None:
            if reply_markup_delete_id!=0:
                context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id=reply_markup_delete_id,reply_markup=None)
                reply_markup_delete_id=0
            return l
    

@log_errors
def evaluation(update: Update, context: CallbackContext):
    if update.message is None:
        query = update.callback_query
        if query.data == 'Bu qanday ishlaydi ❓':
            if usergetlanguage(update.effective_chat.id)=='uz':
                text = how_it_works_uz
                reply_markup=wallet_reply_markup_uz()
            else:
                text = how_it_works_ru
                reply_markup=wallet_reply_markup_ru()
            context.bot.editMessageText(chat_id = update.effective_chat.id,
                                    message_id=update.callback_query.message.message_id,
                                    text=text,
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.HTML

                                    )            
        elif query.data == 'Bu nima ❓':
            if usergetlanguage(update.effective_chat.id)=='uz':
                text = what_is_this_uz
                reply_markup=wallet_reply_markup_uz()
            else:
                text = what_is_this_ru
                reply_markup=wallet_reply_markup_ru()
            context.bot.editMessageText(chat_id = update.effective_chat.id,
                                    message_id=update.callback_query.message.message_id,
                                    text=text,
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.HTML
                                    )           
        elif query.data == 'Daromad 💰':
            user=TelegramUser.objects.get(chat_id=update.effective_chat.id)
            if usergetlanguage(update.effective_chat.id)=='uz':
                text = f"Daromad: <b>{user.income}</b> so'm"
                reply_markup=wallet_reply_markup_uz()
            else:
                text = f'Доход:  <b>{user.income}</b> сум'
                reply_markup=wallet_reply_markup_ru()
            context.bot.editMessageText(chat_id = update.effective_chat.id,
                                    message_id=update.callback_query.message.message_id,
                                    text=text,
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.HTML
                                    )
        elif query.data == 'Xarajat 💶':
            user=TelegramUser.objects.get(chat_id=update.effective_chat.id)
            if usergetlanguage(update.effective_chat.id)=='uz':
                text = f"Hamyondan xarajat: <b>{user.cost}</b> so'm"
                reply_markup=wallet_reply_markup_uz()
            else:
                text = f'Мой кошелёк расходы: <b>{user.cost}</b> сум'
                reply_markup=wallet_reply_markup_ru()
            context.bot.editMessageText(chat_id = update.effective_chat.id,
                                    message_id=update.callback_query.message.message_id,
                                    text=text,
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.HTML
                                    )    
        elif query.data == 'Taklif qilish va bonus olish ❓':
            if usergetlanguage(update.effective_chat.id)=='uz':
                text = offer_bonus_text_uz(update.effective_chat.id)
                reply_markup=wallet_reply_markup_uz()
            else:
                text = offer_bonus_text_ru(update.effective_chat.id)
                reply_markup=wallet_reply_markup_ru()
            context.bot.editMessageText(chat_id = update.effective_chat.id,
                                    message_id=update.callback_query.message.message_id,
                                    text=text,
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.HTML
                                    )  
        elif query.data == 'Filiallar 🏠' or  query.data == 'Филиалы 🏠':
            if usergetlanguage(update.effective_chat.id)=='uz':
                text = about_branche_text_uz
                reply_markup=branche_quantity_reply_markup_uz()
            else:
                text = about_branche_text_ru
                reply_markup=branche_quantity_reply_markup_ru()
            context.bot.editMessageText(chat_id = update.effective_chat.id,
                                    message_id=update.callback_query.message.message_id,
                                    text=text,
                                    reply_markup=reply_markup

                                    )            
        elif query.data == 'Назад 👈🏻' or  query.data == 'Orqaga 👈🏻':
            if usergetlanguage(update.effective_chat.id)=='uz':
                text = about_us_uz
                reply_markup=about_us_reply_markup_uz()
            else:
                text = about_us_ru
                reply_markup=about_us_reply_markup_ru()
            context.bot.editMessageText(chat_id = update.effective_chat.id,
                                    message_id=update.callback_query.message.message_id,
                                    text=text,
                                    reply_markup=reply_markup
                                    )            
        elif '_' in query.data and query.data.split('_')[0]=='branche' and query.data.split('_')[1].isnumeric():
            branches=Branche.objects.filter(id=int(query.data.split('_')[1]))
            if branches!=0:
                if usergetlanguage(update.effective_chat.id)=='uz':
                    text=about_branche_id_uz(int(query.data.split('_')[1]))
                    reply_markup=branche_quantity_reply_markup_uz()
                else:
                    text=about_branche_id_ru(int(query.data.split('_')[1]))
                    reply_markup=branche_quantity_reply_markup_ru()
                context.bot.editMessageText(chat_id = update.effective_chat.id,
                                        message_id=update.callback_query.message.message_id,
                                        text=text,
                                        reply_markup=reply_markup,
                                        parse_mode=ParseMode.HTML
                                        )
            else:
                context.bot.delete_message(chat_id=update.effective_chat.id,
                                            message_id=update.callback_query.message.message_id)
        elif '_' in query.data and query.data.split('_')[0]=='promo' and query.data.split('_')[1].isnumeric():
            promo=Promotion.objects.filter(id=int(query.data.split('_')[1]),disable=False)
            promos=Promotion.objects.filter(disable=False)
            if promo!=0:
                if usergetlanguage(update.effective_chat.id)=='uz':
                    text=f'''{promo[0].name_uz}
{promo[0].description_uz}
                    '''
                    reply_markup=promo_reply_markup_uz(promos)
                else:
                    text=f'''{promo[0].name_ru}
{promo[0].description_ru}
                    '''
                    reply_markup=promo_reply_markup_ru(promos)
                context.bot.edit_message_media(
                    chat_id=update.effective_chat.id,
                    message_id=update.callback_query.message.message_id, 
                    media=InputMediaPhoto(
                        media=open(promo[0].imageURL[1:], 'rb'),
                        caption=text,
                        parse_mode=ParseMode.HTML
                    ),
                    reply_markup=reply_markup
                )
            else:
                context.bot.delete_message(chat_id=update.effective_chat.id,
                                            message_id=update.callback_query.message.message_id)
                

        elif '_' in query.data and query.data.split('_')[0]=='evaluation' and query.data.split('_')[1].isnumeric():
            text=update.callback_query.message.text
            text=text[2:]
            order_id=text[0:text.index('\n')]
            ball=query.data.split('_')[1]
            id=update.effective_chat.id
            user=TelegramUser.objects.get(chat_id=id)
            order=Order.objects.get(user=user,id=int(order_id))
            order.evaluation=int(ball)
            order.save()
            order_detail=OrderDetail.objects.filter(order=order)
            summ=0
            for i in order_detail:
                summ+=i.totalprice
            user.wallet=user.wallet+summ*0.03
            user.save()
            if user.suggested!=0:
                friend=TelegramUser.objects.get(chat_id=user.suggested)
                friend.income=friend.income+summ*0.01
                friend.save()

            if usergetlanguage(update.effective_chat.id)=='uz':
                text='Xizmatimizdan foydalanganingiz uchun katta rahmat🤩'
                # reply_markup=branche_quantity_reply_markup_uz()
            else:
                text='Большое спасибо за использование нашего сервиса🤩'
                # reply_markup=branche_quantity_reply_markup_ru()
            context.bot.editMessageText(chat_id = update.effective_chat.id,
                                    message_id=update.callback_query.message.message_id,
                                    text=text,
                                    parse_mode=ParseMode.HTML
                                    )


@log_errors
def cartmenu(update: Update, context: CallbackContext):
    global category_id
    message = update.message.text
    if message=="/start":
        return start(update,context)
    if message=="/admin":
        return admin(update,context)
    if message == 'Bosh Sahifa 🏠' or message == 'Главное Меню 🏠' :
        return back_home(update,context)
    if message == 'ORQAGA ↩️' or message == 'НАЗАД ↩️':
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = do_we_continue_uz
            reply_markup=category_menu_reply_markup_uz()
        else:
            text = do_we_continue_ru
            reply_markup=category_menu_reply_markup_ru()
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup
                )
        return 'categorymenu'
    if message == "Bo'shatish 🗑" or message == 'Очистить 🗑' :
        id=update.effective_chat.id
        user=TelegramUser.objects.get(chat_id=id)
        order=Order.objects.filter(user=user,status=False)
        OrderDetail.objects.filter(order=order[0]).delete()
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = "Siz savatchangizni bo'shattingiz 😌, men sizga uni yig'ishda yordam beraman"
            reply_markup=main_menu_reply_markup_uz()
        else:
            text = "Вы очистили свою Корзину 😌, я помогу вам собрать её"
            reply_markup=main_menu_reply_markup_ru()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup
            )
        return 'menu'
    if message == "Оформить заказ 🚚" or message == "Buyurtma berish 🚚" :
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = 'Viloyatingizni tanlang.📍'
            reply_markup=region_reply_markup_uz()
        else:
            text ='Выберите свой регион.📍'
            reply_markup=region_reply_markup_ru()

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup
            )
        return 'regionmenu'
    if len(message)!=0:
        message=message[1:-1]
        id=update.effective_chat.id
        pd=Product.objects.filter(Q(name_uz=message) | Q(name_ru=message),disable=False)
        if len(pd)!=0:
            user=TelegramUser.objects.get(chat_id=id)
            order=Order.objects.filter(user=user,status=False)
            ordd=OrderDetail.objects.get(order=order[0],product=pd[0])
            ordd.delete()
            ordd=OrderDetail.objects.filter(order=order[0])
            if len(ordd)==0:
                if usergetlanguage(update.effective_chat.id)=='uz':
                    text = "Siz savatchangizni bo'shattingiz 😌, men sizga uni yig'ishda yordam beraman"
                    reply_markup=main_menu_reply_markup_uz()
                else:
                    text = "Вы очистили свою Корзину 😌, я помогу вам собрать её"
                    reply_markup=main_menu_reply_markup_ru()
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=text,
                    reply_markup=reply_markup
                    )
                return 'menu'
            else:
                if usergetlanguage(update.effective_chat.id)=='uz':
                    text = products_in_cart_uz(ordd)
                    reply_markup=cart_menu_reply_markup_uz(ordd)
                else:
                    text = products_in_cart_ru(ordd)
                    reply_markup=cart_menu_reply_markup_ru(ordd)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=text,
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML)
                return 'cartmenu'


@log_errors
def regionmenu(update: Update, context: CallbackContext):
    message=update.message.text
    if message=="/start":
        return start(update,context)
    if message=="/admin":
        return admin(update,context)
    elif message == 'Bosh Sahifa 🏠' or message == 'Главное Меню 🏠' :
        return back_home(update,context)
    elif message == 'ORQAGA ↩️' or message == 'НАЗАД ↩️':
       return back_basked(update,context)
    
    elif message in region_uz or message in region_ru:
        id=update.effective_chat.id
        user=TelegramUser.objects.get(chat_id=id)
        orders=Order.objects.filter(user=user)
        order=orders[orders.count()-1]
        order.region=message
        order.save()
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = 'Tumaningizni tanlang.📍'
            reply_markup= district_reply_markup('uz',message)

        else:
            text = 'Выберите свой район.📍'
            reply_markup= district_reply_markup('ru',message)
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup
            )
        return 'districtmenu'
    else:
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = 'Viloyatni tanlang.'
        else:
            text ='Выберите регион.'

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            )
        return 'regionmenu'

@log_errors
def districtmenu(update: Update, context: CallbackContext):
    message=update.message.text
    id=update.effective_chat.id
    user=TelegramUser.objects.get(chat_id=id)
    orders=Order.objects.filter(user=user)
    order=orders[orders.count()-1]
    
    if update.message.text=="/start":
        return start(update,context)
    elif message == 'Bosh Sahifa 🏠' or message == 'Главное Меню 🏠' :
        return back_home(update,context)
    elif message == 'ORQAGA ↩️' or message == 'НАЗАД ↩️':
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = 'Viloyatni tanlang.'
            reply_markup=region_reply_markup_uz()
        else:
            text ='Выберите регион.'
            reply_markup=region_reply_markup_ru()

        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup
                )
        return 'regionmenu'
    elif message in dict[usergetlanguage(update.effective_chat.id)][order.region]:
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = "To'lov turini tanlang."
        else:
            text = "Выберите тип оплаты."
        order.district=message
        order.save()
        ordd=OrderDetail.objects.filter(order=order)
        summ=0
        for i in ordd:
            summ+=i.totalprice
        if user.wallet>=summ:
            reply_markup= payment_reply_markup(usergetlanguage(update.effective_chat.id),True)
        else:
            reply_markup= payment_reply_markup(usergetlanguage(update.effective_chat.id),False)
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup
            )
        return 'paymentmenu'
    else:
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = 'Tumanni tanlang.'
        else:
            text = 'Выбор района.'
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text
            )
        return 'districtmenu'

def messagesendtoadmin(update, context,order):
    ordd=OrderDetail.objects.filter(order=order)
    prices=0
    for i in ordd:
        prices+=i.totalprice
    for i in [912823752,1946111097]:
        context.bot.send_message(
            chat_id=i,
            text= f'BUYURTMA QABUL QILINDI ✅\n🆔 BUYURTMA ID: {order.id}\n' \
                    f'💸 BUYURTMA NARXI: {prices}\n' \
                    f'💳 TOLOV TURI: {order.payment_type}\n' \
                    f'📞 BUYURTMACHI RAQAMI: {order.user.phone}\n' \
                    f'📍 BUYURTMACHI VILOYATI: {order.region}\n' \
                    f'📍 BUYURTMACHI TUMANI: {order.district}\n' \
                    f'📆 BUYURTMA BERILGAN KUN: {order.day}\n' \
                    f'⏰ BUYURTMA BERILGAN VAQT: {order.time}\n' \
                    f'📫 BUYURTMA STATUSI: {order.order_status}'
        )

@log_errors
def paymentmenu(update: Update, context: CallbackContext):
    message=update.message.text
    id=update.effective_chat.id
    user=TelegramUser.objects.get(chat_id=id)
    orders=Order.objects.filter(user=user)
    order=orders[orders.count()-1]
    ordd=OrderDetail.objects.filter(order=order)
    summ=0
    for i in ordd:
        summ+=i.totalprice

    if message in ["Click","Payme"]:
        order.payment_type='Click'
        order.status=True
        order.save()
        chat_id = update.message.chat_id
        title = "Alsafia.uz"
        payload = "Custom-Payload"
        if message=="Click":
            description = f'''Buyurtma #{order.id}'''
            provider_token = settings.CLICKTOKEN
            photo_url='https://click.uz/click/images/clickog.png'
        else:
            description = f'''Заказ #{order.id}'''
            provider_token = settings.PAYMETOKEN
            photo_url='https://payme.uz/assets/images/og-image.png'


        currency='UZS'
        price = 100
        ordd=OrderDetail.objects.filter(order=order)
        prices=[]
        for i in ordd:
            if usergetlanguage(update.effective_chat.id)=='uz':
                prices.append(LabeledPrice(i.name_uz, price * int(i.totalprice)))
            else:
                prices.append(LabeledPrice(i.name_ru, price * int(i.totalprice)))
        
        
        context.bot.send_invoice(
            chat_id, title, description, payload, provider_token, currency, prices ,
            photo_url=photo_url,
            photo_height=512,  # !=0/None or picture won't be shown
            photo_width=512,
            photo_size=512,
        )
        messagesendtoadmin(update, context,order)
        return back_home(update,context)


    if message in ["Naqt","Наличные"]:
        order.payment_type='Naqt'
        order.status=True
        order.save()
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = your_order_shipped_uz
            reply_markup=main_menu_reply_markup_uz()
        else:
            text = your_order_shipped_ru
            reply_markup=main_menu_reply_markup_ru()
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup
            )
        messagesendtoadmin(update, context,order)
        return 'menu'
    if user.wallet>=summ:
        if message in ["Hamyon","Кошелёк"]:
            user.wallet=user.wallet-summ
            user.cost=user.cost+summ
            user.save()
            order.payment_type='Hamyon'
            order.status=True
            order.payment_made=True
            order.save()
            if usergetlanguage(update.effective_chat.id)=='uz':
                text = your_order_shipped_uz
                reply_markup=main_menu_reply_markup_uz()
            else:
                text = your_order_shipped_ru
                reply_markup=main_menu_reply_markup_ru()
            context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=text,
                    reply_markup=reply_markup
                )
            messagesendtoadmin(update, context,order)
            return 'menu'

    else:
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = "To'lov turini tanlang."
        else:
            text = "Выберите тип оплаты."
        order.district=message
        order.save()
        ordd=OrderDetail.objects.filter(order=order)
        summ=0
        for i in ordd:
            summ+=i.totalprice
        if user.wallet>=summ:
            reply_markup= payment_reply_markup(usergetlanguage(update.effective_chat.id),True)
        else:
            reply_markup= payment_reply_markup(usergetlanguage(update.effective_chat.id),False)
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup
            )
        return 'paymentmenu'

# @log_errors
# def shipping_callback(update: Update, context: CallbackContext):
#     query = update.shipping_query
#     if query.invoice_payload != 'Custom-Payload':
#         query.answer(ok=False, error_message="Something went wrong...")
#         return

#     options = [ShippingOption('1', 'Shipping Option A', [LabeledPrice('A', 100)])]
#     price_list = [LabeledPrice('B1', 150), LabeledPrice('B2', 200)]
#     options.append(ShippingOption('2', 'Shipping Option B', price_list))
#     query.answer(ok=True, shipping_options=options)



@log_errors
def precheckout_callback(update: Update, context: CallbackContext):
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        query.answer(ok=True)

@log_errors
def successful_payment_callback(update: Update, context: CallbackContext):
    id=update.effective_chat.id
    user=TelegramUser.objects.get(chat_id=id)
    orders=Order.objects.filter(user=user)
    order=orders[orders.count()-1]
    order.payment_made=True
    order.save()
    
    if usergetlanguage(update.effective_chat.id)=='uz':
        update.message.reply_text("To'lovingiz muvaffaqiyatli amalga oshirildi ✅")
    else:
        update.message.reply_text("Ваш платеж успешно обработан ✅")

        
            

def back_basked(update,context):
    id=update.effective_chat.id
    user=TelegramUser.objects.get(chat_id=id)
    order=Order.objects.filter(user=user,status=False)
    if len(order)==0:
        if usergetlanguage(update.effective_chat.id)=='uz':
            text = cart_empty_text_uz
            reply_markup=category_menu_reply_markup_uz()
        else:
            text = cart_empty_text_ru
            reply_markup=category_menu_reply_markup_ru()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup)
        return 'categorymenu'
    else:
        order=order[0]
        ordd=OrderDetail.objects.filter(order=order)
        if len(ordd)==0:
            if usergetlanguage(update.effective_chat.id)=='uz':
                text = cart_empty_text_uz
                reply_markup=category_menu_reply_markup_uz()
            else:
                text = cart_empty_text_ru
                reply_markup=category_menu_reply_markup_ru()
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup)
            return 'categorymenu'
        else:
            if usergetlanguage(update.effective_chat.id)=='uz':
                text = products_in_cart_uz(ordd)
                reply_markup=cart_menu_reply_markup_uz(ordd)
            else:
                text = products_in_cart_ru(ordd)
                reply_markup=cart_menu_reply_markup_ru(ordd)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML)
            return 'cartmenu'

def back_home(update,context):
    if usergetlanguage(update.effective_chat.id)=='uz':
        text = order_start_uz
        reply_markup=main_menu_reply_markup_uz()
    else:
        text = order_start_ru
        reply_markup=main_menu_reply_markup_ru()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup
        )
    return 'menu'

