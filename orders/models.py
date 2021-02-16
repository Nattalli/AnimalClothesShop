from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Пользователь', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.IntegerField(verbose_name='Цена')


class Cart(models.Model):
    data = models.DateField('Дата создания')
    owner = models.ForeignKey('Customer', verbose_name='Пользователь', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    totalProducts = models.PositiveIntegerField(default=0)
    finalPrice = models.IntegerField(verbose_name='Цена')


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер пользователя')
    address = models.CharField(max_length=255, verbose_name='Адресс')


class Payment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    cardType = models.CharField('тип карты', max_length=255)
    cardDetails = models.CharField('детали оплаты', max_length=255)


class OrderStatus(models.Model):
    us = models.ForeignKey(Cart, on_delete=models.CASCADE, default=1)
    status = models.BooleanField(default=False)
    unit = models.IntegerField
