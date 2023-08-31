from django.urls import include, path

from rest_framework_nested import routers

from orders.api import views

router = routers.DefaultRouter()
router.register('', views.OrderViewSet, basename='orders')
router.register('', views.OrderPayViewSet, basename='order_update_pay')
router.register('seller', views.SellerOrderViewSet, basename='seller_order')

urlpatterns = [
    path('', include(router.urls)),
]
