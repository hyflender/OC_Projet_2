# Fichier load.py pour charger les résultats dans une base de données


import pandas as pd
from sqlalchemy import create_engine


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
    df.to_sql(table_name, engine, if_exists="append", index=False)

    print("Les données ont été chargées avec succès dans la base de données SQLite.")
