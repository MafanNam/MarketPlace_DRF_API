from drf_spectacular import openapi
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from MarketPlace.core.permissions import IsSellerShopOrderProduct
from orders.api.serializers import (
    OrderSerializer, CreateOrderSerializer,
    UpdateOrderSerializer)
from orders.models import Order

from datetime import datetime


class OrderViewSet(viewsets.ModelViewSet):
    """Order view"""
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        context = {'user': self.request.user}
        serializer = CreateOrderSerializer(
            data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)

        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer


@extend_schema(
    parameters=[openapi.OpenApiParameter(
        'id', openapi.OpenApiTypes.INT, openapi.OpenApiParameter.PATH)],
    tags=['OrderSeller'])
class OrderPayViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    @action(
        methods=['PATCH'], detail=True, url_path=r"pay", url_name='order_pay')
    def updateOrderToPaid(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order with this id does not exist.'},
                status=status.HTTP_404_NOT_FOUND)

        order.is_paid = True
        order.paid_at = datetime.now()
        order.save()

        return Response('Order was paid.')


@extend_schema(tags=['OrdersSeller'])
class SellerOrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Get, does not work."""
    permission_classes = [IsSellerShopOrderProduct]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(
            order_item__product__seller_shop__owner=user)

    @action(
        methods=['PATCH'], detail=True,
        url_path=r"deliver", url_name='order_deliver')
    def updateOrderToDelivered(self, request, pk):
        try:
            order = Order.objects.get(
                pk=pk,
                order_item__product__seller_shop__owner=self.request.user)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order with this id does not exist.'},
                status=status.HTTP_404_NOT_FOUND)
        if order.is_paid:
            order.is_delivered = True
            order.delivered_at = datetime.now()
            order.save()

            return Response('Order was delivered')
        else:
            return Response('Order was not paid.')
