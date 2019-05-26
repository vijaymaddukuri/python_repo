from django.conf.urls import url
from log_forwarder.views.enable import Enable

urlpatterns = [
    url('api/v1/logforwarder/enable', Enable.as_view(), name='enable_log_forwarder'),
]
