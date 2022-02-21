from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name_uz','name_ru',]
    list_display = ('name_uz','name_ru')
    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        return qs.filter(disable=False)
    def delete_queryset(CategoryAdmin, request, queryset):
        print(queryset)
        for i in queryset:
            i.disable=True
            i.save()
    def delete_model(CategoryAdmin, request, obj):
        obj.disable=True
        obj.save()


class ProductAdmin(admin.ModelAdmin):
    fields = ['category','name_uz','name_ru','image','description_uz','description_ru','price','oldprice','quantity']
    list_display = ('category','image_tag','name_uz','name_ru','price','oldprice','description_uz','description_ru','price','oldprice','quantity')
    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request)
        return qs.filter(disable=False)
    def delete_queryset(ProductAdmin, request, queryset):
        print(queryset)
        for i in queryset:
            i.disable=True
            i.save()
    def delete_model(ProductAdmin, request, obj):
        obj.disable=True
        obj.save()


class BrancheAdmin(admin.ModelAdmin):
    fields = ["name","contact","address","location","start_time","end_time"]
    list_display = ("name","contact","address","location","start_time","end_time")

class OrderAdmin(admin.ModelAdmin):
    fields = ["disable",'payment_made']
    list_display = ("phone","name","date","order_status",'payment_made',"disable","evaluation")
    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        return qs.filter(disable=False)
    def delete_queryset(OrderAdmin, request, queryset):
        print(queryset)
    def delete_model(OrderAdmin, request, obj):
        print(obj)


class PromotionAdmin(admin.ModelAdmin):
    fields = ['name_uz','name_ru','image','description_uz','description_ru']
    list_display = ('name_uz','name_ru','image_tag','description_uz','description_ru')
    def get_queryset(self, request):
        qs = super(PromotionAdmin, self).get_queryset(request)
        return qs.filter(disable=False)
    def delete_queryset(PromotionAdmin, request, queryset):
        print(queryset)
        for i in queryset:
            i.disable=True
            i.save()
    def delete_model(PromotionAdmin, request, obj):
        obj.disable=True
        obj.save()

admin.site.register(Category,CategoryAdmin)
admin.site.register(TelegramUser)
admin.site.register(Product, ProductAdmin)
admin.site.register(Branche,BrancheAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Promotion,PromotionAdmin)

