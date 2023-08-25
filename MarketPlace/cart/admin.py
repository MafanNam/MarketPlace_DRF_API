from django.contrib import admin

from cart.models import CartItem, Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'cart', 'product', 'attribute_value', 'quantity', 'created_at',)
