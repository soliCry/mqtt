import os
from datetime import datetime


class ErrorLogger:
    def __init__(self, log_path='log/error_log.txt'):
        self.log_path = log_path

    def log_error(self, message):
        """
        This function is to record the Errors with current datetime inside the error_log.txt under log folder.
        Args:
            message: String Error Message

        Returns: NA

        """
        mode = 'a' if os.path.exists(self.log_path) else 'w'
        with open(self.log_path, mode) as f:
            f.write(f'Error occur on {datetime.now()} : {message}\n')