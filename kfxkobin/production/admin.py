from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem

# Register your models here.
admin.site.register(Product)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']
    readonly_fields = ('order', 'product', 'price', 'quantity')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False