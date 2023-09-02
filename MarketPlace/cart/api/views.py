from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular import openapi

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cart.api.paginations import CartAPIListPagination
from cart.api.serializers import (
    CartSerializer, AddCartItemSerializer,
    CartItemSerializer, UpdateCartItemSerializer,
)
from cart.models import Cart, CartItem


class CartViewSet(viewsets.ModelViewSet):
    """Cart view for CRUD"""
    queryset = Cart.objects.all().order_by('-created_at').prefetch_related(
        'items__product', 'items__product__seller_shop',
        'items__attribute_value__attribute')
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CartAPIListPagination

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
    """CartItem view for CRUD"""
    permission_classes = [IsAuthenticated]

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(
            cart_id=self.kwargs['cart_pk']).prefetch_related(
            'product', 'product__seller_shop', 'attribute_value',
            'attribute_value__attribute',
        ).select_related('attribute_value', 'attribute_value__attribute',
                         'product__seller_shop')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
