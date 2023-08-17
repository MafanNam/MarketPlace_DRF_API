from django.urls import path, include

from rest_framework.routers import DefaultRouter

from store.api import views

app_name = 'store'

router = DefaultRouter()
router.register(r"", views.ProductAPIView)

urlpatterns = [
    path('<slug>/review/', views.ProductReviewAPIView.as_view(),
         name='review'),

    path('category/', views.CategoryAPIView.as_view(),
         name='list_category'),
    path('brands/', views.BrandAPIView.as_view(),
         name='list_brand'),
    path('attribute-values/', views.AttributeValueAPIView.as_view(),
         name='list_attribute_value'),

    path('', include(router.urls))
]
