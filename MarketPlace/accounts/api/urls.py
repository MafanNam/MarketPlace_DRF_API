"""
URL mappings for the user API.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

app_name = 'accounts'

router = DefaultRouter()
router.register('profile', views.UserProfileView)

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserWithTokenView.as_view(), name='login_with_token'),
    path('user/', views.ManagerUserView.as_view(), name='user'),

    path('', include(router.urls))

    # path('profile/', views.UserProfileView.as_view(), name='profile')
]