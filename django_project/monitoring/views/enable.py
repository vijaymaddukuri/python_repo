from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from monitoring.serializer import MonitoringSerializer
from monitoring.nimsoftmanager import NimsoftAPI
from monitoring.constants import MONITORING_ERRORS
import logging
from common.constants import MONITORING_LOG_ID
from drf_yasg.utils import swagger_auto_schema
from common.exceptions import (TASException,
                               SALTException)

logger = logging.getLogger(__name__)


# Create your views here.
class EnableMonitoring(generics.GenericAPIView):
    serializer_class = MonitoringSerializer

    @swagger_auto_schema(operation_id="Monitoring_Enable",
                         operation_description="Enable monitoring on server",
                         request_body=MonitoringSerializer,
                         responses={200: 'OK',
                                    500: 'Internal server error'})
    def post(self, request, format=None):
        """
        Install Monitoring service on TMZ per tenant.
        """
        logger.info("{} Inside: post of EnableMonitoring".format(MONITORING_LOG_ID))
        logger.debug("{} post of EnableMonitoring: parameters - {} "
                     .format(MONITORING_LOG_ID, str(request.data)))
        monitorserializer = MonitoringSerializer(data=request.data)
        if not monitorserializer.is_valid():
            return Response(monitorserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            post_request = monitorserializer.data
            ns_api = NimsoftAPI()

            # install nimsoft agent
            ns_api.install_nimsoft_agent(post_request['VirtualMachineHostName'],
                                         post_request['VirtualMachineIPAddress'])
            return Response(None, status=status.HTTP_200_OK)
        except TASException as e:
            logger.error('|{}| {}: {}. {}'.format(MONITORING_LOG_ID, e.err_code, e.err_message, e.err_trace))
            return Response(MONITORING_ERRORS["MON009_UNABLE_INSTALL"],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except SALTException as e:
            logger.error('|{}| {}: {}'.format(MONITORING_LOG_ID, e.error_message, e.salt_resp))
            return Response(MONITORING_ERRORS["MON009_UNABLE_INSTALL"],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.exception('{} {}'.format(MONITORING_LOG_ID, str(e)))
            return Response(MONITORING_ERRORS["MON500_INTERNAL_SERVER_ERROR"],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
