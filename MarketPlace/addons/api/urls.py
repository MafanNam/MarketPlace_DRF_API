from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

app_name = 'addons'

router = DefaultRouter()
router.register('news', views.NewsAPIView)
router.register('main', views.MainAPIView)
router.register('about', views.AboutAPIView)
router.register('licence', views.LicenceAPIView)

urlpatterns = [
    path('', include(router.urls)),
]
