from drf_spectacular import openapi
from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets, status, mixins, views
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from store.api.serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    ReviewRatingSerializer, ProductCreateSerializer
)
from store.models import Product, ReviewRating, Category


class ProductAPIView(viewsets.GenericViewSet):
    queryset = Product.objects.is_available()
    lookup_field = 'slug'
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        return ProductDetailSerializer

    def retrieve(self, request, slug=None):
        try:
            serializer = self.serializer_class(
                self.queryset.get(slug=slug), many=False)

            data = Response(serializer.data)

            return data
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product with this slug does not exist.'},
                status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        serializer = self.serializer_class(
            self.queryset.order_by('-created_at'), many=True)

        return Response(serializer.data)


class CreateProductAPIView(generics.GenericAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = self.request.data

        serializer = self.serializer_class(
            data=data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    parameters=[openapi.OpenApiParameter(
        'slug', openapi.OpenApiTypes.STR, openapi.OpenApiParameter.PATH)],
    tags=['review'])
class ProductReviewAPIView(generics.GenericAPIView):
    serializer_class = ReviewRatingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, slug=None):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        product = Product.objects.get(slug=slug)

        already_exists = product.review.filter(user=user).exists()
        if already_exists:
            content = {'detail': 'Product already reviewed.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        ReviewRating.objects.create(
            user=user,
            product=product,
            name=user.get_full_name(),
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = product.review.all()
        count_reviews = reviews.count()
        product.numReviews = count_reviews

        total = 0
        for rev in reviews:
            total += rev.rating

        product.rating = total / count_reviews

        product.save()

        return Response('Review Added.', status=status.HTTP_201_CREATED)

    def patch(self, request, slug=None):
        user = request.user
        product = Product.objects.get(slug=slug)

        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            review = ReviewRating.objects.get(user=user, product=product)
            review.rating = data['rating']
            review.comment = data['comment']
            review.save()
        except ReviewRating.DoesNotExist:
            return Response({'message': 'Review does not exists.'})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, slug=None):
        user = request.user
        product = Product.objects.get(slug=slug)
        try:
            review = ReviewRating.objects.get(user=user, product=product)
            review.delete()
        except ReviewRating.DoesNotExist:
            return Response({'message': 'Review does not exists.'})

        reviews = product.review.all()
        count_reviews = reviews.count()
        product.numReviews = count_reviews

        if count_reviews > 0:
            total = 0
            for rev in reviews:
                total += rev.rating

            product.rating = total / count_reviews
        else:
            product.rating = 0
        product.save()

        return Response(
            'Review was delete.', status=status.HTTP_204_NO_CONTENT)
