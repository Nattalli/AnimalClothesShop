from django.shortcuts import render
from django.http import HttpResponse

from .models import Product, Category, Customer, Cart


def index(request):
    product = Product.objects.all()
    category = Category.objects.all()
    context = {
        'product': product,
        'category': category,
        'title': 'Список товарів'
    }
    return render(request, 'orders/main.html', context=context)


def cart(request):
    return HttpResponse('<h1>Cart<h1/>')


def liked(request):
    return HttpResponse('<h1>Liked<h1/>')


def user(request):
    return HttpResponse('<h1>User<h1/>')


def get_category(request, category_id):
    product = Product.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)
    return render(request, 'orders/category.html', {'product': product, 'categories': categories, 'category': category})


def get_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'orders/product_detail.html', {'product': product})
