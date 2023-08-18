from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/users/', include('accounts.api.urls')),

    path('api/products/', include('store.api.urls')),


    # ADDONS
    path('api/addons/', include('addons.api.urls')),

    # DOCS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),

    path('api/drf-auth/', include('rest_framework.urls'))

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
