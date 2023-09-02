from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return super().has_permission(request, view)


class IsSellerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated and
            obj.seller_shop.owner == request.user
        )


class IsSellerShopOrderProduct(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and request.user.is_authenticated and
            obj.order_item.product.seller_shop.owner == request.user
        )
