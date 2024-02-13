from django.urls import path
from .views import c_canteen_view, s_canteen_view, orders_view, add_menuItem,add_specialItem

urlpatterns = [
    path('c_canteen/', c_canteen_view, name='c_canteen'),
    path('s_canteen/', s_canteen_view, name='s_canteen'),
    path('order/', orders_view, name='orders'),
    path('s_canteen/addMenuItem', add_menuItem, name='add_menuItem'),
    path('s_canteen/addspecialItem', add_specialItem, name='add_specialItem'),
]
