from django.urls import include, path

from rest_framework_nested import routers

from orders.api import views

router = routers.DefaultRouter()
router.register('', views.OrderViewSet, basename='orders')
router.register('', views.OrderPayDeliverViewSet, basename='order_update_pay')

urlpatterns = [
    path('', include(router.urls)),
]
