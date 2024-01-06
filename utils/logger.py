import logging

def logger(output: str, name: str):
    """Créer la fonction logger pour tout les fichiers

    Args:
        output (str): output du log
    """
    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    # Create file handler for output to a file
    file_handler = logging.FileHandler(output)
    formatter = logging.Formatter(name+': %(asctime)s - %(levelname)s - %(filename)s - Line: %(lineno)d - %(message)s')
    
    # AJout du format
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
