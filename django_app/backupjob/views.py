from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from backupjob.serializer import BackupSerializer
from backupjob.message_handler import MessageHandlerService
from backupjob.rabbitmq import RabbitMq
from backupjob.authorization import basicauth
import logging
import json

logger = logging.getLogger(__name__)


class EnableBackup(generics.GenericAPIView):
    """
    post:
        Enable backup for the given Virtual Machine
    """
    # Unused instance so that django will render the class parameters.
    serializer_class = BackupSerializer

    @basicauth
    def post(self, request, format=None):
        """
        This Post method will request for enable  backup
        :param request: Request object
        :param format: Json
        :return: Json response
        """
        logger.info("Inside: post of enable backup")
        logger.debug("POST of enable backup is initiated with the parameters: " + json.dumps(request.data))

        backupserializer = BackupSerializer(data=request.data)
        if not backupserializer.is_valid():
            return Response(backupserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Publish job to the message broker code goes here.
            input_dict = request.data
            client = MessageHandlerService(RabbitMq())
            client.handle_message(input_dict)
            ret_dict = {"message": "Backup job initiated"}

            logger.info("Exit: post of enable backup")
            return Response(ret_dict)
        except Exception as e:
            if hasattr(e, 'message'):
                err_msg = "Unable to initiate the backup due to {}".format(e.message)
            else:
                err_msg = "Unable to initiate the backup due to {}".format(e)
            logger.exception(err_msg)
            content = {"Message": err_msg}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
