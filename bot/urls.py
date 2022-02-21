from django.urls import path
from .views import *

urlpatterns = [
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('',index,name='index'),
    path('alternate',index,name='alternate'),
    path('widgets',widgets,name='widgets'),
    path('ecommerce-products',products,name='ecommerce-products'),
    path('ecommerce-products-details',productdetail,name='ecommerce-products-details'),
    path('ecommerce-add-new-products',addproducts,name='ecommerce-add-new-products'),
    path('ecommerce-orders',orders,name='ecommerce-orders'),
    path('sendmessage/', sendmessage, name='sendmessage'),
    path('changeorderstatus/', changeorderstatus, name='changeorderstatus'),
    path('getorderstatus/', getorderstatus, name='getorderstatus'),
    path('disableorder/', disableorder, name='disableorder'),
    
    

]