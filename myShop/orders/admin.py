from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'product_price', 'get_row_total')
    readonly_fields = ('get_row_total',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'email', 'status', 'is_ordered', 'order_total', 'created_at')
    list_filter = ('status', 'is_ordered', 'created_at')
    search_fields = ('order_number', 'email', 'first_name', 'last_name')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'user', 'is_ordered', 'status', 'created_at', 'updated_at')
        }),
        ('Customer Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Shipping Address', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Order Details', {
            'fields': ('order_total', 'order_note')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'product_price', 'get_row_total')
    search_fields = ('order__order_number', 'product__product_name')
    readonly_fields = ('get_row_total',)
