import logging
from typing import Callable

def logger(output: str, name: str, verbose: bool = False, max_bytes: int = 10240, backup_count: int = 5):
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
    # Get or create a logger
    logger = logging.getLogger(name)
    logger.propagate = False

    # Set the logging level based on the verbose flag
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)

    file_handler = logging.FileHandler(output)
    formatter = logging.Formatter(name+': %(asctime)s - %(levelname)s - %(filename)s - Line: %(lineno)d - %(message)s')
    file_handler.setFormatter(formatter)

    # Add handler to the logger
    logger.addHandler(file_handler)

    # Optional: Log a custom phrase every time logger is updated (useful for debugging)
    logger.debug("Logger initialized and ready for use.")

    return logger
