# from drf_spectacular.utils import extend_schema

# from django.utils.timezone import now
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from orders.api.paginations import OrderAPIListPagination
# from rest_framework.decorators import action

# from MarketPlace.core.permissions import IsSellerShop
from orders.api.serializers import (
    OrderSerializer, CreateOrderSerializer,
    UpdateOrderSerializer)
from orders.models import Order

from datetime import datetime


class OrderViewSet(viewsets.ModelViewSet):
    """Order view"""
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = OrderAPIListPagination
    filter_backends = (SearchFilter,)
    search_fields = ('order_number', 'status')

    def get_permissions(self):
        if self.request.method in ['PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        context = {'user': self.request.user}
        serializer = CreateOrderSerializer(
            data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer


class OrderPayViewSet(viewsets.views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def patch(self, request, pk=None):
        try:
            order = Order.objects.get(
                pk=pk, user=self.request.user)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order with this id does not exist.'},
                status=status.HTTP_404_NOT_FOUND)
        if not order.is_paid:
            order.is_paid = True
            order.paid_at = datetime.now()
            order.save()
        else:
            return Response({'error': 'Order already paid.'})

        return Response('Order was paid.')

# @extend_schema(tags=['OrdersSeller'])
# class SellerOrderViewSet(generics.ListAPIView):
#     """Get, does not work."""
#     permission_classes = [IsSellerShop]
#     serializer_class = OrderSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user:
#             return Order.objects.all()
#         return Order.objects.filter(
#             order_item__product__seller_shop__owner=user)
#
#     @action(
#         methods=['PATCH'], detail=True,
#         url_path=r"deliver", url_name='order_deliver')
#     def updateOrderToDelivered(self, request, pk):
#         try:
#             order = Order.objects.get(
#                 pk=pk,
#                 order_item__product__seller_shop__owner=self.request.user)
#         except Order.DoesNotExist:
#             return Response(
#                 {'error': 'Order with this id does not exist.'},
#                 status=status.HTTP_404_NOT_FOUND)
#         if order.is_paid:
#             order.is_delivered = True
#             order.delivered_at = now()
#             order.save()
#
#             return Response('Order was delivered')
#         else:
#             return Response('Order was not paid.')

# class SelOrder(viewsets.generics.ListAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
