from django.contrib import admin

from .models import Product, Category, Brand


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'brand', 'seller_shop', 'is_available',)
    list_editable = ('is_available',)
    prepopulated_fields = {'slug': ('product_name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    prepopulated_fields = {'slug': ('category_name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name',)
    prepopulated_fields = {'slug': ('brand_name',)}
