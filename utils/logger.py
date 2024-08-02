from os import path
from config.variables import LOG_PATH
import logging


def logger(name: str, verbose: bool = False, max_bytes: int = 10240, backup_count: int = 5):
    """
    Creates a logger for logging to a file with rotation.

    Args:
        output (str): The filename for the log.
        name (str): Name prefix for log entries.
        verbose (bool): Flag to set logging level. True for debug, False for error.
        max_bytes (int): Maximum file size in bytes before rotation.
        backup_count (int): Number of backup files to keep.

    Returns:
        logging.Logger: Configured logger with rotation and custom formatting.
    """
    logger_ = logging.getLogger(name)
    logger_.propagate = False

    if verbose:
        logger_.setLevel(logging.DEBUG)
    else:
        logger_.setLevel(logging.WARNING)

    file_handler = logging.FileHandler(path.join(LOG_PATH, name))
    formatter = logging.Formatter(name+': %(asctime)s - %(levelname)s - %(filename)s - Line: %(lineno)d - %(message)s')
    file_handler.setFormatter(formatter)

    logger_.addHandler(file_handler)
    logger_.debug(f" === Logger {name} initialized and ready for use === ")

    return logger_
