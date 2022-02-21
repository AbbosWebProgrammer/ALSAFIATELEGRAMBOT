from bot.models import Branche
from django.conf import settings

start_text='''Xizmat tilini tanlang
Выберите язык для обслуживания'''

shall_we_start_uz='Boshlaymizmi😊?'
shall_we_start_ru='Приступим😊?'

get_tel_number_uz='''Raqamingizni jo'nating. Pastdagi tugmani bosing👇🏼:'''
get_tel_number_ru='''Отправьте свой номер телефона. Нажмите на кнопку👇🏼:'''

help_text_uz= '''Bot orqali qanday buyurtma berish kerak

1. Kataloga kirish uchun Katalog tugmasini bosing

2. Mahsulot tanlash uchun, Katalog tugmasini tanlang, bo'limini tanlang va mahsulot bilan tanishing

3. Siz tanlangan mahsulotni ko'rish va tekshirish uchun, Savatcha🛒 ga kiring

4. BUYURTMA BERISH uchun Savatcha 🛒 ga kiring, keyin Buyurtma berish 🚕 tugmasini bosib, BOT ko'rsatmalariga rioya qiling 📝'''
help_text_ru='''Как сделать заказ через бота

1. Нажмите кнопку «Каталог», чтобы получить доступ к каталогу.

2. Для выбора товара нажмите кнопку Каталог, выберите раздел и ознакомьтесь с товаром

3. Чтобы просмотреть и проверить выбранный товар, перейдите в корзину🛒

4. Чтобы ЗАКАЗАТЬ, перейдите в Корзину 🛒, затем нажмите кнопку «Заказать» 🚕 и следуйте инструкциям БОТа 📝
'''

delivery_text_uz="<i>Buyurtmani oldindan berishingizni so'rab qolamiz, yetkazib berish muddati 1 - 3 kun, shuningdek botni barcha ko'rsatmalariga rioya qiling.</i>"
delivery_text_ru="<i>Просим вас оставить заказ заранее, так как время доставки от 1 - 3 день, также следуйте всем инструкциям Бота</i>"

shares_uz="Ayni paytda marosimlar yo'q."
shares_ru="В данное время не планируется мероприятий."

about_us_uz='''🛍 ALSAFIA 🏷
Ishonch va sifat 🤝
Hamyon Bob narxlar 💵
+𝟫𝟫𝟪 𝟧𝟧 𝟧𝟢𝟢 𝟢𝟤 𝟢𝟧
Yetkazib berish xizmati bepul 🚚

📞+998 99 077 08 49

🛍📺📱💻🛠👗👚👕👖🧥🕶🧳💍🧢👟🥾🛍

Telegram Botlar 🧑🏻‍💻👉🏼 @Qahhorov_Abbos'''
about_us_ru='''🛍 АЛЬСАФИЯ 🏷
Надежность и качество 🤝
Кошелек Боб Цены 💵
+ 𝟫𝟫𝟪 𝟧𝟧 𝟧𝟢𝟢 𝟢𝟤 𝟢𝟧
Доставка бесплатная 🚚

📞 + 998 99 077 08 49

🛍📺📱💻🛠👗👚👕👖🧥🕶🧳💍🧢👟🥾🛍

Боты Telegram 🧑🏻‍💻👉🏼 @Qahhorov_Abbos
'''

settings_text_uz='''Sozlamalar bo'limiga xush kelibsiz, kerakli bo'limni tanlang.'''
settings_text_ru='Добро пожаловать в раздел настроек, выберите нужный вам раздел.'

order_start_uz='''Buyurtma berishni boshlaymizmi?'''
order_start_ru='Приступим к заказу?'

change_language_text_uz="Qaysi tilga o'tmoqchisiz?"
change_language_text_ru="На какой язык собираетесь перейти?"
changed_language_text_uz="Til o'zgartirildi."
changed_language_text_ru="Язык был изменен."


categorymenu_text_1_uz="🛍 Xo'sh, buyurtmaga o'tamizmi, sizni eng zo'r mahsulotlar kutmoqda 🔥"
categorymenu_text_1_ru="🛍 Ну что, пошли заказывать, лучшие товары ждут вас 🔥"

categorymenu_text_2_uz="Kategoriyalardan birini tanlang..."
categorymenu_text_2_ru="Выберите одну из категорий..."

back_text_uz="Sahifani tanlang 😊"
back_text_ru="Выберите раздел 😊"

def productmenu_text_uz(count,pd,allcount):
    text=f'''Mahsulotlar  🛒  Jami:{allcount} <b>({count}-{count+len(pd)})</b>:
'''
    k=0
    for i in pd:
        k+=1
        text+=f'''<b>{k}</b>. <i>{i.name_uz}</i> <code> {int(i.price)} so'm</code>
'''

    return text
def productmenu_text_ru(count,pd,allcount):
    text=f'''Продукты  🛒  все:{allcount} <b>({count}-{count+len(pd)})</b>:
'''
    k=0
    for i in pd:
        k+=1
        text+=f'''<b>{k}</b>. <i>{i.name_ru}</i>  <code>{int(i.price)} so'm</code>
'''

    return text

