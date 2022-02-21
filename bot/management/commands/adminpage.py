from telegram import ReplyKeyboardMarkup,KeyboardButton,InputMediaPhoto
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from .connectbase import *
def messagetype():
    keys = []
    keys.append([InlineKeyboardButton("Send message",callback_data=str("Send message"))])
    keys.append([InlineKeyboardButton("Send photo message",callback_data=str("Send photo message"))])
    keys.append([InlineKeyboardButton("Send video message",callback_data=str("Send video message"))])
    keys.append([InlineKeyboardButton("<- Back",callback_data=str("<- Back"))])
    murkup = InlineKeyboardMarkup(keys)
    return murkup
def main_menu():
    keys = []
    keys.append([InlineKeyboardButton("Send message all users",callback_data=str("Send message all users"))])
    keys.append([InlineKeyboardButton("Forward message all users",callback_data=str("Forward message all users"))])
    keys.append([InlineKeyboardButton("Send URLmessage all users",callback_data=str("Send URLmessage all users"))])
    murkup = InlineKeyboardMarkup(keys)
    return murkup

def admin(update,context):
    users = get_admin_id()
    print(users)
    print(update.effective_chat.id)
    if update.effective_chat.id in  users:
        murkup = main_menu()
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'''Assalomu aleykum Admin page xush kelibsiz!''',
            reply_markup=murkup)
        return "selectmessagetype"


def users(update,context):
    users = get_admin_id()
    if str(update.effective_chat.id) in  users:
        users_count=get_bot_user_count()
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'''{users_count}''',
            )
        return "admin"
    else:
        return "start"



def selectmessagetype(update,context):

    query = update.callback_query
    query.answer()
    if query.data == 'Send message all users':
        murkup = messagetype()
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                        message_id=update.callback_query.message.message_id,
                        text="Qanday xabar jo'natmoqchisiz",
                        reply_markup=murkup)
        return 'all_users_send_message'
    if query.data == 'Forward message all users':
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                        message_id=update.callback_query.message.message_id,
                        text = f''' Xabarni jo'nating ! ''')
        return 'forward_message_all_users'
    if query.data == 'Send URLmessage all users':
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                        message_id=update.callback_query.message.message_id,
            text = f'''
Button nomi va URLni kiriting.
Buttonnomi:ButtonURL ko'rinishida kiriting! 
            ''')
        return 'send_URLmessage_all_users'


# send_URLmessage_all_users
def send_URLmessage_all_users(update,context):
    global buttonURL
    buttonURL = update.message.text
    murkup=messagetype()
    context.bot.delete_message(chat_id = update.effective_chat.id,
            message_id = update.message.message_id,)
    context.bot.send_message(chat_id = update.effective_chat.id,
            text="Qanday xabar jo'natmoqchisiz",
            reply_markup=murkup)
    return "send_URLmessage_all_users_message"
def send_URLmessage_all_users_message(update,context):
    query = update.callback_query
    query.answer()
    if query.data == 'Send message':
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Xabarni jo'nating!",)
        return 'send_URLmessage_all_users_text'
    if query.data == 'Send photo message':
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text=" Rasmli xabarni jo'nating!")
        return 'send_URLmessage_all_users_photo'
    if query.data == 'Send video message':
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text=" Videoli xabarni jo'nating!")
        return 'send_URLmessage_all_users_video'
    if query.data == '<- Back':
        murkup=main_menu()
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Assalomu aleykum Admin page xush kelibsiz",
                                reply_markup=murkup)
        return "selectmessagetype"

def forward_message_all_users(update,context):
    chatids=get_peoples_chat_id()
    k=0
    l=0
    for i in chatids:
        try:
            context.bot.forward_message(chat_id=int(i),
                        from_chat_id=update.message.chat_id,
                        message_id=update.message.message_id)
            l+=1
        except Exception as e:
                k+=1
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'''{l+k} Usersdan {l} usersga xabar jo'natildi, {k} usersga jo'natishda xatoli yuz berdi''')
    return "admin"

def send_URLmessage_all_users_text(update,context):
    x = buttonURL.split(":", 1)
    keys = []
    keys.append([InlineKeyboardButton(text=f"{x[0]}", url=f"{x[1]}")])
    murkup = InlineKeyboardMarkup(keys)
    message = update.message.text
    chatids=get_peoples_chat_id()
    k=0
    l=0
    for i in chatids:
        try:
            context.bot.send_message(chat_id = int(i),
                                    text=message,
                                    reply_markup=murkup
                                    )
            l+=1
        except Exception as e:
                k+=1
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'''{l+k} Usersdan {l} usersga xabar jo'natildi, {k} usersga jo'natishda xatoli yuz berdi''')

    return "admin"

def send_URLmessage_all_users_photo(update,context):
    file = update.message.photo[-1].file_id
    filename=str(update.update_id)+'.jpg'
    # print(update.message)
    caption=update.message.caption
    obj = context.bot.get_file(file)
    down=obj.download(filename)
    chatids=get_peoples_chat_id()
    k=0
    l=0
    x = buttonURL.split(":", 1)
    keys = []
    keys.append([InlineKeyboardButton(text=f"{x[0]}", url=f"{x[1]}")])
    murkup = InlineKeyboardMarkup(keys)
    for i in chatids:
        try:
            context.bot.send_photo(
            chat_id=int(i),
            photo = open(filename,'rb'),
            caption=caption,
            reply_markup=murkup
             )
            l+=1
        except Exception as e:
                k+=1
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'''{l+k} Usersdan {l} usersga xabar jo'natildi, {k} usersga jo'natishda xatoli yuz berdi''')
    return "admin"
