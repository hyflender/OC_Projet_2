import requests
import csv
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor


def get_all_categories(url="https://books.toscrape.com"):
    try:
        response = requests.get(url)  # Récupération de la réponse par requête GET
        response.raise_for_status()  # Lève une exception pour les erreurs HTTP

        # Utilisation de html.parser pour le parsing HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Récupération des liens de toutes les catégories dans la navigation avec la classe "nav-list"
        category_links = soup.select("ul.nav.nav-list ul li a")

        # Mise en forme des URLs par urljoin
        category_urls = [urljoin(url, link["href"]) for link in category_links]

        return category_urls

    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la récupération des catégories. Détails : {e}"


# Fonction pour récupérer tous les livres présents dans chaque catégorie
def get_all_books_in_category(category_urls):
    all_books_info = []  # Pour compter le nombre maximum de livres

    def fetch_books(url):
        books_in_category = []
        category = url.split("/")[-2]

        while url:  # boucle pour les pages suivantes
            try:
                response = requests.get(
                    url
                )  # Récupération de la réponse par requête GET
                response.raise_for_status()  # Lève une exception pour les erreurs HTTP

                # Utilisation de html.parser pour le parsing HTML
                soup = BeautifulSoup(response.text, "html.parser")

                book_links = soup.select("ol.row h3 a[href]")

                for link in book_links:
                    book_url = urljoin(url, link["href"])

                    book_infos = book_info(book_url)
                    all_books_info.append(book_infos)
                    books_in_category.append(book_infos)

                # Recherche de pages suivante
                next_link = soup.find("li", class_="next")

                if next_link:
                    url = urljoin(url, next_link.find("a")["href"])
                else:
                    url = None

            except requests.exceptions.RequestException as e:
                print(
                    f"Erreur lors de la récupération des livres dans la catégorie. Détails : {e}"
                )
                url = None

        print(f"Il y a {len(books_in_category)} livres dans la catégorie {category}.")
        save_data(category, books_in_category)

    # Multithreading pour accélerer le processus de scraping équivalent au nombre de coeur processeur
    with ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(fetch_books, category_urls)

    return all_books_info


# Fonction pour récupérer les informations d'un livre
def book_info(url):
    # Récupération de la réponse par requests GET
    response = requests.get(url)
    response.encoding = "utf-8"

    # BS va récupérer les informations de response et les stocks dans un object "soup"
    soup = BeautifulSoup(response.text, "html.parser")

    # Gestion des informations vides / erreurs
    def get_text(soup, selector, attribute=None, next_sibling=False):
        try:
            element = soup.select_one(selector)
            if element is None:
                return "Information non présente"
            if next_sibling:
                sibling = element.find_next_sibling()
                if sibling is None:
                    return "Information non présente"
                return sibling.text.strip()
            elif attribute:
                return element.get(attribute)
            else:
                return element.text.strip()
        except AttributeError:
            return "Information non présente"

    # Extraction du nombre de livres disponibles sinon dire Rupture
    availability_text = get_text(soup, 'th:-soup-contains("Availability") + td')
    match = re.search(r"\d+", availability_text)
    if match:
        availability = match.group()
    else:
        availability = "Rupture"

    # Définition des variables pour chaque informations nécessaires
    book_info = {
        "URL de la page du produit": url,
        "Code universel du produit": get_text(soup, 'th:-soup-contains("UPC") + td'),
        "Titre": get_text(soup, "div.product_main h1"),
        "Prix TTC": get_text(soup, 'th:-soup-contains("Price (incl. tax)") + td'),
        "Prix HT": get_text(soup, 'th:-soup-contains("Price (excl. tax)") + td'),
        "Nombre disponible": availability,
        "Description du produit": get_text(soup, "#product_description + p"),
        "Catégorie": get_text(soup, "ul.breadcrumb li:nth-child(3)"),
        "Note d'évaluation": get_text(soup, "div.product_main p.star-rating", "class")[
            1
        ],
        "URL de l'image": urljoin(
            "https://books.toscrape.com/", soup.select_one("div.item.active img")["src"]
        ),
    }

    return book_info


# Fonction pour sauvegarder toutes les informations de tous les livres dans un fichier .CSV
def save_data(category, all_books_info):
    # Vérification que la liste n'est pas vide
    if not all_books_info:
        print("Aucune information à enregistrer.")
        return

    # Création du nom du fichier
    filename = f"{category}-all_books_info.csv"

    try:
        # Vérification et création du dossier 'downloads' s'il n'existe pas
        downloads_folder = "downloads"
        if not os.path.exists(downloads_folder):
            os.makedirs(downloads_folder)

        # Vérification et création du sous-dossier pour la catégorie
        category_folder = os.path.join(downloads_folder, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        # Écriture des informations de tous les livres dans le fichier CSV
        with open(
            file=os.path.join(downloads_folder, category, filename),
            mode="w",
            newline="",
            encoding="utf-8",
        ) as csvfile:
            fieldnames = all_books_info[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for book_info in all_books_info:
                writer.writerow(book_info)

        print(f"Données enregistrées avec succès dans {filename}")

    except (OSError, IOError) as e:
        print(f"Erreur lors de l'enregistrement des données. Détails : {e}")

    save_picture(category, all_books_info)


def save_picture(category, all_books_info):
    # Chemin du dossier d'enregistrement des images
    image_folder = os.path.join("downloads", category, "images")

    # Création du dossier pour stocker les images s'il n'existe pas
    os.makedirs(image_folder, exist_ok=True)

    # Téléchargement et sauvegarde de l'image de chaque livre
    for book_info in all_books_info:
        image_url = book_info.get("URL de l'image")
        image_title = book_info.get("Titre")

        if image_url:

            # Ajout d'un nom de fichier sécurisé (élimination de caractères non autorisés)
            image_title = "".join(
                c if c.isalnum() or c in [" ", "-", "_"] else "" for c in image_title
            )
            image_title += ".jpg"

            image_filename = os.path.join(image_folder, image_title)
            try:
                response = requests.get(image_url)
                response.raise_for_status()

                with open(image_filename, mode="wb") as f:
                    f.write(response.content)
            except requests.exceptions.RequestException as e:
                print(
                    f"Erreur lors du téléchargement de l'image pour {book_info.get('Titre')}. Détails : {e}"
                )


def main():

    data = get_all_categories()
    print(f"Il y a {len(data)} catégories")

    data = get_all_books_in_category(data)
    print(f"il y a {len(data)} livres analysés")


if __name__ == "__main__":
    main()
