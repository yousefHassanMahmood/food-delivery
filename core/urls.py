from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('', views.restaurant_list, name='home'),
    path('restaurant/<int:id>/', views.menu_view, name='menu'),
    path('cart/', views.cart_view, name='cart'),
    path('track/<int:order_id>/', views.tracking_view, name='tracking'),
    path('about/', views.about_view, name='about'),
]
