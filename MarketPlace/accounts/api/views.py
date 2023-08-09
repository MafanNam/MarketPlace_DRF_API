from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

import jwt

from .serializers import (
    RegisterUserSerializer, MyTokenObtainPairSerializer,
    UserSerializer, UserProfileSerializer
)

from ..models import UserProfile

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


class VerifyEmail(generics.GenericAPIView):
    """Activate user with send email jwt token link"""

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


class LoginUserWithTokenView(TokenObtainPairView):
    """Login user with jwt token"""
    serializer_class = MyTokenObtainPairSerializer


class ManagerUserView(generics.RetrieveUpdateDestroyAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class UserProfileView(generics.RetrieveUpdateAPIView,
                      viewsets.GenericViewSet):
    """User Profile view for auth user"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return UserProfile.objects.filter(pk=pk)
