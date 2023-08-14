import datetime

from django.template.defaultfilters import slugify
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from accounts.api.serializers import SellerShopProfileSerializer
from accounts.models import SellerShop
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
    profile_image = serializers.CharField(
        source='user.user_profile.profile_image', read_only=True)
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
            product=obj, is_main_image=True)
        if product_image.exists():
            product_image = product_image.order_by('-updated_at')[0]
        else:
            print(obj)
            product_image = ProductImage.objects.create(
                product=obj, is_main_image=True)
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


class ProductCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=False)
    attribute_value = serializers.PrimaryKeyRelatedField(
        queryset=AttributeValue.objects.all(), many=True)
    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), many=False)
    seller_shop = serializers.CharField(required=False, read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Product
        exclude = (
            'id', 'is_available', 'rating', 'numReviews',
            'price_old', 'article',
        )

    def create(self, validated_data):
        request = self.context.get('request')

        seller_shop = SellerShop.objects.get(owner=request.user)
        validated_data['seller_shop'] = seller_shop
        attribute_ids = validated_data['attribute_value']

        category_initials = ''.join(
            word[0] for word in validated_data['category'].category_name.split())
        product_initials = validated_data['product_name'].replace(' ', '')[:3]

        formatted_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        validated_data['article'] = f"{category_initials}-{product_initials}{formatted_time}"

        validated_data['slug'] = slugify(f"{validated_data['product_name']}-{formatted_time}")

        product = super().create(validated_data)

        product.attribute_value.set(attribute_ids)

        return product