Add_product_to_cart_uz="Maxsulotni Savatga🛒 qo'shish uchun, sonini kiriting 👇🏼"
Add_product_to_cart_ru="Укажите количество данного продукта снизу 👇🏼, и введите вручную, чтобы добавить в Корзину 🛒"\

about_branche_text_uz="Filiallardan birini tanlang 🛍👇🏼"
about_branche_text_ru="Выберите один из Филиалов 🛍👇🏼"

def about_branche_id_uz(id):
    branche=Branche.objects.get(id=int(id))
    text=f'''
<b>{branche.name}</b>

📞 Kontaktlar:  {branche.contact}
🏠 Manzil:   {branche.address}
⏳ Ish vaqti:  {str(branche.start_time)[0:5]} - {str(branche.end_time)[0:5]} (Ochiq)

📍:  {branche.location}
        '''
    return text
def about_branche_id_ru(id):
    branche=Branche.objects.get(id=int(id))
    text=f'''
<b>{branche.name}</b>

📞 Контакты:  {branche.contact}
🏠 Адрес:   {branche.address}
⏳ График:  {str(branche.start_time)[0:5]} - {str(branche.end_time)[0:5]} (Открыто)

📍:  {branche.location}
        '''
    return text



Added_product_to_cart_uz=" - Savatchaga🛒 qo'shildi."
Added_product_to_cart_ru=" - добавлен в Корзину🛒"

do_we_continue_uz="Xo'sh davom etamizmi 😍?"
do_we_continue_ru="Ну что продолжим 😍?"

cart_delete_text_uz='''
«❌ Taom » - taomni savatdan o'chirish.
«🗑 Bo'shatish » - savatni bo'shatadi.'''
cart_delete_text_ur='''
«❌ Наименование » - удалить одну позицию.
«🗑 Очистить » - полная очистка корзины.'''

cart_empty_text_uz="Savatingiz bo'sh, keling buyurtmani birga qilamiz 😇🛍"
cart_empty_text_ru="Ваша корзина пуста, давайте что нибудь закажем 😇🛍"
def products_in_cart_uz(ordd):
    text='''Savatcham:
'''
    summ=0
    summ1=0
    a=0
    for i in ordd:
        a+=1
        text+=f'''
<b>{a}. {i.name_uz}:</b>
<code>{int(i.price)} x {i.quantity} = {int(i.totalprice)} so'm</code>
<s>{int(i.oldprice)} x {i.quantity} = {int(i.totaloldprice)}</s> so'm
        '''
        summ+=int(i.totalprice)
        summ1+=int(i.totaloldprice)
    text+=f'''
    
<b>Jami: {int(summ)} so'm</b>
'''
    text+='''
Diqqat! 100,000 so'mdan yuqori bo'lgan buyurtmalar O'bekiston bo'ylab bepul yetkazib beriladi'''
    return text

def products_in_cart_ru(ordd):
    text='''Корзина:
'''
    summ=0
    summ1=0
    a=0
    for i in ordd:
        a+=1
        text+=f'''
<b>{a}. {i.name_ru}:</b>
<code>{int(i.price)} x {i.quantity} = {int(i.totalprice)} сум</code>
<s>{int(i.oldprice)} x {i.quantity} = {int(i.totaloldprice)}</s> сум
        '''
        summ+=int(i.totalprice)
        summ1+=int(i.totaloldprice)
    text+=f'''
    
<b>Итого: {int(summ)} сум</b>
'''
    text+='''
Внимание! Бесплатная доставка по всему Узбекистану, при заказе от 100,000 сум'''
    return text

location_submit_uz="Joylashuvni yuborish."
location_submit_ru="Отправить местоположение."

your_order_shipped_uz="Sizga tez orada operatorlarimiz qo'ngiroq qilishadi va buyurtmangizni tasdiqlashadi✅"
your_order_shipped_ru="Наши операторы перезвонят вам в ближайшее время и подтвердят ваш заказ✅"
your_order_list_uz="Buyutmalaringiz ro'yxati. Nimalar zakar qilganigizni ko'rmoqchi bo'lsangiz buyurtma qilingan vaqtini tanlang."
your_order_list_ru="Список ваших заказов. Выберите время, которое вы заказали, если вы хотите увидеть, что вы заказали."

def my_order_products_uz(ordd):
    text='''Ro'yxat:
'''
    summ=0
    a=0
    for i in ordd:
        a+=1
        text+=f'''
<b>{a}. {i.name_uz}:</b>
<code>{int(i.price)} x {i.quantity} = {int(i.totalprice)} so'm</code>
        '''
        summ+=int(i.totalprice)
    text+=f'''
    
Jami:<b> {int(summ)} so'm</b>
'''
    text+='''
    '''
    return text
