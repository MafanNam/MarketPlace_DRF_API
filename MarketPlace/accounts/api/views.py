from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import (
    smart_bytes, smart_str,
    DjangoUnicodeDecodeError
)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from drf_spectacular.utils import extend_schema
from drf_spectacular import openapi

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from .serializers import (
    RegisterUserSerializer, UserSerializer, UserProfileSerializer,
    ResetPasswordEmailSerializer, SetNewPasswordSerializer,
    EmailVerificationSerializer, PasswordTokenCheckSerializer,
    SellerShopProfileSerializer, RegisterSellerShopUserSerializer,
)
from ..models import UserProfile, SellerShop
from .utils import Util


class RegisterUserView(generics.GenericAPIView):
    """Create(register) a new user in the system."""
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = get_user_model().objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('accounts:email_activate')
        abs_url = 'http://' + current_site + relative_link + \
                  '?token=' + str(token)
        email_body = 'Hi ' + user.get_full_name() + \
                     ' Use link below to verify your email. \n' + abs_url

        data = {'email_body': email_body,
                'email_subject': 'Verify your email',
                'to_email': user.email}
        Util.send_verification_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class RegisterSellerShopView(RegisterUserView):
    """Create(register) a new Seller Shop user in the system."""
    serializer_class = RegisterSellerShopUserSerializer


class VerifyEmail(APIView):
    """Activate user with send email jwt token link"""
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.OpenApiParameter(
        'token', openapi.OpenApiTypes.STR)

    @extend_schema(parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
            user = get_user_model().objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
                return Response({'email': 'Successfully activated.'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'email': 'Already activated.'},
                                status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid Token.'},
                            status=status.HTTP_400_BAD_REQUEST)


class ManagerUserView(generics.RetrieveUpdateDestroyAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class RequestResetPasswordEmail(generics.GenericAPIView):
    """Request reset password with send email"""
    serializer_class = ResetPasswordEmailSerializer

    def post(self, request):
        data = {'request': request, 'data': request.data}
        self.serializer_class(data=data)

        email = request.data['email']
        if get_user_model().objects.filter(email=email).exists():
            user = get_user_model().objects.get(email__exact=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(
                request=request).domain
            relative_link = reverse(
                'accounts:password_reset_confirm',
                kwargs={'uidb64': uidb64, 'token': token})
            abs_url = 'http://' + current_site + relative_link
            email_body = 'Hello, \n Use link below to resset your password. \n' + abs_url

            data = {'email_body': email_body,
                    'email_subject': 'Resset your Password',
                    'to_email': user.email}
            Util.send_verification_email(data)

            return Response(
                {'success': 'We have sent you a link to resset your password.'},
                status=status.HTTP_200_OK)

        return Response(
            {'error': 'User with this email is not register.'},
            status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    """Check password valid token"""
    serializer_class = PasswordTokenCheckSerializer

    token_param_config = openapi.OpenApiParameter(
        'token', openapi.OpenApiTypes.STR,
        openapi.OpenApiParameter.PATH)
    uidb64_param_config = openapi.OpenApiParameter(
        'uidb64', openapi.OpenApiTypes.STR,
        openapi.OpenApiParameter.PATH)

    @extend_schema(parameters=[token_param_config, uidb64_param_config])
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'error': 'Token is not valid, please request a new one.'},
                    status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credential Valid',
                             'uidb64': uidb64, 'token': token, },
                            status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response(
                {'error': 'Token is not valid, please request a new one.'},
                status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    """Set new password for user"""
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            {'success': True, 'message': 'Password reset success.'},
            status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User Profile view for auth user"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.all().select_related('user').get(
            user=self.request.user)


class SellerShopProfileView(generics.RetrieveUpdateAPIView):
    """User Profile view for auth user"""
    serializer_class = SellerShopProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return SellerShop.objects.all().select_related('owner').get(
            owner=self.request.user)
