from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

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


class OrderPayDeliverViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

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

    # @action(
    #     methods=['PATCH'], detail=True,
    #     url_path=r"deliver", url_name='order_deliver')
    # @permission_classes([IsSellerShop])
    # def updateOrderToDelivered(self, request, pk):
    #     order = Order.objects.get(pk=pk)
    #
    #     order.is_delivered = True
    #     order.delivered_at = datetime.now()
    #     order.save()
    #
    #     return Response('Order was delivered')
