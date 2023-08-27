from django.contrib import admin

from orders.models import (
    Order, OrderStatus,
    OrderItem, Tax
)


class OrderItemInLine(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'order_number', 'payment_method', 'total_price',
        'status', 'is_paid', 'is_delivered')
    list_editable = ('is_paid', 'is_delivered')
    inlines = (OrderItemInLine,)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'created_at')


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('status',)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name_tax', 'value_tax')
