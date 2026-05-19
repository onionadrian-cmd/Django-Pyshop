from django.contrib import admin
from .models import Product, Banner, WebsiteCustomization

# Register your models here.

class WebsiteCustomizationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Primary Colors', {
            'fields': ('primary_color', 'secondary_color', 'accent_color'),
        }),
        ('Background Settings', {
            'fields': ('background_type', 'background_color', 'background_gradient', 'background_image'),
            'description': 'Choose between solid color, gradient, or image for background',
        }),
        ('Text Colors', {
            'fields': ('text_color', 'heading_color'),
        }),
        ('Button Styling', {
            'fields': ('button_color', 'button_text_color', 'button_hover_color', 'button_hover_text_color'),
        }),
        ('Link Styling', {
            'fields': ('link_color', 'link_hover_color'),
        }),
        ('Header & Footer', {
            'fields': ('header_background', 'footer_background', 'footer_text_color'),
        }),
    )

    def has_add_permission(self, request):
        return not WebsiteCustomization.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'id')
    list_editable = ('is_active',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'product_stock', 'category', 'modified_date', 'created_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    search_fields = ('product_name', 'product_description')


admin.site.register(WebsiteCustomization, WebsiteCustomizationAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Product, ProductAdmin)