def my_order_products_ru(ordd):
    text='''Список:
'''
    summ=0
    a=0
    for i in ordd:
        a+=1
        text+=f'''
<b>{a}. {i.name_ru}:</b>
<code>{int(i.price)} x {i.quantity} = {int(i.totalprice)} сум</code>
        '''
        summ+=int(i.totalprice)
    text+=f'''
    
Итого:<b> {int(summ)} сум</b>
'''
    text+='''
    '''
    return text

def wallet_text_uz(user):
    text=f'''
<b>Sizni Balansingiz 💰</b>: {user.wallet+user.income} сум

<code>Siz taklif qilidingiz:</code> {user.invitedfriends} do'stlaringizni

Chegirmalarga ega bo'lish uchun do'stlaringizni silkaingiz bilan taklif qiling
'''
    return text
def wallet_text_ru(user):
    text=f'''
<b>Ваш баланс 💰:</b> {user.wallet+user.income} сум

<code>Вы пригласили:</code> {user.invitedfriends} друзей

Пригласите ваших друзей чтобы получить скидки на ваш заказ
'''
    return text

how_it_works_uz=f'''
<b>Ushbu Tizim Qanday ishlaydi❓</b>

Har bir buyurtmalaringizdan 3% miqdori hamyoningizda tushadi

Siz taklif qilingan do'stlaringiz buyurtmalaridan 1% miqdori hamyoningizga tushadi

🔗 taklif qilish uchun ->>> <b>Qanday taklif va bonusni olish❓</b> tugmasidan foydalaning
'''
how_it_works_ru=f'''
<b>Как работает эта Система❓</b>

С каждого заказа вы получаете 3% Кешбэк на свой кошелёк.

С каждого заказа друга который пришёл к нам с помощью вашего приглашения, вы получается 1% на свой кошелёк.

🔗 Чтобы получить ссылку приглашения нажмите ->>> <b>Как пригласить❓</b>
'''

what_is_this_uz=f'''
«Alsafia» dan ajoyib imkoniyat

Bu shu sizning shu akkauntda biriktirilgan Shaxsiy Hamyoningiz

Siz bu hamyoningiz yordamida bizning botga tanishlaringiz va do'stlaringizni taklif qilishingiz mumkin, va doimiy ravishda ularning 
buyurtmalaridan foizlar olishingiz mumkin 
Shuningdek Hamyoningizga har bir sizning buyurtmalaringizdan keshbek tushadi

Qachonki hamyoningiz balansi 10000 so'mdan oshsa, siz to'plangan pullaringizni buyurtmalaringizga ishlatsagiz bo'ladi

<b>HAMYONNI QANDAY TO'LDIRISH UCHUN</b>, shu tugmani bosing ->>> <b>Bu qanday ishlaydi </b>❓
'''
what_is_this_ru=f'''
«Alsafia» и большие возможности

Это ваш Личный кошелек, привязанный к этой учетной записи.

Вы можете приглашать своих ботов и друзей через знакомство с этим кошельком и совершать регулярные посещения.
можно использовать заказы
Каждый ваш заказ будет иметь кэшбэк в вашем кошельке

Когда баланс вашего кошелька превышает 10 000 сумов, вы можете использовать собранные деньги для своих заказов

Чтобы узнать <b>КАК ПОПОЛНИТЬ КОШЕЛЕК</b>, смотрите ->>> <b>Как это работает ❓</b>'''

def offer_bonus_text_uz(id):
    text=f'''Do'stlaringizni taklif qilish uchun mana shu shaxsiy ssilkaingiz bilan foydalaning:https://t.me/{settings.BOTUSERNAME}t?start={id}

Ushbu ssilkani do'stlaringiz va gruppalar bilan ulashing'''
    return text
def offer_bonus_text_ru(id):
    text=f'''Это ваша уникальная ссылка для приглашения ваших друзей: https://t.me/{settings.BOTUSERNAME}?start={id}

Отправьте эту ссылку как можно больше вашим друзьям, и в группах'''
    return text

def about_product_id_uz(pd,n):
    text=f'''
<b>{pd.name_uz}</b>

<b>Narxi: {int(pd.price)} so'm</b>
<b>Oldingi narxi: <s>{int(pd.oldprice)}</s> so'm</b>

{pd.description_uz}

<code>{int(pd.price)} x {n} = {int(pd.price)*n} so'm</code>
<s>{int(pd.oldprice)} x {n} = {int(pd.oldprice)*n}</s> so'm
        '''
    return text
def about_product_id_ru(pd,n):
    text=f'''
<b>{pd.name_ru}</b>

<b>Цена: {int(pd.price)} сум</b>
<b>старая цена: <s>{int(pd.oldprice)}</s>  сум</b>

{pd.description_ru}

<code>{int(pd.price)} x {n} = {int(pd.price)*n} сум</code>
<s>{int(pd.oldprice)} x {n} = {int(pd.oldprice)*n}</s> сум

        '''
    return text

about_promo_text_uz="Aksiyalardan birini tanlang 🎁"
about_promo_text_ru="Выберите один из акции 🎁"