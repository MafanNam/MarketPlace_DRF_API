from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from accounts.api.serializers import SellerShopProfileSerializer
from store.models import (
    Category, Brand, Product,
    AttributeValue, ProductImage, ReviewRating,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ('id',)


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(source='attribute.name')

    class Meta:
        model = AttributeValue
        exclude = ('id',)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ('id', 'product', 'updated_at',)


class ReviewRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = ReviewRating
        exclude = ('id', 'is_available', 'product')


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.category_name')
    brand = serializers.CharField(source='brand.brand_name')
    seller_shop = serializers.CharField(
        source='seller_shop.shop_name', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = (
            'id', 'description', 'link_youtube', 'article',
            'stock_qty', 'created_at', 'updated_at', 'attribute_value')

    @extend_schema_field(OpenApiTypes.STR)
    def get_image(self, obj):
        product_image = ProductImage.objects.filter(
            product=obj, is_main_image=True).order_by('-updated_at')[0]
        return ProductImageSerializer(
            product_image, many=False).data['url_image']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.category_name')
    brand = serializers.CharField(source='brand.brand_name')
    seller_shop = SellerShopProfileSerializer(many=False, read_only=True)
    attribute_value = AttributeValueSerializer(many=True)
    images = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        exclude = ('id',)

    @extend_schema_field(ProductImageSerializer)
    def get_images(self, obj):
        product_images = ProductImage.objects.filter(
            product=obj).order_by('-is_main_image', '-updated_at')
        return ProductImageSerializer(product_images, many=True).data

    @extend_schema_field(ReviewRatingSerializer)
    def get_review(self, obj):
        review = ReviewRating.objects.filter(
            product=obj).order_by('-updated_at')
        return ReviewRatingSerializer(review, many=True).data
