from django.db.models import Min

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


from accounts.api.serializers import SellerShopProfileSerializer
from store.models import (
    Category, Brand, Product, ProductLine,
    ProductLineImage, AttributeValue, Attribute,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ('id',)


class ProductLineImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLineImage
        exclude = ('id', 'product_line', 'updated_at',)


class ProductLineSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = ProductLine
        exclude = ('id', 'created_at', 'updated_at', 'product',)

    @extend_schema_field(OpenApiTypes.STR)
    def get_images(self, obj):
        product_line_images = ProductLineImage.objects.filter(
            product_line=obj).order_by('-is_main_image', '-updated_at')
        return ProductLineImageSerializer(product_line_images, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.category_name')
    brand = serializers.CharField(source='brand.brand_name')
    seller_shop = serializers.CharField(source='seller_shop.shop_name')
    image = serializers.SerializerMethodField()
    price_min = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ('id', 'description', 'link_youtube')

    @extend_schema_field(OpenApiTypes.STR)
    def get_image(self, obj):
        product_image = ProductLineImage.objects.filter(
            product_line__product_id=obj.id,
            is_main_image=True).order_by('-updated_at')[0]
        return ProductLineImageSerializer(
            product_image, many=False).data['url_image']

    @extend_schema_field(OpenApiTypes.INT)
    def get_price_min(self, obj):
        product_line = ProductLine.objects.filter(product=obj).aggregate(
            Min('price_new'))
        return product_line['price_new__min']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.category_name')
    brand = serializers.CharField(source='brand.brand_name')
    seller_shop = SellerShopProfileSerializer(many=False)
    product_line = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    @extend_schema_field(ProductLineSerializer)
    def get_product_line(self, obj):
        product_lines = ProductLine.objects.filter(product=obj).order_by('price_new')
        return ProductLineSerializer(product_lines, many=True).data
