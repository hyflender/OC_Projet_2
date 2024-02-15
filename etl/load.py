# Fichier load.py pour charger les résultats dans une base de données


import pandas as pd
from sqlalchemy import create_engine

from log_config import configure_logger

log = configure_logger("load")  # Chargement du logger


def load_data_to_db(data, table_name, db_name):
    """
    Cette fonction charge les données dans une base de données SQLite.
    :param data: Les données à charger.
    :param table_name: Le nom de la table où charger les données.
    :param db_name: Le nom de la base de données SQLite.
    """

    # Création d'un dataframe à partir des données
    df = pd.DataFrame(data)

    # Création de l'engine de la base de données SQLite
    engine = create_engine(f"sqlite:///{db_name}.db")

    # Chargement des données dans la base de données
    df.to_sql(table_name, engine, if_exists="replace", index=False)

    log.info("Les données ont été chargées avec succès dans la base de données SQLite.")


def save_data_to_csv(data, filename):
    """
    Cette fonction enregistre les données dans un fichier CSV.
    :param data: Les données à enregistrer.
    :param filename: Le nom du fichier CSV.
    """
    # Création d'un dataframe à partir des données
    df = pd.DataFrame(data)

    # Enregistrement des données dans un fichier CSV
    df.to_csv(f"downloads/{filename}.csv", index=False, encoding="utf-8")

    log.info(
        f"Les données ont été enregistrées avec succès dans le fichier {filename}.csv."
    )
