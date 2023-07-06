from django.contrib import admin
from import_export import resources
from .models import URLaddress, Page, Product
# Register your models here.

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        export_order = ['id', 'name', 'link', 'disclosure']

admin.site.register(URLaddress)
admin.site.register(Page)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'disclosure']

admin.site.register(Product, ProductAdmin)
