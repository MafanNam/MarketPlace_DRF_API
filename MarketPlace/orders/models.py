from django.contrib.auth import get_user_model
from django.db import models

from store.models import Product


def get_status():
    return OrderStatus.objects.filter(default=True)[0]


def get_tax():
    return Tax.objects.filter(default=True)[0]


class Order(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name='order')
    payment_method = models.CharField(max_length=255)
    order_number = models.CharField(max_length=255, unique=True)
    order_note = models.CharField(max_length=255, blank=True)
    shipping_price = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, default=0)
    total_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    tax = models.ForeignKey(
        'Tax', on_delete=models.PROTECT, default=get_tax)
    status = models.ForeignKey(
        'OrderStatus', on_delete=models.PROTECT, default=get_status)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    # additional fields
    paid_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    delivered_at = models.DateTimeField(
        auto_now_add=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number


class Tax(models.Model):
    name_tax = models.CharField(max_length=255)
    value_tax = models.DecimalField(max_digits=5, decimal_places=2)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name_tax}-{self.value_tax}"


class OrderStatus(models.Model):
    status = models.CharField(max_length=255)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.status


class OrderItem(models.Model):
    order = models.ForeignKey(
        'Order', on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    # additional fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order}-{self.product}"


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        'Order', on_delete=models.CASCADE, related_name='address')
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    oblast = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    depart_num = models.CharField(max_length=20)

    # additional fields
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
