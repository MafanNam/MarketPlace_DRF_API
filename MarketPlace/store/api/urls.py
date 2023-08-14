from django.urls import path, include

from rest_framework.routers import DefaultRouter

from store.api import views

app_name = 'store'

router = DefaultRouter()
router.register(r"", views.ProductAPIView)

urlpatterns = [
    path('<slug>/review/', views.ProductReviewAPIView.as_view(),
         name='review'),
    path('create/', views.CreateProductAPIView.as_view(),
         name='create_product'),

    path('', include(router.urls))
]
