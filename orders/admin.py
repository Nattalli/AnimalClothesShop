from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resources import ProductResource

admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)


@admin.register(Product)
class ProductUserAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
