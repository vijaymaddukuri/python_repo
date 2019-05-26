from django.urls import path
from monitoring.views.enable import EnableMonitoring
from monitoring.views.disable import DisableMonitoring
from django.conf.urls import url

urlpatterns = [
    url('api/v1/monitoring/enable', EnableMonitoring.as_view(), name='enable_monitoring'),
    url('api/v1/monitoring/disable', DisableMonitoring.as_view(), name='disable_monitoring')
    ]
