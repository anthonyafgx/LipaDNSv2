from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5

class Logger(ABC):
    """ 
    Logger interface\n
    The levels are described as follows:\n
    **Debug**: Information only useful while debugging.\n
    **Info**: They include information about successful operations within the application, such as a successful start, pause, or exit of the application.\n
    **Warning**: Might indicate that an operation will fail in the future if action is not taken now.\n
    **Error**: This category is assigned to event logs that contain an application error message.\n
    **Critical**: This category is assigned for critical errors, such as hardware failure.\n
    """
    @abstractmethod
    def __init__(self, log_level: LogLevel):
        pass

    @abstractmethod
    def _log(self, level: LogLevel, message: str, *args: Any, **kwargs: Any):
        pass

    @abstractmethod
    def debug(self, message: str, *args: Any, **kwargs: Any):
        """Detailed information, typically only of interest to a developer trying to diagnose a problem."""
        pass

    @abstractmethod
    def info(self, message: str, *args: Any, **kwargs: Any):
        """Confirmation that things are working as expected."""
        pass

    @abstractmethod
    def warning(self, message: str, *args: Any, **kwargs: Any):
        """An indication that something unexpected happened, or that a problem might occur in the near future (e.g. ‘disk space low’). The software is still working as expected"""
        pass

    @abstractmethod
    def error(self, message: str, *args: Any, **kwargs: Any):
        """Due to a more serious problem, the software has not been able to perform some function."""
        pass

    @abstractmethod
    def critical(self, message: str, *args: Any, **kwargs: Any):
        """A serious error, indicating that the program itself may be unable to continue running."""
        pass