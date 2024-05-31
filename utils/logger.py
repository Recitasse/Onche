import logging
from typing import Callable

def logger(output: str, name: str, verbose: bool):
    """Créer la fonction logger pour tout les fichiers

    Args:
        output (str): output du log
    """
    logger = logging.getLogger(__name__)
    logger.propagate = False
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)

    file_handler = logging.FileHandler(output)
    formatter = logging.Formatter(name+': %(asctime)s - %(levelname)s - %(filename)s - Line: %(lineno)d - %(message)s')

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
