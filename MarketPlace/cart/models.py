import uuid

from django.contrib.auth import get_user_model
from django.db import models

from store.models import Product, AttributeValue


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    total_price = models.DecimalField(
        default=0.00, max_digits=5, decimal_places=2)
    total_item = models.PositiveIntegerField(default=0)

    # additional fields
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.total_price}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='cart_item')
    attribute_value = models.ForeignKey(
        AttributeValue, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    sub_total = models.DecimalField(
        default=0.00, max_digits=5, decimal_places=2)

    # additional fields
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product}-{self.quantity}"
