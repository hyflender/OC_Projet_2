# Fichier requests_utils.py pour effectuer les requêtes HTTP et Récupération des images

import requests
from requests.exceptions import RequestException

from utils.log_config import configure_logger

log = configure_logger("requests_utils")  # Chargement du logger


def get_request(url):
    # Envoie une requête GET à l'URL spécifiée et renvoie la réponse.
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie que la requête a réussi
        response.encoding = "utf-8"
        return response

    except RequestException as e:
        log.critical(f"Erreur lors de l'envoi de la requête GET à {url}. Détails : {e}")
        return None


def get_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie que la requête a réussi
        return response

    except requests.exceptions.RequestException as e:
        log.critical(
            f"Une erreur s'est produite lors de la récupération de l'image : {e}"
        )
        return None
