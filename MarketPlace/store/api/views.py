from drf_spectacular import openapi
from drf_spectacular.utils import extend_schema

from rest_framework import (
    generics, viewsets, status,
    mixins, )
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from store.api.serializers import (
    ProductSerializer, ProductDetailSerializer,
    ReviewRatingSerializer, ProductCreateSerializer,
    CategorySerializer, BrandSerializer,
    AttributeValueSerializer,
)
from store.api.utils import update_product_review
from store.models import (
    Product, ReviewRating, Category,
    Brand, AttributeValue
)
from MarketPlace.core.permissions import IsAdminOrReadOnly, IsSellerOrReadOnly


class ProductAPIView(viewsets.GenericViewSet,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Product.objects.is_available()
    lookup_field = 'slug'
    permission_classes = [IsSellerOrReadOnly, IsAuthenticatedOrReadOnly]
    """CRUD for Product."""

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action in ('create', 'update', 'partial_update',):
            return ProductCreateSerializer
        return ProductSerializer

    def list(self, request):
        """List products."""
        serializer = self.get_serializer(
            self.queryset.order_by('-created_at'), many=True)

        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        """Detail product."""
        try:
            serializer = self.get_serializer(
                self.queryset.get(slug=slug), many=False)

            data = Response(serializer.data)

            return data
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product with this slug does not exist.'},
                status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Create product."""
        data = self.request.data

        serializer = self.get_serializer(
            data=data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryAPIView(generics.ListAPIView):
    """List Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class BrandAPIView(generics.ListAPIView):
    """List Brand."""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]


class AttributeValueAPIView(generics.ListAPIView):
    """List AttributeValue."""
    queryset = AttributeValue.objects.all().select_related('attribute')
    serializer_class = AttributeValueSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(
    parameters=[openapi.OpenApiParameter(
        'slug', openapi.OpenApiTypes.STR, openapi.OpenApiParameter.PATH)],
    tags=['review'])
class ProductReviewAPIView(generics.GenericAPIView):
    serializer_class = ReviewRatingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, slug=None):
        """Create review for Product."""
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product does not exists.'},
                status=status.HTTP_404_NOT_FOUND)

        if user == product.seller_shop.owner:
            return Response(
                {'message': 'You can not reviewing own Product'},
                status=status.HTTP_200_OK)

        already_exists = product.review.filter(user=user).exists()
        if already_exists:
            return Response({'detail': 'Product already reviewed.'},
                            status=status.HTTP_400_BAD_REQUEST)

        ReviewRating.objects.create(
            user=user,
            product=product,
            name=user.get_full_name(),
            rating=data['rating'],
            comment=data['comment'],
        )

        update_product_review(product)

        return Response('Review Added.', status=status.HTTP_201_CREATED)

    def patch(self, request, slug=None):
        """Update Review for Product."""
        user = request.user
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product does not exists.'},
                status=status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            review = ReviewRating.objects.get(user=user, product=product)
            review.rating = data['rating']
            review.comment = data['comment']
            review.save()

        except ReviewRating.DoesNotExist:
            return Response({'message': 'Review does not exists.'},
                            status=status.HTTP_404_NOT_FOUND)

        update_product_review(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, slug=None):
        """Delete review."""
        user = request.user

        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product does not exists.'},
                status=status.HTTP_404_NOT_FOUND)

        try:
            review = ReviewRating.objects.get(user=user, product=product)
            review.delete()
        except ReviewRating.DoesNotExist:
            return Response({'message': 'Review does not exists.'})

        update_product_review(product)

        return Response(status=status.HTTP_204_NO_CONTENT)
