from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('cart/add/', views.cart_add, name='cart_add'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/update/<int:item_id>/', views.cart_update_quantity, name='cart_update_quantity'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('contact/', views.contact, name='contact'),
    path('products/<int:product_id>/quickview/', views.quick_view, name='quick_view'),
]