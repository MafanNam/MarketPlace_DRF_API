from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from orders.api.serializers import OrderSerializer
from orders.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
