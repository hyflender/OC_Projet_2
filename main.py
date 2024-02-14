from etl import extract, transform, load
from utils import file_utils, requests_utils


def main():
    # Extraction des URLs de toutes les catégories
    try:
        category_urls = extract.get_all_categories("https://books.toscrape.com/")
        print(f"Il y a {len(category_urls)} catégories de livres sur le site")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'extraction des catégories : {e}")

    # Extraction des URLs de tous les livres pour chaque catégorie
    try:
        books_urls = extract.get_all_books_in_categories(category_urls)
        print(f"Il y a {len(books_urls)} livres à extraire")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'extraction des livres : {e}")

    # Extractions des données de chaque livres stockés dans books_urls
    try:
        data = extract.get_book_info(books_urls)
        print(f"Il y a {len(data)} livres analysés")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'analyse des livres : {e}")

    # Transformation
    try:
        print("Transformation des données")
        transformed_data = transform.transform_data(data)
    except Exception as e:
        print(f"Une erreur s'est produite lors de la transformation des données : {e}")

    # Load
    try:
        file_utils.write_to_csv(transformed_data)
        # file_utils.save_picture(data)
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'écriture des données dans le fichier CSV : {e}")


if __name__ == "__main__":
    main()
