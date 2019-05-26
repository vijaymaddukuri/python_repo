from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
import logging
from backup.serializer import (EnableVMBackupSerializer,
                               PauseVMBackupSerializer,
                               ResumeVMBackupSerializer,
                               DisableVMBackupSerializer,
                               DecommissionVMBackupSerializer)
from backup.networkermanager import NetworkerAPI
from backup.constants import BACKUP_ERRORS
from common.functions import get_pg_for_retention_time
from common.constants import (BACKUP_SERVICE_ERRORS,
                              BACKUP_LOG_ID,)

logger = logging.getLogger(__name__)

# Following is link for Django respose with status or error code:
#   http://www.django-rest-framework.org/api-guide/status-codes/


class EnableVMBackup(generics.GenericAPIView):
    """
    This View handles the entire process of Installing Networker Client and then enabling backup
    """
    serializer_class = EnableVMBackupSerializer

    @swagger_auto_schema(operation_id="Backup_Enable", operation_description="Enable backup on backup server",
                         request_body=EnableVMBackupSerializer,
                         responses={200: 'OK', 404: 'Backup server not found', 401: 'Unauthorized',
                                    500: 'Internal server error'})
    def post(self, request, format=None):
        """
        Enable backup on backup server
        ---

        :request: The POST request contains hostname of the Client for which backup needs to be Enabled
        :return: Appropriate HTTP response code is sent to the caller
        """
        logger.info("{} Inside: post of Enable_Backup".format(BACKUP_LOG_ID))
        logger.debug("{} post of Enable_Backup: parameters : {}".format(BACKUP_LOG_ID, str(request.data)))
        try:
            serializer = EnableVMBackupSerializer(data=request.data)
            if not serializer.is_valid():
                logger.error("{} Request Body malformed".format(BACKUP_LOG_ID))
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:

                post_request = serializer.data
                nw_api = NetworkerAPI()

                networker = nw_api.pick_networker(post_request['VirtualMachineHostName'])

                if not networker:
                    logger.error("{} Internal Server Error Occurred. Networker not selected "
                                 .format(BACKUP_LOG_ID))
                    return Response(BACKUP_SERVICE_ERRORS["NO_NETWORKER"],
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                log_networker = networker.copy()
                log_networker.pop("username")
                log_networker.pop("password")
                logger.info('{} Selected Networker: {}'.format(BACKUP_LOG_ID, log_networker))

                vm_minion_status_resp = nw_api.check_minion_status(post_request['VirtualMachineIPAddress'])
                if not vm_minion_status_resp:
                    logger.error("{} Internal Server Error Occurred. Errors: {} "
                                 .format(BACKUP_LOG_ID, BACKUP_SERVICE_ERRORS["CHECK_HOSTNAME"]))
                    return Response(BACKUP_SERVICE_ERRORS["CHECK_HOSTNAME"],
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Fetch minion id of client VM
                vm_minion_id_resp = nw_api.get_minion_name(
                    post_request['VirtualMachineIPAddress'])
                if vm_minion_id_resp['status'] is False:
                    logger.error("{} Internal Server Error Occurred. Errors: {} "
                                 .format(BACKUP_LOG_ID, vm_minion_id_resp['comment']))
                    return Response(BACKUP_SERVICE_ERRORS[500],
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                vm_minion_id = vm_minion_id_resp['minion_name']

                # Fetch PG Name
                pg_name = get_pg_for_retention_time(networker,
                                                    post_request['retentionPeriod'],
                                                    post_request['retentionPeriodType'])
                logger.debug("{} Protection Group : {} ".format(BACKUP_LOG_ID, pg_name))

                # If PG Not Found or values Invalid
                if pg_name == "":
                    logger.error("{} Protection Group not found".format(BACKUP_LOG_ID))
                    return Response(BACKUP_SERVICE_ERRORS["PG_NOT_FOUND"],
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                elif pg_name == "Invalid type":
                    logger.error("{} Invalid Retention Policy Type: {} "
                                 .format(BACKUP_LOG_ID, post_request['retentionPeriodType']))
                    return Response(BACKUP_SERVICE_ERRORS["INVALID_TYPE"],
                                    status=status.HTTP_400_BAD_REQUEST)

                # Fetch FQDN of Client VM From grains
                vm_fqdn_resp = nw_api.get_fqdn_from_minion_id(vm_minion_id)
                if not vm_fqdn_resp['status']:
                    logger.error("{} Internal Server Error Occurred. Errors: {} "
                                 .format(BACKUP_LOG_ID, vm_fqdn_resp['comment']))
                    return Response(BACKUP_SERVICE_ERRORS[500], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                vm_fqdn = vm_fqdn_resp['fqdn']

                # Install Networker Client in VM
                nw_install_response = nw_api.install_networker_agent(
                    post_request['VirtualMachineHostName'], vm_minion_id)

                # Validate Networker Installation response
                if not nw_install_response['status']:
                    logger.error("{} Internal Server Error Occurred. Errors: {} "
                                 .format(BACKUP_LOG_ID, nw_install_response['comment']))
                    return Response(BACKUP_SERVICE_ERRORS[500], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                nw_add_dns_response = nw_api.add_entry_to_host_file(
                    post_request['VirtualMachineHostName'], post_request['VirtualMachineIPAddress'],
                    vm_fqdn, networker['minionid'])

                # Validate Add DNS Step
                if not nw_add_dns_response['status']:
                    logger.error("{} Internal Server Error Occurred. Errors: {}"
                                 .format(BACKUP_LOG_ID, nw_add_dns_response['comment']))
                    return Response(BACKUP_SERVICE_ERRORS[500],
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Add Host entry on minion VM.
                host_entry_add_resp = nw_api.add_host_entry_on_minion(vm_minion_id)

                # Validate Host entry add response.
                if not host_entry_add_resp['status']:
                    logger.error("{} Internal Server Error Occurred. Errors: {} "
                                 .format(BACKUP_LOG_ID, host_entry_add_resp['comment']))
                    return Response(BACKUP_SERVICE_ERRORS[500],
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Enable Backup on VM
                nw_enable_response = nw_api.enable_backup_on_client(vm_fqdn, ['All'], pg_name, networker)
                # Validate Status
                if not nw_enable_response['status']:
                    return Response(BACKUP_SERVICE_ERRORS[500],
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                logger.info("{} Exit: post of Enable_Backup".format(BACKUP_LOG_ID))
                return Response(None, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("{} {}".format(BACKUP_LOG_ID, str(e)))
            return Response(BACKUP_SERVICE_ERRORS[500], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PauseVMBackup(generics.GenericAPIView):
    """
    This View Pause the backup service for the VM in the backup server.
    """
    serializer_class = PauseVMBackupSerializer

    @swagger_auto_schema(operation_id="Backup_Pause", operation_description="Pause the backup service for VM",
                         request_body=PauseVMBackupSerializer,
                         responses={200: 'OK', 404: 'Backup server not found', 401: 'Unauthorized',
                                    500: 'Internal server error'})
    def post(self, request, format=None):
        """
        Pause backup service on backup server
        ---

        :request: The POST request contains VM details of the Client for which
                  backup service needs to be Paused
        :return: An Appropriate HTTP response is sent to the caller
        """
        logger.info("{} Inside: post of PauseVMBackup".format(BACKUP_LOG_ID))
        logger.debug("{} post of PauseVMBackup: parameters : {}".format(BACKUP_LOG_ID, str(request.data)))
        try:
            serializer = PauseVMBackupSerializer(data=request.data)
            if not serializer.is_valid():
                logger.error("{} Request Body malformed".format(BACKUP_LOG_ID))
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:

                post_request = serializer.data
                nw_api = NetworkerAPI()
                hostname = post_request['VirtualMachineHostName']
                task_id = post_request['TaskID']
                pause_response = nw_api.pause_vm_backup_service(hostname, task_id)

                if pause_response['status'] is False:
                    logger.error("{} Internal Server Error Occurred. "
                                 "Errors: error_code - {} and error_message - {} "
                                 .format(BACKUP_LOG_ID, pause_response['err_code'],
                                         pause_response['comment']))
                    return Response(BACKUP_ERRORS["BACKUP017_PAUSE_SERVICE_FAILURE"],
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                logger.info("{} Exit: post of PauseVMBackup".format(BACKUP_LOG_ID))
                return Response(None, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("{} {}".format(BACKUP_LOG_ID, str(e)))
            return Response(BACKUP_ERRORS["BACKUP500_INTERNAL_SERVER_ERROR"],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DisableVMBackup(generics.GenericAPIView):
    """
    This View Disables the backup service for the VM in the backup server.
    """
    serializer_class = DisableVMBackupSerializer

    @swagger_auto_schema(operation_id="Backup_Disable",
                         operation_description="Disables the backup service for VM",
                         request_body=DisableVMBackupSerializer,
                         responses={200: 'OK', 404: 'Backup server not found', 401: 'Unauthorized',
                                    500: 'Internal server error'})
    def post(self, request, format=None):
        """
        Disable backup service on backup server
        ---
        :request: The POST request contains hostname of the Client for which backup needs to be disabled
        :return: Appropriate HTTP response code is sent to the caller
        :responses:
        -  Code: 200 OK
        -  Code: 404 NOT FOUND
           #### Content: { error_message : "Resource doesn't exist" }
        -  Code: 401 UNAUTHORIZED
           #### Content:{ error_message : "You are unauthorized to make this request." }
        -  Code: 500 INTERNAL SERVER ERROR
           #### Content:{ error_message : "Unexpected error occured, please contact administrator." }
        """
        logger.info("{} Inside: post of DisableVMBackup".format(BACKUP_LOG_ID))
        logger.debug("{} post of DisableVMBackup: parameters : {}"
                     .format(BACKUP_LOG_ID, str(request.data)))
        try:
            serializer = DisableVMBackupSerializer(data=request.data)
            if not serializer.is_valid():
                logger.error("{} Request Body malformed".format(BACKUP_LOG_ID))
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:

                post_request = serializer.data
                nw_api = NetworkerAPI()
                hostname = post_request['VirtualMachineHostName']
                task_id = post_request['TaskID']
                disable_response = nw_api.disable_vm_backup_service(
                    hostname, post_request['VirtualMachineIPAddress'], task_id)

                if disable_response['status'] is False:
                    logger.error("{} Internal Server Error Occurred. Errors: "
                                 "error_code - {} and error_message - {} "
                                 .format(BACKUP_LOG_ID, disable_response['err_code'],
                                         disable_response['comment']))
                    return Response(BACKUP_ERRORS["BACKUP019_DISABLE_SERVICE_FAILURE"],
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                logger.info("{} Exit: post of DisableVMBackup".format(BACKUP_LOG_ID))
                return Response(None, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("{} {}".format(BACKUP_LOG_ID, str(e)))
            return Response(BACKUP_ERRORS["BACKUP500_INTERNAL_SERVER_ERROR"],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DecommissionVMBackup(generics.GenericAPIView):
    """
    This View Decommissions the backup service for the VM in the backup server.
    """
    serializer_class = DecommissionVMBackupSerializer

    @swagger_auto_schema(operation_id="Backup_Decommission",
                         operation_description="Disables backup service for a VM to be decommissioned",
                         request_body=DecommissionVMBackupSerializer,
                         responses={200: 'OK', 404: 'Backup server not found', 401: 'Unauthorized',
                                    500: 'Internal server error'})
    def post(self, request, format=None):
        """
        Decommission backup service on backup server
        ---
        :request: The POST request contains hostname of the Client
                  for which backup needs to be disabled
        :return: Appropriate HTTP response code is sent to the caller
        :responses:
        -  Code: 200 OK
        -  Code: 404 NOT FOUND
           #### Content: { error_message : "Resource doesn't exist" }
        -  Code: 401 UNAUTHORIZED
           #### Content:{ error_message : "You are unauthorized to make this request." }
        -  Code: 500 INTERNAL SERVER ERROR
           #### Content:{ error_message : "Unexpected error occured, please contact administrator." }
        """
        logger.info("{} Inside: post of DecommissionVMBackup".format(BACKUP_LOG_ID))
        logger.debug("{} post of DecommissionVMBackup: parameters : {}"
                     .format(BACKUP_LOG_ID, str(request.data)))
        try:
            serializer = DecommissionVMBackupSerializer(data=request.data)
            if not serializer.is_valid():
                logger.error("{} Request Body malformed".format(BACKUP_LOG_ID))

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                post_request = serializer.data
                nw_api = NetworkerAPI()
                hostname = post_request['VirtualMachineHostName']
                task_id = post_request['TaskID']
                response = nw_api.decommission_vm_backup_service(hostname, task_id)

                if response['status'] is False:
                    logger.error("{} Internal Server Error Occurred. Errors: "
                                 "error_code - {} and error_message - {} "
                                 .format(BACKUP_LOG_ID, response['err_code'], response['comment']))
                    return Response(BACKUP_ERRORS["BACKUP020_DECOMMISSION_SERVICE_FAILURE"],
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                logger.info("{} Exit: post of DecommissionVMBackup".format(BACKUP_LOG_ID))
                return Response(None, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("{} {}".format(BACKUP_LOG_ID, str(e)))
            return Response(BACKUP_ERRORS["BACKUP500_INTERNAL_SERVER_ERROR"],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResumeVMBackup(generics.GenericAPIView):
    """
    This View Resume the backup service for the VM in the backup server.
    """
    serializer_class = ResumeVMBackupSerializer

    @swagger_auto_schema(operation_id="Backup_Resume",
                         operation_description="Resume the backup service for VM",
                         request_body=ResumeVMBackupSerializer,
                         responses={200: 'OK', 404: 'Backup server not found', 401: 'Unauthorized',
                                    500: 'Internal server error'})
    def post(self, request, format=None):
        """
        Resume backup service on backup server
        ---
        :request: The POST request contains VM details of the Client for which
                  backup service needs to be resumed
        :return: Appropriate HTTP response code is sent to the caller
        """
        logger.info("{} Inside: post of ResumeVMBackup".format(BACKUP_LOG_ID))
        logger.debug("{} post of ResumeVMBackup: parameters : {}".format(BACKUP_LOG_ID, str(request.data)))
        try:
            serializer = ResumeVMBackupSerializer(data=request.data)
            if not serializer.is_valid():
                logger.error("{} Request Body malformed".format(BACKUP_LOG_ID))
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            post_request = serializer.data
            nw_api = NetworkerAPI()
            hostname = post_request['VirtualMachineHostName']
            task_id = post_request['TaskID']
            resume_response = nw_api.resume_vm_backup_service(hostname, task_id)

            if not resume_response['status']:
                logger.error("{} Internal Server Error Occurred. Errors: "
                             "error_code - {} and error_message - {} "
                             .format(BACKUP_LOG_ID, resume_response['err_code'], resume_response['comment']))
                return Response(BACKUP_ERRORS["BACKUP018_RESUME_SERVICE_FAILURE"],
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info("{} Exit: post of ResumeVMBackup".format(BACKUP_LOG_ID))
            return Response(None, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("{} {}".format(BACKUP_LOG_ID, str(e)))
            return Response(BACKUP_ERRORS["BACKUP500_INTERNAL_SERVER_ERROR"],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
