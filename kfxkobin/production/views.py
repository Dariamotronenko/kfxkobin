from .models import Product, Cart, CartItem, Order, OrderItem
from .forms import OrderForm 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages 
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


def home(request):
    """
    Представление для главной страницы.
    """
    return render(request, 'production/home.html')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'production/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    data = {
        'id': product.id,
        'name': product.name,
        'price': str(product.price),  # Преобразуйте Decimal в строку
        'description': product.description,
        'image': product.image.url if product.image else None,  # Обработайте отсутствие изображения
        'specs': {
            'Вес': '1 кг',  # Замените на реальные данные из вашей модели
            'Срок хранения': '12 месяцев',
            'Упаковка': 'Пакет',
            'Сорт': 'Высший'
        }
    }
    return JsonResponse(data)


from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Product, Cart, CartItem

import json
import logging
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Product, Cart, CartItem


logger = logging.getLogger(__name__)  # Получаем логгер

@csrf_exempt
def cart_add(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))

            product = get_object_or_404(Product, id=product_id)
            cart, created = Cart.objects.get_or_create(session_id=request.session.session_key)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            cart_item.quantity += quantity
            cart_item.save()

            cart_total_items = sum(item.quantity for item in cart.items.all())

            return JsonResponse({
                'success': True,
                'message': 'Товар добавлен в корзину',
                'cart_total_items': cart_total_items
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Ошибка при добавлении в корзину: {e}'
            }, status=400)

def cart_update_quantity(request, item_id):
    """
    Обновляет количество товара в корзине.
    """
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity'))

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({'message': 'Количество обновлено', 'success': True})
    else:
        cart_item.delete()
        return JsonResponse({'message': 'Товар удален', 'success': True})

@require_POST
def cart_remove(request, item_id):
    """
    Удаляет товар из корзины.
    """
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return JsonResponse({'message': 'Товар удален', 'success': True})


def cart_detail(request):
    """
    Отображает содержимое корзины.
    """
    # Получаем корзину для текущей сессии
    cart = None
    try:
        cart = Cart.objects.get(session_id=request.session.session_key)
    except Cart.DoesNotExist:
        pass  # Корзина еще не создана для этой сессии

    return render(request, 'production/cart_detail.html', {'cart': cart})

def create_order(request):
    """
    Представление для создания заказа.
    """
    cart = None
    try:
        cart = Cart.objects.get(session_id=request.session.session_key)
    except Cart.DoesNotExist:
        messages.error(request, "Ваша корзина пуста.")
        return redirect('cart_detail')  # Перенаправляем на страницу корзины

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Создаем заказ
            order = Order.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                postal_code=form.cleaned_data['postal_code'],
                city=form.cleaned_data['city']
            )

            # Создаем элементы заказа
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,  # Сохраняем цену на момент заказа
                    quantity=item.quantity
                )

            # Очищаем корзину
            cart.items.all().delete()
            cart.delete()
            request.session.pop('session_key', None)  # Очищаем session_key

            # Перенаправляем на страницу подтверждения заказа
            return redirect('order_confirmation', order_id=order.id)
        else:
            # Форма не валидна, отображаем ошибки
            return render(request, 'production/create_order.html', {'cart': cart, 'form': form})
    else:
        form = OrderForm()
        return render(request, 'production/create_order.html', {'cart': cart, 'form': form})
    
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'production/order_confirmation.html', {'order': order})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Отправка email
            try:
                send_mail(
                    f'Сообщение с сайта от {name} ({email})',
                    f'Телефон: {phone}\n\n{message}',
                    settings.DEFAULT_FROM_EMAIL,  # Укажите в settings.py
                    [settings.CONTACT_EMAIL],  # Укажите в settings.py
                    fail_silently=False,
                )
                messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
                return redirect('contact')  # Перенаправляем на эту же страницу
            except Exception as e:
                messages.error(request, f'Произошла ошибка при отправке сообщения. Пожалуйста, попробуйте позже. Ошибка: {e}')
                # Логирование ошибки (вместо print)
                print(f"Ошибка при отправке email: {e}")
    else:
        form = ContactForm()
    return render(request, 'production/contact.html', {'form': form})

def quick_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'production/quickview.html', {'product': product})