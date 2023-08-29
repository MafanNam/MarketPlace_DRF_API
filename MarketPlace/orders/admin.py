from django.contrib import admin

from orders.models import (
    Order, OrderStatus,
    OrderItem, Tax,
    ShippingAddress,
)


class OrderItemInLine(admin.TabularInline):
    model = OrderItem


class ShippingAddressInLine(admin.TabularInline):
    model = ShippingAddress


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'order_number', 'payment_method', 'total_price',
        'status', 'is_paid', 'is_delivered')
    list_editable = ('is_paid', 'is_delivered')
    inlines = (OrderItemInLine, ShippingAddressInLine)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'created_at')


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'default')
    list_editable = ('default',)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name_tax', 'value_tax', 'default')
    list_editable = ('default',)


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('order', 'country', 'oblast', 'city', 'created_at')
    ordering = ('created_at',)
    search_fields = ('country', 'oblast', 'city', 'depart_num',)
