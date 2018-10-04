from auc.baseusecase import BaseUseCase
from robot.api import logger


class ValidateEnableBackupFromWorkerLogs(BaseUseCase):
    def validate_enable_backup_from_worker_logs(self, search_text, log_file_path):
        if log_file_path is None:
            logger.debug("No file name provided!")
            return None
        else:
            try:
                with open(log_file_path, 'rb') as lf:
                    found = False if len([line for line in lf.readlines() if search_text in line])\
                                       == 0 else True
                    return found
            except (IOError, ValueError) as e:
                logger.debug("Exception while reading file,Exception: %s" % e)
                return None

    def run_test(self, search_text, log_file_path):
        self.validate_enable_backup_from_worker_logs(search_text, log_file_path)
