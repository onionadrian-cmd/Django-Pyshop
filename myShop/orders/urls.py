from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-placed/<str:order_number>/', views.order_placed, name='order_placed'),
    path('orders/', views.order_list, name='order_list'),
]
