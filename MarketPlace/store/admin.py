from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Product, Category, Brand,
    AttributeValue, Attribute,
    ProductImage, ReviewRating
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


class ProductImageInLine(admin.TabularInline):
    model = ProductImage


class AttributeValueInLine(admin.TabularInline):
    model = AttributeValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name', 'category', 'brand', 'seller_shop', 'is_available',
    )
    list_editable = ('is_available',)
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = (ProductImageInLine,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    prepopulated_fields = {'slug': ('category_name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name',)
    prepopulated_fields = {'slug': ('brand_name',)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'updated_at',)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value',)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'is_available', 'created_at')
    list_editable = ('is_available',)
