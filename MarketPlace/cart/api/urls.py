from django.urls import path, include

from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

app_name = 'cart'

router = DefaultRouter()
router.register('', views.CartViewSet)

cart_router = NestedDefaultRouter(router, '', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('', include(router.urls), name='cart'),
    path('', include(cart_router.urls), name='cart-item')
]
