from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Product, Category, Brand, ProductLine,
    ProductLineImage, AttributeValue, Attribute
)


class EditLinkInLine(object):
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_"
            f"{instance._meta.model_name}_change",
            args=[instance.pk]
        )
        if instance.pk:
            link = mark_safe(f'<a href="{url}">edit</a>')
            return link
        else:
            return ''


class ProductLineInLine(EditLinkInLine, admin.TabularInline):
    model = ProductLine
    readonly_fields = ('edit',)


class ProductLineImageInLine(admin.TabularInline):
    model = ProductLineImage


class AttributeValueInLine(admin.TabularInline):
    model = AttributeValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name', 'category', 'brand', 'seller_shop', 'is_available',
    )
    list_editable = ('is_available',)
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = (ProductLineInLine,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    prepopulated_fields = {'slug': ('category_name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name',)
    prepopulated_fields = {'slug': ('brand_name',)}


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'article', 'price_new', 'price_old', 'stock_qty',
        'get_attribute_value', 'is_available', 'created_at',)
    list_editable = ('is_available',)
    inlines = (ProductLineImageInLine,)


@admin.register(ProductLineImage)
class ProductLineImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_line', 'is_main_image', 'url_image',)
    list_editable = ('is_main_image',)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value',)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
