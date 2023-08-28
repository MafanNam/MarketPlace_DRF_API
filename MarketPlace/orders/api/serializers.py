from rest_framework import serializers

from orders.models import (
    Order, OrderItem, OrderStatus,
    ShippingAddress, Tax,
)
from store.models import Product


class SimpleProductSerializer(serializers.ModelSerializer):
    seller_shop = serializers.CharField(source='seller_shop.shop_name')

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'slug',
                  'seller_shop', 'article', 'price_new')


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        exclude = ('id',)


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        exclude = ('id',)


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'created_at', 'updated_at')


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, read_only=True)
    tax = TaxSerializer(many=False, read_only=True)
    status = OrderStatusSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class CreateOrderSerializer(serializers.Serializer):
    pass
