from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,ConversationHandler,CallbackQueryHandler
from telegram.utils.request import Request
from .keybord import *
from .connectbase import *
from .menu import *
from .adminpage import *

class Command(BaseCommand):
    help = 'TELEGRAM-BOT'
    
    def handle(self, *args, **options):
        request = Request(
            connect_timeout=1,
            read_timeout=100000,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
            base_url=getattr(settings, 'PROXY_URL', None),
        )
        k=bot.get_me()
        settings.BOTUSERNAME=k.username
        print(settings.BOTUSERNAME)
        updater = Updater(
            bot=bot,
            use_context=True,
        )
        updater = Updater(token=settings.TOKEN,use_context = True)

        
        dispatcher = updater.dispatcher
        handler = ConversationHandler(
        entry_points= [
        CommandHandler('start', start),
        CommandHandler('admin', admin),
        ],

        states={
            
            'language':[MessageHandler(Filters.text,language)],
            'contact_callback':[MessageHandler(Filters.contact,contact_callback)],
            'check_contact_number':[MessageHandler(Filters.text,check_contact_number)],
            'menu':[MessageHandler(Filters.text,menu)],
            'botsettings':[MessageHandler(Filters.text,botsettings)],
            'botchangelanguagesettings':[MessageHandler(Filters.text,botchangelanguagesettings)],
            'categorymenu':[MessageHandler(Filters.text,categorymenu)],
            'cartmenu':[MessageHandler(Filters.text,cartmenu)],
            'myordermenu':[MessageHandler(Filters.text,myordermenu)],
            'callbackquery':[CallbackQueryHandler(callbackquery),MessageHandler(Filters.text,callbackquery)],
            'regionmenu':[MessageHandler(Filters.text,regionmenu)],
            'districtmenu':[MessageHandler(Filters.text,districtmenu)],
            'paymentmenu':[MessageHandler(Filters.text,paymentmenu)],
            'evaluation':[CallbackQueryHandler(evaluation)],
            'forward_message_all_users':[MessageHandler(Filters.all,forward_message_all_users)],
            
            'selectmessagetype':[CallbackQueryHandler(selectmessagetype)],
            'send_URLmessage_all_users':[MessageHandler(Filters.text,send_URLmessage_all_users)],
            'send_URLmessage_all_users_message':[CallbackQueryHandler(send_URLmessage_all_users_message)],
            'send_URLmessage_all_users_text':[MessageHandler(Filters.text,send_URLmessage_all_users_text)],
            'send_URLmessage_all_users_photo':[MessageHandler(Filters.photo,send_URLmessage_all_users_photo)],
            'send_URLmessage_all_users_video':[MessageHandler(Filters.video,send_URLmessage_all_users_video)],
            'all_users_send_message':[CallbackQueryHandler(all_users_send_message)],
            'all_users_send_message_text':[MessageHandler(Filters.text,all_users_send_message_text)],
            'all_users_send_message_photo':[MessageHandler(Filters.photo,all_users_send_message_photo)],
            'all_users_send_message_video':[MessageHandler(Filters.video,all_users_send_message_video)],
        },
        fallbacks=[
        CommandHandler('start', start),
        CommandHandler('admin', admin),
        CallbackQueryHandler(evaluation)
        ]
        )
        # dispatcher.add_handler(ShippingQueryHandler(shipping_callback))
        dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
        dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))
        dispatcher.add_handler(handler)
        updater.start_polling()
        updater.idle()

  








