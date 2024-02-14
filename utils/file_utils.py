# Fichier file_utils.py pour les fonctions utilitaires liées à la manipulation de fichiers


import os
import csv
from utils.requests_utils import get_image


def create_directory(category):
    try:
        # Vérification et création du dossier 'downloads' s'il n'existe pas
        downloads_folder = "downloads"
        if not os.path.exists(downloads_folder):
            os.makedirs(downloads_folder)

        # Vérification et création du sous-dossier pour la catégorie
        category_folder = os.path.join(downloads_folder, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        # Vérification et création du sous-dossier pour les images
        image_folder = os.path.join("downloads", category, "images")
        os.makedirs(image_folder, exist_ok=True)

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


# Fonction pour sauvegarder toutes les informations dans le fichier .CSV
def write_to_csv(books_infos):

    try:
        # Vérification que la liste n'est pas vide
        if not books_infos:
            print("Aucune information à enregistrer.")
            return

        # Création d'un dictionnaire pour regrouper les informations par catégorie
        category_books = {}
        for book_info in books_infos:
            category = book_info["Category"]
            if category not in category_books:
                category_books[category] = []
            category_books[category].append(book_info)

        # Écriture des informations de chaque catégorie dans un fichier CSV séparé
        for category, books in category_books.items():
            filename = f"{category}-all_books_info.csv"
            csv_path = os.path.join("downloads", category, filename)

            create_directory(category)

            # Écriture des informations de tous les livres dans le fichier CSV
            with open(
                file=csv_path,
                mode="w",
                newline="",
                encoding="utf-8",
            ) as csvfile:
                fieldnames = list(books[0].keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for book_info in books:
                    writer.writerow(book_info)

            print(f"Données enregistrées avec succès dans {filename}")

    except (OSError, IOError) as e:
        print(f"Erreur lors de l'enregistrement des données. Détails : {e}")


def save_picture(books_info):
    try:
        # Téléchargement et sauvegarde de l'image de chaque livre
        for book_info in books_info:
            image_url = book_info.get("Image URL")
            image_title = book_info.get("Image Title")
            category = book_info.get("Category")

            # Vérification de l'existence des dossiers
            create_directory(category)

            if image_url:
                # Nomination de la sous catégorie
                image_folder = os.path.join("downloads", category, "images")

                image_filename = os.path.join(image_folder, image_title)
                try:
                    response = get_image(image_url)

                    with open(image_filename, mode="wb") as f:
                        f.write(response.content)
                except Exception as e:
                    print(
                        f"Erreur lors du téléchargement de l'image pour {book_info.get('Title')}. Détails : {e}"
                    )
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
