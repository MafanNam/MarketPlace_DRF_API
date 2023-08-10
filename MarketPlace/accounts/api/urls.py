"""
URL mappings for the user API.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

app_name = 'accounts'

router = DefaultRouter()


urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserWithTokenView.as_view(),
         name='login_with_token'),
    path('logout/', views.LogOutUserAPIView.as_view(),
         name='logout_with_token'),
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
    path('profile/', views.UserProfileView.as_view(), name='profile')
    # path('', include(router.urls))
]
