import logging


def configure_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Gestionnaire de fichier
    file_handler = logging.FileHandler("debug.log")
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Gestionnaire de flux
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Ajouter les gestionnaires au logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
