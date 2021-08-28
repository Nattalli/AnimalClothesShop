"""MyShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django_email_verification import urls as mail_urls
from django.conf.urls import url


from orders.views import (
    get_category, get_product, get_user, CartView, AddToCartView,
    DeleteFromCartView, ChangeQTYView, CheckoutView, MakeOrderView,
    LoginView, RegistrationView, ProfileView, PasswordsChangeView, password_success)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orders.urls')),
    path('animalshop/', include('orders.urls')),
    path('category/<int:category_id>/', get_category),
    path('<int:product_id>/', get_product),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email/', include(mail_urls)),
    path('password/', PasswordsChangeView.as_view(template_name='orders/change_password.html'),),
    path('password_success', password_success, name='password_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
