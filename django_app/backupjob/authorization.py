from rest_framework.response import Response
from rest_framework import status
from common.functions import get_config
from common.constants import KEY_MIDDLEWARE_SERVICE, AUTHORIZATION_ERRORS
import logging
import base64

logger = logging.getLogger(__name__)


def basicauth(function):
    """ This decorator is to authorize the credentials provided
        :param function: Function name before which, this decorator is called
        :return: rest framework response
        :except: Exception in authorization
     """

    def wrap(instance, request, *args, **kwargs):
        logger.info("Inside: Basic Authorization decorator")

        try:
            username = get_config(KEY_MIDDLEWARE_SERVICE, "username")
            password = get_config(KEY_MIDDLEWARE_SERVICE, "password")

            # If header found, proceed further, else return error response
            if 'HTTP_AUTHORIZATION' not in request.META:
                response = AUTHORIZATION_ERRORS["AUTH_HEADER_NOT_FOUND"]
                auth_status = status.HTTP_400_BAD_REQUEST
                logger.error("Authorization failed. Details: " + response)
                return Response(response, auth_status)

            # If Auth header contains 2 strings, proceed further.
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) != 2:
                response = AUTHORIZATION_ERRORS["INCORRECT_AUTH_HEADER"]
                auth_status = status.HTTP_400_BAD_REQUEST
                logger.error("Authorization failed. Details: " + response)
                return Response(response, auth_status)

            # If the Authorization type is not Basic, return error message
            if auth[0].lower() != "basic":
                response = AUTHORIZATION_ERRORS["UNSUPPORTED_AUTH_TYPE"]
                auth_status = status.HTTP_401_UNAUTHORIZED
                logger.error("Authorization failed. Details: " + response)
                return Response(response, auth_status)

            # Validate username and password
            uname, passwd = base64.b64decode(auth[1]).decode('ASCII').split(":")
            if str(uname) == username and str(passwd).strip("'") == password:
                logger.info("Authorization is successful, with the status: " + str(status.HTTP_200_OK))
                logger.info("Exit: basicauth Decorator")
                return function(instance, request, *args, **kwargs)
            else:
                response = AUTHORIZATION_ERRORS["INCORRECT_CREDENTIALS"]
                auth_status = status.HTTP_401_UNAUTHORIZED
                logger.error("Authorization failed. Details: " + response)
                return Response(response, auth_status)

        except Exception as e:
            logger.exception("Authorization failed. Details: " + str(e))
            return Response(AUTHORIZATION_ERRORS["GENERIC_SERVER_ERROR"],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrap
