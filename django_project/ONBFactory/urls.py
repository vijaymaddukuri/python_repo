from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from django.conf.urls import url
from ONBFactory.views import Tas_Healthcheck
from ONBFactory.views import Tas_Version
from ONBFactory.views import Tas_Configuration_Data
from backup.views import EnableVMBackup, DisableVMBackup

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="TAS API",
        default_version='v1',
        description="Tenant Automation Service",
        terms_of_service="https://www.VIJAY.com/use-policy",
        contact=openapi.Contact(email="vec.he@VIJAY.com"),
        license=openapi.License(name=""),
    ),
    permission_classes=[permissions.AllowAny, ],
    public=False,
    authentication_classes=[],
)

router = DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/v1/healthcheck', Tas_Healthcheck.as_view(), name="tas_healthcheck"),
    url('api/v1/version', Tas_Version.as_view(), name="tas_version"),
    path('', include('backup.urls')),
    path('', include('security.urls')),
    path('', include('monitoring.urls')),
    path('', include('log_forwarder.urls')),
    path('api/v1/', include(router.urls)),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
      name='schema-json'),
    url(r'^swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^api/v1/getconfigdata/$', Tas_Configuration_Data.as_view(), name="tas_configuration_data"),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
