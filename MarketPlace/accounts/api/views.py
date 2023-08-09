from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    RegistrationUserSerializer,
    MyTokenObtainPairSerializer, UserSerializer, UserProfileSerializer
)

from ..models import UserProfile


class RegisterUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = RegistrationUserSerializer
    permission_classes = (AllowAny,)


class LoginUserWithTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ManagerUserView(generics.RetrieveUpdateDestroyAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class UserProfileView(generics.RetrieveUpdateDestroyAPIView,
                      viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return UserProfile.objects.filter(pk=pk)
