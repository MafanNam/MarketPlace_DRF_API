from rest_framework import viewsets, mixins

from MarketPlace.core.permissions import IsAdminOrReadOnly
from addons.models import News, Main, Licence, About
from .serializers import (
    NewsSerializer, LicenceSerializer,
    AboutSerializer, MainSerializer,
)


class BaseAddonsAPIView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnly]


class NewsAPIView(BaseAddonsAPIView):
    """News view for List, Retrieve"""
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class MainAPIView(BaseAddonsAPIView):
    """Main view for List, Retrieve"""
    queryset = Main.objects.all()
    serializer_class = MainSerializer


class LicenceAPIView(BaseAddonsAPIView):
    """Licence view for List, Retrieve"""
    queryset = Licence.objects.all()
    serializer_class = LicenceSerializer


class AboutAPIView(BaseAddonsAPIView):
    """About view for List, Retrieve"""
    queryset = About.objects.all()
    serializer_class = AboutSerializer
