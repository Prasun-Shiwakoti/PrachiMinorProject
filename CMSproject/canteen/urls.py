from django.urls import path
from .views import c_canteen_view, s_canteen_view, orders_view, add_menuItem,add_specialItem,delete_specialItem, delete_menuItem,order_item,confirm_order,logout_view

urlpatterns = [
    path('customer/', c_canteen_view, name='c_canteen'),
    path('staff/', s_canteen_view, name='s_canteen'),
    path('order/', orders_view, name='orders'),
    path('staff/addMenuItem', add_menuItem, name='add_menuItem'),
    path('staff/addspecialItem', add_specialItem, name='add_specialItem'),
    path('staff/deletespecialItem', delete_specialItem, name='delete_specialItem'),
    path('staff/deletemenuItem', delete_menuItem, name='delete_menuItem'),
    path('customer/order_item/', order_item, name='order_Item'),
    path('order/confirm_order', confirm_order, name='confirm_order'),
    path('logout/', logout_view, name='logout'),

]