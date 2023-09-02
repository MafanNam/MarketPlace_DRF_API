from django.urls import include, path

from rest_framework_nested import routers

from orders.api import views

app_name = 'orders'

router = routers.DefaultRouter()
router.register('', views.OrderViewSet, basename='orders')
router.register('seller', views.SellerOrderViewSet, basename='seller_order')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/pay/', views.OrderPayViewSet.as_view(), name='order_pay')
]
