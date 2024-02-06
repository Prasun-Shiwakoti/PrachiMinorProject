from django.urls import path
from .views import c_canteen_view, s_canteen_view, orders_view

urlpatterns = [
    path('c_canteen/<uuid:user>', c_canteen_view, name='c_canteen'),
    path('s_canteen/<uuid:user>', s_canteen_view, name='s_canteen'),
    path('order/<uuid:user>', orders_view, name='orders')
]
