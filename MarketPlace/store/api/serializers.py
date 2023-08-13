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
        exclude = ('id', 'product_line',)


class ProductLineSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = ProductLine
        exclude = ('id', 'created_at', 'updated_at',)

    def get_images(self, obj):
        product_line_images = ProductLineImage.objects.filter(
            product_line=obj.id).order_by('-is_main_image', '-updated_at')
        return ProductLineImageSerializer(product_line_images, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.category_name')
    brand = serializers.CharField(source='brand.brand_name')
    seller_shop = serializers.CharField(source='seller_shop.shop_name')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ('id', 'description', 'link_youtube')

    def get_image(self, obj):
        product_image = ProductLineImage.objects.filter(
            product_line__product_id=obj.id,
            is_main_image=True).order_by('-updated_at')[0]
        return ProductLineImageSerializer(
            product_image, many=False).data['url_image']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.category_name')
    brand = serializers.CharField(source='brand.brand_name')
    seller_shop = SellerShopProfileSerializer(many=False)
    product_line = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_product_line(self, obj):
        product_lines = ProductLine.objects.filter(product=obj)
        return ProductLineSerializer(product_lines, many=True).data
