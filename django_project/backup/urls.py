from backup.views import (EnableVMBackup,
                          DisableVMBackup,
                          DecommissionVMBackup,
                          PauseVMBackup,
                          ResumeVMBackup)
from django.conf.urls import url

urlpatterns = [
   url('api/v1/backup/enable', EnableVMBackup.as_view(), name='enableBackup'),
   url('api/v1/backup/disable', DisableVMBackup.as_view(), name='disableBackup'),
   url('api/v1/backup/decommission', DecommissionVMBackup.as_view(), name='decommissionBackup'),
   url('api/v1/backup/pause', PauseVMBackup.as_view(), name='pauseBackup'),
   url('api/v1/backup/resume', ResumeVMBackup.as_view(), name='resumeBackup')]

