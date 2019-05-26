from common.functions import get_config
from common.constants import (
    WORKER_PROCS,
    TAS_SVC_CHECK_CMD,
    TAS_NO_OF_PROCESSES,
)
import subprocess
import logging

logger = logging.getLogger(__name__)

def get_tas_status():
    logger.info("Inside: get_tas_status")
    cmd_output = subprocess.check_output(TAS_SVC_CHECK_CMD,
                                         shell=True).decode().strip()
    logger.debug("TAS_SVC_CHECK_CMD output :- {}".format(cmd_output))
    logger.info("Exit: get_tas_status")
    return cmd_output 

def get_tas_processes_status():
    logger.info("Inside: get_tas_processes_status")
    cmd_output = subprocess.check_output(TAS_NO_OF_PROCESSES,
                                         shell=True).decode().strip()
    logger.debug("TAS_NO_OF_PROCESSES output :- {}".format(cmd_output))
    logger.info("Exit: get_tas_processes_status")
    return cmd_output

def get_service_status():
    """
    Checks whether all the tas service components is running or not.
    """
    logger.info("Inside: get_service_status")
    no_of_workers = get_config(WORKER_PROCS, "no_of_proc")
    overall_status = True
    status_dict = {}
    status_dict["tas-service"] = {}
    status_dict["tas-service"]["status"] = True
    status_dict["tas-service"]["expected_worker_processes"] = str(no_of_workers)

    # Checking for tas service.
    if not get_tas_status()=="active":
        status_dict["tas-service"]["status"] = False
        overall_status = False

    # Checking for all tas processes status.
    out = get_tas_processes_status()
    status_dict["tas-service"]["running_worker_processes"] = str(max(0, int(out) - 1))
    if not str(no_of_workers) == status_dict["tas-service"]["running_worker_processes"]:
        overall_status = False

    logger.info("Exit: get_service_status")
    return overall_status, status_dict
