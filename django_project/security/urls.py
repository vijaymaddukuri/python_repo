from security.views.enable import Enable
from security.views.decommission import Decommission
from django.conf.urls import url

urlpatterns = [
   url('api/v1/security/enable', Enable.as_view(), name = 'enableSecurity'),
   url('api/v1/security/decommission', Decommission.as_view(), name='decommissionSecurity'),
]

