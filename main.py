from etl import extract, transform, load
from utils import file_utils, requests_utils
from log_config import configure_logger

log = configure_logger("Scraping")  # Chargement du log


def main():
    # Extraction des URLs de toutes les catégories
    try:
        category_urls = extract.get_all_categories("https://books.toscrape.com/")
        log.info(f"Il y a {len(category_urls)} catégories de livres sur le site")
    except Exception as e:
        log.critical(
            f"Une erreur s'est produite lors de l'extraction des catégories : {e}"
        )

    # Extraction des URLs de tous les livres pour chaque catégorie
    try:
        books_urls = extract.get_all_books_in_categories(category_urls)
        log.info(f"Il y a {len(books_urls)} livres à extraire")
    except Exception as e:
        log.critical(f"Une erreur s'est produite lors de l'extraction des livres : {e}")

    # Extractions des données de chaque livres stockés dans books_urls
    try:
        data = extract.get_book_info(books_urls)
        log.info(f"Il y a {len(data)} livres analysés")
    except Exception as e:
        log.critical(f"Une erreur s'est produite lors de l'analyse des livres : {e}")

    # Transformation
    try:
        log.info("Transformation des données")
        transformed_data = transform.transform_data(data)
    except Exception as e:
        log.critical(
            f"Une erreur s'est produite lors de la transformation des données : {e}"
        )

    # Load
    try:
        file_utils.write_to_csv(transformed_data)
        file_utils.save_picture(transformed_data)

    except Exception as e:
        log.critical(
            f"Une erreur s'est produite lors de l'écriture des données dans le fichier CSV : {e}"
        )

    try:
        load.load_data_to_db(
            transformed_data, "books", "sqlite"
        )  # Load Data in Sqlite Data Base
    except Exception as e:
        log.critical(
            f"Une erreur s'est produite lors de la création de la DataBase : {e}"
        )


if __name__ == "__main__":
    main()
