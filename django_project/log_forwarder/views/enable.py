from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
import logging
from log_forwarder.serializer import EnableLogForwarderSerializer
from log_forwarder.splunkmanager import SplunkSaltManager
from log_forwarder.constants import (LOG_FORWARDER_ERROR,
                                     LOG_FORWARDER_ID)
from common.exceptions import (TASException,
                              SALTException)

logger = logging.getLogger(__name__)


# Create your views here.
class Enable(generics.GenericAPIView):
    serializer_class = EnableLogForwarderSerializer

    @swagger_auto_schema(operation_id="Enable_Log_Forwarder",
                         operation_description="Enable log Forwarder on server",
                         request_body=EnableLogForwarderSerializer,
                         responses={200: 'OK',
                                    500: 'Internal server error'})
    def post(self, request, format=None):
        """
        Install Log Forwarder service on TMZ per tenant.
        """
        logger.info("{} Inside: post of Enable_Log_Forwarder".format(LOG_FORWARDER_ID))
        logger.debug("{} post of Enable_Log_Forwarder: parameters - {} "
                     .format(LOG_FORWARDER_ID, str(request.data)))
        log_forwarder_serializer = EnableLogForwarderSerializer(data=request.data)
        if not log_forwarder_serializer.is_valid():
            return Response(log_forwarder_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            post_request = log_forwarder_serializer.data
            splunk_api = SplunkSaltManager()

            # install splunk forwarder
            splunk_api.install_splunk_forwarder(post_request['VirtualMachineIPAddress'])
            return Response(None, status=status.HTTP_200_OK)

        except TASException as e:
            logger.error('|{}| {}: {}. {}'.format(LOG_FORWARDER_ID, e.err_code, e.err_message, e.err_trace))
            return Response(LOG_FORWARDER_ERROR["LOG_FWRDR009_UNABLE_INSTALL"],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except SALTException as e:
            logger.error('|{}| {}: {}'.format(LOG_FORWARDER_ID, e.error_message, e.salt_resp))
            return Response(LOG_FORWARDER_ERROR["LOG_FWRDR009_UNABLE_INSTALL"],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.exception('{} {}'.format(LOG_FORWARDER_ID, str(e)))
            return Response(LOG_FORWARDER_ERROR["LOG_FWRDR500_INTERNAL_SERVER_ERROR"],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
