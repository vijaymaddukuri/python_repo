from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ONBFactory.service_checks import get_service_status
from ONBFactory import VERSION
import logging
from common.constants import KEY_NIMSOFT_SERVER
from common.constants import HUB_NAME
from common.functions import get_config
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
logger = logging.getLogger(__name__)

class Tas_Healthcheck(generics.GenericAPIView):
    @swagger_auto_schema(operation_id="Health_check",
                         operation_description="Health Check of Tas Services",
                         responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized',
                                    500: 'Internal server error'})
    def get(self, format=None):
        """
        Returns the tas service health.
        """
        logger.info("Inside: get of tas service health_check")
        try:
            service_status, msg_dict = get_service_status()
        except Exception as e:
            if hasattr(e, 'message'):
                err_msg = "Unable to check service status due to {}".format(e.message)
            else:
                err_msg = "Unable to check service status due to {}".format(e)
            logger.exception(err_msg)
            content = {"message": err_msg}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.info("Exit: get of tas service health_check")
        if not service_status:
            return Response(msg_dict, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(msg_dict) 

class Tas_Version(generics.GenericAPIView):
    @swagger_auto_schema(operation_id="Version_check",
                         operation_description="Check Version of Tas Service",
                         responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized',
                                    500: 'Internal server error'})
    def get(self, format=None):
        """
        Returns the tas service version.
        """
        logger.info("Inside: get of tas service version")
        logger.info("Exit: get of tas service version")
        return Response("v" + VERSION)

class Tas_Configuration_Data(generics.GenericAPIView):
    serializer_class = serializers.Serializer

    def get(self, request, format=None):
        """
        Returns the value for the key specified.
        """
        try:
            logger.info("Inside: get of Tas_Configuration_Data")
            query_params = self.request.GET['params']
            if query_params == HUB_NAME:
                param_value = get_config(KEY_NIMSOFT_SERVER, query_params)
                if not param_value:
                    return Response("Unable to get the value for the specified parameter", status=status.HTTP_404_NOT_FOUND)
                logger.info("Exit: get of Tas_Configuration_Data")
                return Response(param_value)
            return Response("Key not supported", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            if hasattr(e, 'message'):
                err_msg = "Internal server error occured due to {}".format(e.message)
            else:
                err_msg = "Internal server error occured due to {}".format(e)
            logger.exception(err_msg)
            return Response(err_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


