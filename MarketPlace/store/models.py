import os

from django.db import models

from accounts.models import SellerShop


# PRODUCT AND ADDONS

class Product(models.Model):
    """Product model."""
    product_name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(max_length=500, blank=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET('non category'), blank=True)
    brand = models.ForeignKey(
        'Brand', on_delete=models.SET('non brand'), blank=True)
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

class ProductLine(models.Model):
    """Product line for Product."""
    article = models.CharField(max_length=50, unique=True)
    price_new = models.PositiveIntegerField()
    price_old = models.PositiveIntegerField(blank=True)
    stock_qty = models.PositiveIntegerField()
    attribute_value = models.ManyToManyField('AttributeValue')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    # additional fields
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} - {self.attribute_value}"

    def get_attribute_value(self):
        return ",".join([str(value) for value in self.attribute_value.all()])


def get_upload_path_product_line(instance, filename):
    return os.path.join(
        "SellerShops", "%d" % instance.prodict_line.product.product_name,
        "product_line_images", filename)


class ProductLineImage(models.Model):
    """Image for product line."""
    name = models.CharField(max_length=20, blank=True)
    alternative_name = models.CharField(max_length=20, blank=True)
    url_image = models.ImageField(upload_to=get_upload_path_product_line)
    product_line = models.ForeignKey('ProductLine', on_delete=models.CASCADE)
    is_main_image = models.BooleanField(default=False)

    def __str__(self):
        return str(self.url_image)


class Attribute(models.Model):
    """Attribute for Attribute Value models."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    """Attribute value for product line."""
    value = models.CharField(max_length=50, unique=True)
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attribute} - {self.value}"
