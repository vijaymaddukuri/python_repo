from django.contrib import admin
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls import url
from django_app.backupjob.views import EnableBackup
from rest_framework_swagger.views import get_swagger_view
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter


schema_view = get_swagger_view(title="MIDDLEWARE API")
router = DefaultRouter()

urlpatterns = [
    url(r'^$', schema_view),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    url('api/v1/service/backup/enable', EnableBackup.as_view()),
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False))]
