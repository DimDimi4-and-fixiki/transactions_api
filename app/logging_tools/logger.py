__author__ = 'Dima Kalinin'
__version__ = '1.0.0'


import logging
from typing import AnyStr
from ..utilities.git_tools import get_git_signature


class IterLogger(type):
    """
    Class for Logger iteration operation
    Overwrites iter and len methods
    """

    def __iter__(cls):
        return iter(cls._allLoggers)

    def __len__(cls):
        return len(cls._allLoggers)


class Logger:

    # Collection of all Loggers objects
    _allLoggers = []

    def __init__(self, module_name, log_file_path: AnyStr = None, level=logging.DEBUG):

        # Flag if it is a first logger in the project
        self.first_logger = False

        # Update first logger flag
        if len(self._allLoggers) == 0:
            self.first_logger = True

        # Add current Logger to loggers collection
        self._allLoggers.append(self)

        # Initialize logger and set logging level
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(level)

        # If file for logging was specified
        if log_file_path is not None:

            # Add .log extension to the log file if needed
            if not log_file_path.endswith('.log'):
                log_file_path += '.log'

            # Define file handler for logger
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(logging.INFO)

            # Set logging format
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)

            # Add file handler to the logger config
            self.logger.addHandler(file_handler)

        # Define stream handler for logger
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_formatter = logging.Formatter('%(asctime)s - %(levelname)s: ------ %(message)s ------')
        stream_handler.setFormatter(stream_formatter)

        # Add stream handler to the logger config
        self.logger.addHandler(stream_handler)

        # Log git repo signature if it is a first logger in the project
        if self.first_logger:
            git_signature = get_git_signature()
            self.log(f'Logger initialized for git repo with signature {git_signature}',
                     level='info')

    def log(self, msg: str, level: str = 'debug'):

        # Logger methods for all logging levels
        logging_functions = {
            'debug': self.logger.debug,
            'info': self.logger.info,
            'error': self.logger.error,
            'critical': self.logger.critical,
            'exception': self.logger.exception
        }

        # Get logging level
        level = level.lower()

        # Log message with logger level if possible
        if level in logging_functions:
            logging_function = logging_functions[level]
            logging_function(msg)

        # Raise logging level warning
        else:
            logging_levels = list(logging_functions.keys())

            # Display logging error message
            error_message = f'Inappropriate logging level was specified - {level}, ' \
                            f'available levels are: ({", ".join(logging_levels)})'
            self.logger.warning(error_message)
