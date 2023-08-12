"""
URL mappings for the user API.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from . import views

app_name = 'accounts'

router = DefaultRouter()

urlpatterns = [
    # Auth
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('register-seller-shop/', views.RegisterSellerShopView.as_view(),
         name='register_seller_shop'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # User
    path('user/', views.ManagerUserView.as_view(), name='user'),

    # Verification Email
    path('email-activate/', views.VerifyEmail.as_view(),
         name='email_activate'),

    # Resset Password
    path('password-resset-request/', views.RequestResetPasswordEmail.as_view(),
         name='request_resset_password'),
    path('password-reset/<uidb64>/<token>/',
         views.PasswordTokenCheckAPI.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(),
         name='password_reset_complete'),

    # Profile
    path('profile/', views.UserProfileView.as_view(), name='profile'),

    # Seller Shop
    path('seller-shop-profile/', views.SellerShopProfileView.as_view(),
         name='seller_shop_profile')

    # path('', include(router.urls))
]
