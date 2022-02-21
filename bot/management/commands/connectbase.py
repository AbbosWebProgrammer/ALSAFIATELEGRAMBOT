from click import password_option
from bot.models import *

def userid(id,first_name,username,suggested):
    try:
        users=list(TelegramUser.objects.values_list('chat_id', flat=True))
        if id not in users:
            created  = TelegramUser.objects.create(
                chat_id=id,
                name=first_name,
                username=username,
                suggested=suggested
            )
            created.save()
        return True
    except Exception as e:
        return False

def useraddlanguage(id,lang):
    try:
        user = TelegramUser.objects.get( chat_id=id)
        user.lang=lang
        user.save()
    except Exception as e:
        print(e)
def useraddphone(id,phone,password):
    try:
        createadmin = TelegramUser.objects.get( chat_id=id,)
        createadmin.phone=phone
        createadmin.smscode=password
        createadmin.save()
    except Exception as e:
        print(e)
def userchangepassword(id,password):
    try:
        createadmin = TelegramUser.objects.get( chat_id=id,)
        createadmin.smscode=password
        createadmin.save()
    except Exception as e:
        print(e)

def usergetphone(id):
    try:
        user = TelegramUser.objects.get( chat_id=id)
        return user.phone 
    except Exception as e:
        print(e)
def usergetlanguage(id):
    try:
        user = TelegramUser.objects.get( chat_id=id)
        return user.lang 
    except Exception as e:
        print(e)



def get_admin_id():
    try:
        users=list(TelegramUser.objects.filter(admin=True).values_list('chat_id', flat=True))
        return users

    except Exception as e:
        print(e)
def check_approved(id):
    try:
        user=TelegramUser.objects.get(chat_id=id)
        return user.approved
    except Exception as e:
        print(e)
# def get_group_chat_id():
#     try:
#         groups=list(Groupinfo.objects.values_list('group_id', flat=True))
#         return groups

#     except Exception as e:
#         
# def get_group_chat_info():
#     try:
#         groups=list(Groupinfo.objects.values_list('group_id','group_title','group_username'))
#         return groups

#     except Exception as e:
#         print(e)


def get_bot_user_count():
    try:
        users=list(TelegramUser.objects.values_list('chat_id', flat=True))
        return len(users)

    except Exception as e:
        print(e)

def get_bot_user_list():
    try:
        users=list(TelegramUser.objects.values_list('chat_id',"name","username"))
        return users

    except Exception as e:
        print(e)


def get_peoples_chat_id():
    try:
        users=list(TelegramUser.objects.values_list('chat_id', flat=True))
        return users

    except Exception as e:
        print(e)








