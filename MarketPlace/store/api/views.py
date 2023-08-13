from rest_framework import generics, viewsets
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

    def retrieve(self, request, slug=None):
        serializer = ProductDetailSerializer(
            self.queryset.get(slug=slug), many=False)

        data = Response(serializer.data)

        return data

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)
