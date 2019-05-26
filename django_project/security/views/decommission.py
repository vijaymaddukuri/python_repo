from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from security.serializer import DecommissionSerializer
from security.trendmicromanager import TrendMicroAPI
from security.constants import SECURITY_ERRORS
import logging
from drf_yasg.utils import swagger_auto_schema
from common.constants import SECURITY_LOG_ID, SALT_MINION_ERRORS
from common.utils import RestClient
logger = logging.getLogger(__name__)


class Decommission(generics.GenericAPIView):
    """
    This View handles the process of removing security from trend micro.
    """
    serializer_class = DecommissionSerializer

    @swagger_auto_schema(operation_id="Decommission", operation_description="Decommission security on server",
                         request_body=DecommissionSerializer,
                         responses={200: 'OK', 400: 'Bad request',
                                    500: 'Internal server error'})
    def post(self, request, format=None):
        """
        Decommission security on Deep security Manager(DSM) server
        ---
        :request: The POST request contains hostname of the Client for which security needs to be Enabled
        :return: An Appropriate REST response is sent to the caller
        :responses:
        -  Code: 200 OK
        -  Code: 400 Bad Rquest
           #### Content: { error_message : "Bad Request" }
        -  Code: 404 Not found
        -  Code: 500 INTERNAL SERVER ERROR
           #### Content:{ error_message : "Unexpected error occured, please contact administrator." }
        """
        logger.info("{} Inside: post of Decommission_Security".format(SECURITY_LOG_ID))
        logger.debug("{} post of Decommission_Security: parameters - {} ".format(SECURITY_LOG_ID, str(request.data)))
        serializer = DecommissionSerializer(data=request.data)
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

            tm_resp = tm_api.get_dsm_response(post_request['VirtualMachineIPAddress'])[1]
            tm_resp_json = tm_resp.json()
            if not tm_resp_json["computers"]:
                msg = "No computer found with the hostname {}".format(post_request['VirtualMachineHostName'])
                logger.info(msg)
                return Response(msg, status=status.HTTP_404_NOT_FOUND)

            computer_id = RestClient.getFromDict(tm_resp_json, ['computers', 0, 'ID'])
            logger.info("computer_id : {}".format(computer_id))
            tm_decommission_response = tm_api.delete_computer(computer_id)

            logger.info("{} Exit: post of Decommission_Security".format(SECURITY_LOG_ID))
            return Response(None, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception('{} {}'.format(SECURITY_LOG_ID, str(e)))
            return Response(SECURITY_ERRORS["SEC500_INTERNAL_SERVER_ERROR"],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
