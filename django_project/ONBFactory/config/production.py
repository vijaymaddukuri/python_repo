import os
from .common import Common

class Production(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS
    # Site
    # https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["*"]
    INSTALLED_APPS += ("gunicorn", )

    # set the log file path
    LOG_PATH = "/var/log/tas/"
    Common.LOGGING["handlers"]["logfile"]["filename"] = os.path.join(LOG_PATH, Common.LOG_FILE_NAME)
