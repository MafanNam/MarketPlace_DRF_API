from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular import openapi

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cart.api.serializers import (
    CartSerializer, AddCartItemSerializer,
    CartItemSerializer, UpdateCartItemSerializer,
)
from cart.models import Cart, CartItem


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    http_method_names = ['get', 'post', 'delete']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    parameters=[openapi.OpenApiParameter(
        'cart_pk', openapi.OpenApiTypes.UUID, openapi.OpenApiParameter.PATH)])
@extend_schema_view(
    partial_update=extend_schema(parameters=[
        openapi.OpenApiParameter('id', openapi.OpenApiTypes.INT,
                                 openapi.OpenApiParameter.PATH)]),
    update=extend_schema(parameters=[
        openapi.OpenApiParameter('id', openapi.OpenApiTypes.INT,
                                 openapi.OpenApiParameter.PATH)]),
    retrieve=extend_schema(parameters=[
        openapi.OpenApiParameter('id', openapi.OpenApiTypes.INT,
                                 openapi.OpenApiParameter.PATH)]),
    destroy=extend_schema(parameters=[
        openapi.OpenApiParameter('id', openapi.OpenApiTypes.INT,
                                 openapi.OpenApiParameter.PATH)]),
)
class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
