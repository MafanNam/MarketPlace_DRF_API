from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.api.serializers import OrderSerializer, CreateOrderSerializer
from orders.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

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
        return OrderSerializer

    # def get_serializer_context(self):
    #     context = {'user': self.request.user}
    #     return context
