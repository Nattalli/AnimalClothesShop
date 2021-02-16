from django.contrib import admin
from .models import Category
from .models import Product
from .models import CartProduct
from .models import Cart
from .models import OrderStatus
from .models import Payment
from .models import Customer


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(OrderStatus)
admin.site.register(Payment)
admin.site.register(Customer)
