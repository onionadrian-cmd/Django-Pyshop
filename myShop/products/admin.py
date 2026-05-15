from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('prodname', 'price', 'stock')
    search_fields = ('prodname',)


admin.site.register(Product, ProductAdmin)