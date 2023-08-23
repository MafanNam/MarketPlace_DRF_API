from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from cart.models import Cart, CartItem
from store.api.serializers import AttributeValueSerializer
from store.models import Product, AttributeValue


class SimpleProductSerializer(serializers.ModelSerializer):
    seller_shop = serializers.CharField(source='seller_shop.shop_name')

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'seller_shop', 'article', 'price_new')


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    attribute_value = AttributeValueSerializer(many=False)
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'attribute_value', 'quantity', 'sub_total')

    @extend_schema_field(OpenApiTypes.INT)
    def get_sub_total(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price_new


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_item = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'total_price', 'total_item', 'items')
        extra_kwargs = {'user': {'read_only': True}}

    @extend_schema_field(OpenApiTypes.INT)
    def get_total_price(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price_new for item in items])
        return total

    @extend_schema_field(OpenApiTypes.INT)
    def get_total_item(self, cart: Cart):
        return cart.items.count()


class AddCartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=False
    )
    attribute_value = serializers.PrimaryKeyRelatedField(
        queryset=AttributeValue.objects.all(), many=False
    )

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'attribute_value')


    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product = self.validated_data['product']
        quantity = self.validated_data['quantity']
        attribute_value = self.validated_data['attribute_value']

        try:
            cart_item = CartItem.objects.get(
                product=product, cart_id=cart_id,
                attribute_value=attribute_value
            )
            cart_item.quantity += quantity
            cart_item.save()

            self.instance = cart_item

        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance
