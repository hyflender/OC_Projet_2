# Fichier extract.py pour extraire les informations demandées dans le cadre d'une Pipeline ETL

from log_config import configure_logger
from utils.requests_utils import get_request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

log = configure_logger("Scraping")  # Chargement du logger


def get_all_categories(url="https://books.toscrape.com"):
    try:
        # Appel de la fonction get_request() du fichier requests_utils
        response = get_request(url)

        # Utilisation de html.parser pour le parsing HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Récupération des liens de toutes les catégories dans la navigation avec la classe "nav-list" par méthode css-selector
        category_links = soup.select("ul.nav.nav-list ul li a")

        # Mise en forme des URLs par urljoin
        category_urls = [urljoin(url, link["href"]) for link in category_links]

        return category_urls
    except Exception as e:
        log.critical(f"Une erreur s'est produite lors de l'extraction des catégories : {e}")


def get_all_books_in_categories(category_urls):
    all_books_urls = []  # Table pour stocker les données

    def fetch_books(url):
        log.info(
            f"Analyse et récupérations des URLs des livres de la catégorie - URL : {url}"
        )
        while url:  # boucle pour les pages suivantes
            try:
                response = get_request(url)
                soup = BeautifulSoup(response.text, "html.parser")

                book_links = soup.select(
                    "ol.row h3 a[href]"
                )  # Récupération de tous les liens des livres présents dans la catégorie

                for link in book_links:
                    book_url = urljoin(url, link["href"])
                    all_books_urls.append(book_url)

                # Recherche de pages suivante
                next_link = soup.find("li", class_="next")

                if next_link:
                    url = urljoin(url, next_link.find("a")["href"])
                else:
                    url = None

            except Exception as e:
                log.critical(
                    f"Erreur lors de la récupération des livres dans la catégorie. Détails : {e}"
                )
                url = None

    # Multithreading pour accélerer le processus de scraping équivalent au nombre de coeur processeur
    with ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(fetch_books, category_urls)

    return all_books_urls


def get_book_info(url):
    all_books_infos = []  # Table pour stocker les données

    def fetch_books(url):
        log.info(f" Récupération des informations du livre - url : {url}")
        response = get_request(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Definition of variables for each necessary information
        book_info = {
            "Product page URL": url,
            "Universal Product Code": soup.select_one(
                'th:-soup-contains("UPC") + td'
            ).text.strip(),
            "Title": soup.select_one("div.product_main h1").text.strip(),
            "Price incl. tax": soup.select_one(
                'th:-soup-contains("Price (incl. tax)") + td'
            ).text.strip(),
            "Price excl. tax": soup.select_one(
                'th:-soup-contains("Price (excl. tax)") + td'
            ).text.strip(),
            "Availability": soup.select_one(
                'th:-soup-contains("Availability") + td'
            ).text.strip(),
            "Product Description": soup.select_one(
                "#product_description + p"
            ).text.strip(),
            "Category": soup.select_one("ul.breadcrumb li:nth-child(3)").text.strip(),
            "Rating": soup.select_one("div.product_main p.star-rating")["class"][1],
            "Image URL": urljoin(
                "https://books.toscrape.com/",
                soup.select_one("div.item.active img")["src"],
            ),
        }
        all_books_infos.append(book_info)

    # Multithreading pour accélerer le processus de scraping équivalent au nombre de coeur processeur
    with ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(fetch_books, url)
    return all_books_infos
