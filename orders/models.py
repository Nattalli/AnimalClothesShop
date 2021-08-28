from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
import datetime


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Імя категорії')

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, default='Назва продукту')
    slug = models.SlugField(unique=True, default=1, blank=True)
    description = models.TextField(default='Опис товару', blank=True)
    price = models.IntegerField(verbose_name='Ціна', default=0)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default='image/default.jpg', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

    def get_features(self):
        return {f.feature.feature_name: ' '.join([f.value, f.feature.unit or ""]) for f in self.features.all()}

    def __unicode__(self):
        return str(self.title)


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Користувач', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
    qty = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, default=0)
    final_price = models.IntegerField(verbose_name='Ціна')

    def __str__(self):
        return "Продукти"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Користувач', on_delete=models.CASCADE, default=0)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    totalProducts = models.PositiveIntegerField(default=0)
    finalPrice = models.IntegerField(verbose_name='Ціна', default=0)
    status = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер користувача')
    address = models.CharField(max_length=255, verbose_name='Адреса')
    orders = models.ManyToManyField('Order', verbose_name='Замовлення користувача', related_name='related_order')

    def __str__(self):
        return "Користувач: {} {}".format(self.user.first_name, self.user.last_name)


def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0
    cart.total_products = cart_data['id__count']
    cart.save()


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Нове замовлення'),
        (STATUS_IN_PROGRESS, 'Замовлення в обробці'),
        (STATUS_READY, 'Замовлення готове'),
        (STATUS_COMPLETED, 'Замовлення виконане')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовивіз'),
        (BUYING_TYPE_DELIVERY, 'Доставка новою поштою')
    )

    customer = models.ForeignKey(Customer, verbose_name='Замовник', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Імя')
    last_name = models.CharField(max_length=255, verbose_name='Прізвище')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Кошик', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адреса', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус замовлення',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип замовлення',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Коментар до замовлення', null=True, blank=True)

    def __str__(self):
        return str(self.id)