def send_URLmessage_all_users_video(update,context):
    filename = str(update.message.video.file_id)+'.mp4'
    file_id = update.message.video.file_id
    caption=update.message.caption
    obj = context.bot.get_file(file_id)
    down=obj.download(filename)
    # print(update.message)
    x = buttonURL.split(":", 1)
    keys = []
    keys.append([InlineKeyboardButton(text=f"{x[0]}", url=f"{x[1]}")])
    murkup = InlineKeyboardMarkup(keys)
    if down:
        # print("ishladi")
        chatids=get_peoples_chat_id()
        k=0
        l=0
        for i in chatids:
            try:
                context.bot.send_video(
                chat_id= int(i),
                video=open(filename, 'rb'),
                caption=caption,
                timeout=10000000,
                reply_markup=murkup)
                l+=1
            except Exception as e:
                k+=1
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'''{l+k} Usersdan {l} usersga xabar jo'natildi, {k} usersga jo'natishda xatoli yuz berdi''')
    else:
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'''Xatolik sodir bo'ldi
            ''')

    return "admin"

# <<<<<<<<<=======send_message_user_id_id=======>>>>>>>>>>>>>>>>>>>

#  AllUsers send message
def all_users_send_message(update,context):

    query = update.callback_query
    query.answer()
    if query.data == 'Send message':
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Xabarni jo'nating!",)
        return 'all_users_send_message_text'
    if query.data == 'Send photo message':
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text=" Rasmli xabarni jo'nating!")
        return 'all_users_send_message_photo'
    if query.data == 'Send video message':
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text=" Videoli xabarni jo'nating!")
        return 'all_users_send_message_video'
    if query.data == '<- Back':
        murkup=main_menu()
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Assalomu aleykum Admin page xush kelibsiz",
                                reply_markup=murkup)
        return "selectmessagetype"


def all_users_send_message_text(update,context):
    keys = []
    keys.append([InlineKeyboardButton("Батафсил",callback_data=str("Batafsil"))])
    murkup = InlineKeyboardMarkup(keys)
    message = update.message.text
    chatids=get_peoples_chat_id()
    k=0
    l=0
    for i in chatids:
        try:
            context.bot.send_message(chat_id = int(i),
                                    text=message,
                                    reply_markup=murkup
                                    )
            l+=1
        except Exception as e:
                k+=1
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'''{l+k} Usersdan {l} usersga xabar jo'natildi, {k} usersga jo'natishda xatoli yuz berdi''')

    return "admin"

def all_users_send_message_photo(update,context):
    file = update.message.photo[-1].file_id
    filename=str(update.update_id)+'.jpg'
    # print(update.message)
    caption=update.message.caption
    obj = context.bot.get_file(file)
    down=obj.download(filename)
    chatids=get_peoples_chat_id()
    k=0
    l=0
    for i in chatids:
        try:
            context.bot.send_photo(
            chat_id=int(i),
            photo = open(filename,'rb'),
            caption=caption,
             )
            l+=1
        except Exception as e:
                k+=1
    context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'''{l+k} Usersdan {l} usersga xabar jo'natildi, {k} usersga jo'natishda xatoli yuz berdi''')
    return "admin"

def all_users_send_message_video(update,context):
    filename = str(update.message.video.file_id)+'.mp4'
    file_id = update.message.video.file_id
    caption=update.message.caption
    obj = context.bot.get_file(file_id)
    down=obj.download(filename)
    # print(update.message)
    if down:
        # print("ishladi")
        chatids=get_peoples_chat_id()
        k=0
        l=0
        for i in chatids:
            try:
                context.bot.send_video(
                chat_id= int(i),
                video=open(filename, 'rb'),
                caption=caption,)
                l+=1
            except Exception as e:
                k+=1
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'''{l+k} Usersdan {l} usersga xabar jo'natildi, {k} usersga jo'natishda xatoli yuz berdi''')
    else:
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'''Xatolik sodir bo'ldi
            ''')

    return "admin"



def edit_home_page(update,context):
    query = update.callback_query
    query.answer()
    if query.data == 'Home page':
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Xabarni jo'nating!",)
        return 'edit_home_page_text'
    if query.data == 'Batafsil':
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Xabarni jo'nating!")
        return 'edit_home_page_batafsil_text'
    if query.data == 'Dastur':
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Xabarni jo'nating!")
        return 'edit_home_page_dastur_text'
    if query.data == "To'lov":
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Xabarni jo'nating!")
        return 'edit_home_page_tulov_text'
    if query.data == "Aloqa":
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Xabarni jo'nating!")
        return 'edit_home_page_aloqa_text'

    if query.data == '<- Back':
        murkup=main_menu()
        context.bot.editMessageText(chat_id = update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Assalomu aleykum Admin page xush kelibsiz",
                                reply_markup=murkup)
        return "selectmessagetype"




