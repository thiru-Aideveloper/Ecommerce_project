from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:id>/',product_detail,name='product_detail'),
    
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('add-to-cart/<int:id>/', add_to_cart,  name='add_to_cart'),
    path('cart/',cart,name='cart'),
    path('remove/<int:id>/',remove_cart,  name='remove_cart'),


    path('checkout/',checkout,name='checkout'),
    path('payment-success/',payment_success,name='payment_success'),

    path('orders/',orders,name='orders'),
] 