import logging


def configure_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:  # Pour éviter les duplications
        logger.setLevel(logging.INFO)

        # Gestionnaire de fichier
        file_handler = logging.FileHandler("debug.log", encoding="utf-8")
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
