from drf_spectacular.utils import extend_schema
from drf_spectacular import openapi

from rest_framework import viewsets, generics, mixins

from cart.api.serializers import CartSerializer, AddCartItemSerializer, CartItemSerializer
from cart.models import Cart, CartItem


class CartViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    parameters=[openapi.OpenApiParameter(
        'cart_pk', openapi.OpenApiTypes.INT, openapi.OpenApiParameter.PATH),
        openapi.OpenApiParameter(
            'id', openapi.OpenApiTypes.INT, openapi.OpenApiParameter.PATH)])
class CartItemViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
