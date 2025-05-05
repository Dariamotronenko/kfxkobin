from django.db import models
from django.contrib.auth.models import User  # Если нужна привязка к пользователю

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    
    # Дополнительные поля
    nutrition_facts = models.TextField(blank=True)  # Пищевая ценность
    storage_conditions = models.CharField(max_length=200, blank=True) # Условия хранения
    manufacturer_info = models.TextField(blank=True) # Информация о производителе

    def __str__(self):
        return self.name

class Cart(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) # Привязка к пользователю (если нужна аутентификация)
    session_id = models.CharField(max_length=100, null=True, blank=True) # Альтернатива для неавторизованных пользователей
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина {self.id}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} в корзине {self.cart.id}"

    def get_total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Привязка к пользователю
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20) 
    address = models.CharField(max_length=250) # Можно разбить на больше полей
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False) # Статус оплаты

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity