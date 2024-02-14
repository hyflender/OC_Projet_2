# Fichier transform.py pour modéliser les informations

import pandas as pd


def clear_data(data):
    df = pd.DataFrame(data)
    df = df.replace("", None)
    return df.to_dict(orient="records")


def clear_price(data):
    df = pd.DataFrame(data)
    df["Price incl. tax"] = df["Price incl. tax"].str.extract(
        r"(\d+\.\d+)", expand=False
    )
    df["Price excl. tax"] = df["Price excl. tax"].str.extract(
        r"(\d+\.\d+)", expand=False
    )
    return df.to_dict(orient="records")


def clear_availability(data):
    df = pd.DataFrame(data)
    df["Availability"] = df["Availability"].str.extract(r"(\d+)", expand=False)
    df["Availability"] = df["Availability"].fillna(0)
    return df.to_dict(orient="records")


def uppercase_upc(data):
    df = pd.DataFrame(data)
    df["Universal Product Code"] = df["Universal Product Code"].str.upper()
    return df.to_dict(orient="records")


def transform_data(data):
    data = clear_data(data)
    data = clear_price(data)
    data = clear_availability(data)
    data = uppercase_upc(data)
    return data
