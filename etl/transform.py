# Fichier transform.py pour modéliser les informations

import pandas as pd


class Transform:
    def __init__(self, data) -> None:
        self.data = data

    def clear_data(self):
        df = pd.DataFrame(self.data)
        df = df.replace("", None)
        return df.to_dict(orient="records")

    def clear_price(self):
        df = pd.DataFrame(self.data)
        df["Price incl. tax"] = df["Price incl. tax"].str.extract(
            r"(\d+\.\d+)", expand=False
        )
        df["Price excl. tax"] = df["Price excl. tax"].str.extract(
            r"(\d+\.\d+)", expand=False
        )
        return df.to_dict(orient="records")

    def clear_availability(self):
        df = pd.DataFrame(self.data)
        df["Availability"] = df["Availability"].str.extract(r"(\d+)", expand=False)
        df["Availability"] = df["Availability"].fillna(0)
        return df.to_dict(orient="records")

    def uppercase_upc(self):
        df = pd.DataFrame(self.data)
        df["Universal Product Code"] = df["Universal Product Code"].str.upper()
        return df.to_dict(orient="records")

    def secure_image_title(self):
        df = pd.DataFrame(self.data)
        df["Image Title"] = df["Title"].apply(
            lambda x: "".join(e for e in x if e.isalnum()) + ".jpeg"
        )
        return df.to_dict(orient="records")

    def apply_transformation(self):
        data = self.secure_image_title(
            self.uppercase_upc(
                self.clear_availability(self.clear_price(self.clear_data(self.data)))
            )
        )
        return data
