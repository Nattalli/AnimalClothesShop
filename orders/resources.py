from import_export import resources
from .models import Product


class ProductResource(resources.ModelResource):

    class Meta:
        model = Product
        skip_unchanged = True
        report_skipped = True
        fields = ('title', 'description', 'price', 'slug')
        export_order = ('title', 'price')
        import_id_fields = ['title']
