import os

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from accounts.models import SellerShop, User


def get_upload_path_main_product_image(instance, filename):
    return os.path.join(
        "SellerShops",
        "owner_%d" % instance.seller_shop.owner.id,
        "Products", instance.product_name,
        "product_line_images", filename)


def get_upload_path_product_image(instance, filename):
    return os.path.join(
        "SellerShops",
        "owner_%d" % instance.product.seller_shop.owner.id,
        "Products", instance.product.product_name,
        "product_line_images", filename)


class ManagerQuerySet(models.QuerySet):
    def is_available(self):
        return self.filter(is_available=True)


# PRODUCT AND ADDONS

class Product(models.Model):
    """Product model."""
    product_name = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True, )
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(
        upload_to=get_upload_path_main_product_image,
        default='static/images/default/default_project.png')
    category = models.ForeignKey(
        'Category', on_delete=models.SET('non category'), blank=True)
    brand = models.ForeignKey(
        'Brand', on_delete=models.SET('non brand'), blank=True)
    attribute_value = models.ManyToManyField('AttributeValue')
    seller_shop = models.ForeignKey(SellerShop, on_delete=models.CASCADE)
    link_youtube = models.URLField(blank=True)
    article = models.CharField(max_length=50, unique=True, db_index=True)
    price_new = models.PositiveIntegerField()
    price_old = models.PositiveIntegerField(blank=True, default=0)
    stock_qty = models.PositiveIntegerField()

    # Rating
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.PositiveIntegerField(default=0, null=True, blank=True)

    # additional fields
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ManagerQuerySet.as_manager()

    def __str__(self):
        return self.product_name

    def get_attribute_value(self):
        return ",".join([str(value) for value in self.attribute_value.all()])


class Category(models.Model):
    """Category model for products."""
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(db_index=True)
    description = models.TextField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    """Brand model for products."""
    brand_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(db_index=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.brand_name


class ProductImage(models.Model):
    """Image for products."""
    image = models.ImageField(
        upload_to=get_upload_path_product_image,
        default='static/images/default/default_project.png')
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='images')

    # additional fields
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.image)


class Attribute(models.Model):
    """Attribute for Attribute Value models."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    """Attribute value for products."""
    value = models.CharField(max_length=50, unique=True)
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attribute} - {self.value}"


class ReviewRating(models.Model):
    """Review rating model for products."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='review')
    name = models.CharField(max_length=100)
    rating = models.FloatField(
        validators=[MinValueValidator(0.5), MaxValueValidator(5)])
    comment = models.TextField(max_length=500, blank=True)

    # additional fields
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ManagerQuerySet.as_manager()

    def __str__(self):
        return f"{self.name}-{self.rating}"
