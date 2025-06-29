# core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('signup/', views.signup_view,   name='signup'),
    path('login/',  views.login_view,    name='login'),
    path('logout/', views.logout_view,   name='logout'),

    path('',views.home,name='home'),
    
    path('restaurant/<int:id>/', views.menu_view,name='menu'),
    path('track/', views.tracking_list, name='tracking'),
    path('track/update-status/', views.update_order_status, name='update_order_status'),
    path('about/',views.about_view,name='about'),
    
    path('menu-item/save/',views.add_or_edit_menu_item,name='add_or_edit_menu_item'),
    path('menu-item/delete/', views.delete_menu_item,        name='delete_menu_item'),
    
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart_view,name='cart'),
    path('cart/update/',        views.update_cart_item,  name='update_cart_item'),
    path('cart/delete/',        views.delete_cart_item,  name='delete_cart_item'),
    path('cart/checkout/',      views.checkout,          name='checkout'),

]
