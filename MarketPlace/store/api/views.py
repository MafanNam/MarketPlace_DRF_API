from rest_framework import generics, viewsets, status
from rest_framework.response import Response

from store.api.serializers import ProductSerializer, ProductDetailSerializer
from store.models import Product


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
            return Response({'error': 'Product with this slug does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)
