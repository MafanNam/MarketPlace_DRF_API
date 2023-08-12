from django.db import models

from accounts.models import SellerShop


# PRODUCT AND ADDONS

class Product(models.Model):
    """Product model."""
    product_name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(max_length=500, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET('non category'), blank=True)
    brand = models.ForeignKey('Brand', on_delete=models.SET('non brand'), blank=True)
    seller_shop = models.ForeignKey(SellerShop, on_delete=models.CASCADE)
    link_youtube = models.URLField(blank=True)

    # additional fields
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


class Category(models.Model):
    """Category model for products."""
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    description = models.TextField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    """Brand model for products."""
    brand_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.brand_name

# PRODUCT LINE AND ADDONS
