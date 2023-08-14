from drf_spectacular import openapi
from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets, status, mixins, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store.api.serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    ReviewRatingSerializer
)
from store.models import Product, ReviewRating


class ProductAPIView(viewsets.GenericViewSet):
    queryset = Product.objects.is_available()
    lookup_field = 'slug'
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        elif self.action == 'list-detail':
            return ProductDetailSerializer
        else:
            return ProductDetailSerializer

    def retrieve(self, request, slug=None):
        try:
            serializer = ProductDetailSerializer(
                self.queryset.get(slug=slug), many=False)

            data = Response(serializer.data)

            return data
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product with this slug does not exist.'},
                status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


@extend_schema(
    parameters=[openapi.OpenApiParameter(
        'slug', openapi.OpenApiTypes.STR, openapi.OpenApiParameter.PATH)])
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

        return Response('Review Added.')

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

        return Response('Review was delete.')
