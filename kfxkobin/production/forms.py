from django import forms

class OrderForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=100)
    last_name = forms.CharField(label='Фамилия', max_length=100)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Телефон', max_length=20)
    address = forms.CharField(label='Адрес', max_length=250)
    postal_code = forms.CharField(label='Почтовый индекс', max_length=20)
    city = forms.CharField(label='Город', max_length=100)

    # Например, для телефона можно использовать TextInput с атрибутом type="tel"
    # phone = forms.CharField(label='Телефон', max_length=20, widget=forms.TextInput(attrs={'type': 'tel'}))
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='ФИО', max_length=100)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Телефон', max_length=20)
    subject = forms.CharField(label='Тема обращения', max_length=100)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)