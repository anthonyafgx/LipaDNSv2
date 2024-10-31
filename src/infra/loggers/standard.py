import logging
import logging.handlers
from typing import Any
from src.infra.loggers.interface import Logger, LogLevel

class StandardLogger(Logger):
    """
    Logger implementation that uses the Standard "Logging" Library.
    """
    def __init__(self, log_level: LogLevel):
        logging_level: Any

        match log_level:
            case LogLevel.DEBUG:
                logging_level = logging.DEBUG
            case LogLevel.INFO:
                logging_level = logging.INFO
            case LogLevel.WARNING:
                logging_level = logging.WARNING
            case LogLevel.ERROR:
                logging_level = logging.ERROR
            case LogLevel.CRITICAL:
                logging_level = logging.CRITICAL
            case _: # type: ignore
                logging_level = logging.DEBUG
        
        formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        timed_file_handler = logging.handlers.TimedRotatingFileHandler(
            filename='logs\\logs.txt',
            when='midnight',
            backupCount=0,
            utc=False)
        timed_file_handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(timed_file_handler)
        logger.setLevel(logging_level)

    def _log(self, level: LogLevel, message: str, *args: Any, **kwargs: Any):
        pass

    def debug(self, message: str, *args: Any, **kwargs: Any):
        logging.debug(message, *args, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any):
        logging.info(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any):
        logging.warning(message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any):
        logging.error(message, *args, **kwargs)

    def critical(self, message: str, *args: Any, **kwargs: Any):
        logging.critical(message, *args, **kwargs)
        