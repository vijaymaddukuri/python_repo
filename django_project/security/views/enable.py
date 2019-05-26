from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from security.serializer import EnableSerializer
from security.trendmicromanager import TrendMicroAPI
from security.constants import SECURITY_ERRORS
import logging
from drf_yasg.utils import swagger_auto_schema
from common.constants import SECURITY_LOG_ID, SALT_MINION_ERRORS
logger = logging.getLogger(__name__)


class Enable(generics.GenericAPIView):
    """
    This View handles the entire process of Installing trend micro and then enabling the security
    """
    serializer_class = EnableSerializer

    @swagger_auto_schema(operation_id="Security_Enable", operation_description="Enable security on server",
                         request_body=EnableSerializer,
                         responses={200: 'OK', 400: 'Bad request',
                                    500: 'Internal server error'})
    def post(self, request, format=None):
        """
        Enable security on Deep security Manager(DSM) server
        ---

        :request: The POST request contains hostname of the Client for which security needs to be Enabled
        :return: An Appropriate REST response is sent to the caller
        :responses:
        -  Code: 200 OK
        -  Code: 400 NOT FOUND
           #### Content: { error_message : "Bad Request" }
        -  Code: 500 INTERNAL SERVER ERROR
           #### Content:{ error_message : "Unexpected error occured, please contact administrator." }
        """
        logger.info("{} Inside: post of Enable_Security".format(SECURITY_LOG_ID))
        logger.debug("{} post of Enable_Security: parameters - {} ".format(SECURITY_LOG_ID, str(request.data)))
        serializer = EnableSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error("{} Request Body malformed".format(SECURITY_LOG_ID))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            post_request = serializer.data
            tm_api = TrendMicroAPI()

            # Check if client vm is up and running
            vm_minion_status_resp = tm_api.check_minion_status(post_request['VirtualMachineIPAddress'])
            if not vm_minion_status_resp:
                logger.error("{} Internal Server Error Occurred. Errors: {} "
                             .format(SECURITY_LOG_ID, SECURITY_ERRORS["SEC008_CHECK_VM_STATUS"]))
                return Response(SECURITY_ERRORS["SEC008_CHECK_VM_STATUS"], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Install and enable trend micro in VM
            tm_enable_response = tm_api.enable_security(
                post_request['VirtualMachineHostName'], post_request['VirtualMachineIPAddress'],
                post_request['LinuxPolicyID'], post_request['WindowsPolicyID'])

            # Validate security Installation response
            if not tm_enable_response['status']:
                return Response(SECURITY_ERRORS["SEC003_TREND_MICRO_AGENT_INSTALL_FAILURE"], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info("{} Exit: post of Enable_Security".format(SECURITY_LOG_ID))
            return Response(None, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception('{} {}'.format(SECURITY_LOG_ID, str(e)))
            return Response(SECURITY_ERRORS["SEC500_INTERNAL_SERVER_ERROR"],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
