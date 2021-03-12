from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse


User = get_user_model()


#class LatestProductsManager:

#    @staticmethod
#    def get_latest_products(self, *args, **kwargs):
 #      products = []
  #      ct_models = ContentType.objects.filter(model__in=args)
   #     for ctm in ct_models:
    #        model_product = ct_models.model_class()._base_manager.all().order_by('-id')[:5]
     #       products.extend(model_product)
      #  if with_respect_to:
       #     ct_model = ContentType.objects.filter(models = with_respect_to)
        #    if ct_model.exists():
         #       if with_respect_to in args:
          #          return sorted(
           #             products, key = lambda x: x.__class__.meta.model_name.startswith(with_respect_to), reverse=True
            #        )
        #return products


#class LatestProducts:

 #   objects = LatestProductsManager()


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя категории')

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='Назва продукту')
    slug = models.SlugField(unique=True, default=1)
    description = models.TextField(default='Опис товару', blank=True)
    price = models.IntegerField(verbose_name='Цена', default=500)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Пользователь', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=0)
    content_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'content_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return "Продукты"


class Cart(models.Model):
    data = models.DateField('Дата создания')
    owner = models.ForeignKey('Customer', verbose_name='Пользователь', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    totalProducts = models.PositiveIntegerField(default=0)
    finalPrice = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return "Cart"


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер пользователя')
    address = models.CharField(max_length=255, verbose_name='Адресс')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class OrderStatus(models.Model):
    us = models.ForeignKey(Cart, on_delete=models.CASCADE, default=1)
    status = models.BooleanField(default=False)
    unit = models.IntegerField
