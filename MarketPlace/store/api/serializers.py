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
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = AttributeValue
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image',)


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

    class Meta:
        model = Product
        exclude = (
            'id', 'description', 'link_youtube', 'article',
            'stock_qty', 'created_at', 'updated_at', 'attribute_value')


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        source='category.category_name', read_only=True)
    brand = serializers.CharField(source='brand.brand_name', read_only=True)
    seller_shop = SellerShopProfileSerializer(many=False, read_only=True)
    attribute_value = AttributeValueSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    review = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        exclude = ('id',)

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
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Product
        exclude = (
            'id', 'is_available', 'rating', 'numReviews',
            'price_old', 'article',
        )
        extra_kwargs = {
            'seller_shop': {'read_only': True, 'required': False},
            'image': {'required': True},
            'slug': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        uploaded_images = validated_data.pop('uploaded_images')

        seller_shop = SellerShop.objects.get(owner=request.user)
        validated_data['seller_shop'] = seller_shop
        attribute_ids = validated_data['attribute_value']

        product = super().create(validated_data)

        product.attribute_value.set(attribute_ids)

        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)

        return product
