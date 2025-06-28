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
    path('cart/',views.cart_view,name='cart'),
    path('track/<int:order_id>/', views.tracking_view, name='tracking'),
    path('about/',views.about_view,name='about'),
]
