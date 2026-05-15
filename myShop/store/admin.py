from django.contrib import admin
from .models import Product, Banner

# Register your models here.

class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'id')
    list_editable = ('is_active',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'product_stock', 'category', 'modified_date', 'created_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    search_fields = ('product_name', 'product_description')


admin.site.register(Banner, BannerAdmin)
admin.site.register(Product, ProductAdmin)
