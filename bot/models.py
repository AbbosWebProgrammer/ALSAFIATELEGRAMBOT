from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import  pandas as pd
from django.utils.html import format_html

LANGUAGE_CHOICES = (
    ('uz','UZ'),
    ('ru', 'RU')
)
class TelegramUser(models.Model):
    chat_id=models.IntegerField(null=False,unique=True)
    name = models.CharField(max_length=100,null=False)
    username=models.CharField(max_length=100,null=True)
    admin=models.BooleanField(null=False,default=False)
    phone = PhoneNumberField(_('phone'))
    suggested=models.IntegerField(default=0)
    wallet=models.IntegerField(default=0)
    income=models.IntegerField(default=0)
    cost=models.IntegerField(default=0)
    approved=models.BooleanField(default=False)
    smscode=models.CharField(max_length=10,null=True)
    invitedfriends=models.IntegerField(default=0)
    lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    def __str__(self):
        return str(self.chat_id)
    class Meta:
        ordering = ['id']
        db_table = 'TelegramUser'
        verbose_name = 'TelegramUser'
        verbose_name_plural = 'TelegramUsers'

class Category(models.Model):
    name_uz = models.CharField(max_length=100,null=False,unique=True)
    name_ru = models.CharField(max_length=100,null=False,unique=True)
    disable=models.BooleanField(default=False)

    def __str__(self):
        return f'''{self.name_uz}<||>{self.name_ru}'''
    class Meta:
        ordering = ['id']
        db_table = 'Category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name_uz = models.CharField(max_length=100,null=False,unique=True)
    name_ru = models.CharField(max_length=100,null=False,unique=True)
    image=models.ImageField(null=False)
    description_uz=models.CharField(max_length=1000,null=False)
    description_ru=models.CharField(max_length=1000,null=False)
    price = models.FloatField(null=False)
    oldprice = models.FloatField(null=False)
    quantity = models.IntegerField(default=0)
    buy_quantity = models.IntegerField(default=0)
    disable=models.BooleanField(default=False)
    @property
    def image_tag(self):
        return format_html('<img src="{}"  width="150" />'.format(self.image.url))
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
    def __str__(self):
        return f'''{self.name_uz}<||>{self.name_uz}'''
    class Meta:
        ordering = ['id']
        db_table = 'Product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Promotion(models.Model):
    image=models.ImageField(null=False)
    name_uz = models.CharField(max_length=100,null=False)
    name_ru = models.CharField(max_length=100,null=False)
    description_uz=models.CharField(max_length=1000,null=False)
    description_ru=models.CharField(max_length=1000,null=False)
    disable=models.BooleanField(default=False)
    @property
    def image_tag(self):
        return format_html('<img src="{}"  width="150" />'.format(self.image.url))
    def __str__(self):
        return f'''{self.name_uz}<||>{self.name_ru}'''
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
    def __str__(self):
        return f'''{self.name_uz}<||>{self.name_uz}'''
    @property
    def image_tag(self):
        return format_html('<img src="{}"  width="150" />'.format(self.image.url))
    class Meta:
        ordering = ['id']
        db_table = 'Promotion'
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'




class Order(models.Model):
    STATUS_CHOICES = (
    ('FULFILLED','FULFILLED'),
    ('CONFIRMED', 'CONFIRMED'),
    ('PARTIALLY SHIPPED', 'PARTIALLY SHIPPED'),
    ('REFUSAL', 'REFUSAL'),
)
    PAYMENT_CHOICES = (
    ('Naqt','Naqt'),
    ('Click', 'Click'),
    ('Payme', 'Payme'),
    ('Hamyon', 'Hamyon'),
)
    user=models.ForeignKey(TelegramUser,on_delete=models.CASCADE,null=False)
    phone = PhoneNumberField()
    name = models.CharField(max_length=100,blank=True,null=True)
    username = models.CharField(max_length=100,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    region = models.CharField(max_length=100,blank=True,null=True)
    district = models.CharField(max_length=100,blank=True,null=True)
    status=models.BooleanField(default=False)
    payment_made=models.BooleanField(default=False)
    hatchback=models.BooleanField(default=False)
    payment_type=models.CharField(max_length=20,choices=PAYMENT_CHOICES,default='Naqt')
    order_status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='CONFIRMED')
    disable=models.BooleanField(default=False)
    evaluation=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)],null=True)
    @property
    def day(self):
        return pd.to_datetime(self.date).strftime("%m/%d/%Y")
    @property
    def time(self):
        return pd.to_datetime(self.date).strftime("%H:%M:%S")
    def __str__(self):
        return f"{self.phone}  {self.day}  {self.time}"
    class Meta:
        ordering = ['id']
        db_table = 'Order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    name_uz = models.CharField(max_length=100,blank=True,null=True)
    name_ru = models.CharField(max_length=100,blank=True,null=True)
    quantity = models.IntegerField(null=False)
    price = models.FloatField(null=False)
    oldprice = models.FloatField(null=False)
    totalprice=models.FloatField(null=True)
    totaloldprice=models.FloatField(null=True)

    def save(self, *args, **kwargs):
        self.price = self.product.price
        self.oldprice = self.product.oldprice
        self.name_uz = self.product.name_uz
        self.name_ru = self.product.name_ru
        self.totalprice = self.product.price*self.quantity
        self.totaloldprice = self.product.oldprice*self.quantity
        super(OrderDetail, self).save(*args, **kwargs)
    def __str__(self):
        return f"orderid: {self.order.id} || totalpice: {self.totalprice}"
    class Meta:
        ordering = ['id']
        db_table = 'OrderDetail'
        verbose_name = 'OrderDetail'
        verbose_name_plural = 'OrderDetails'

class Productevaluation(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    evaluation=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    def __str__(self):
        return f'''{self.product}<||>{self.evaluation}'''
    class Meta:
        ordering = ['id']
        db_table = 'Productevaluation'
        verbose_name = 'Productevaluation'
        verbose_name_plural = 'Productevaluations'
class Branche(models.Model):
    name = models.CharField(max_length=100,null=False)
    contact=PhoneNumberField(_('phone'))
    address=models.CharField(max_length=100,null=False)
    location = models.CharField(max_length=1000,null=False)
    start_time = models.TimeField(_(u"Start Time"),null=False)
    end_time = models.TimeField(_(u"End Time"),null=False)
    def __str__(self):
        return f'''{self.name}'''
    class Meta:
        ordering = ['id']
        db_table = 'Branche'
        verbose_name = 'Branche'
        verbose_name_plural = 'Branche'

