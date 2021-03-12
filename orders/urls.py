from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart),
    path('liked/', views.liked),
    path('user/', views.user),
]
