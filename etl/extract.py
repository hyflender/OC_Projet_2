# Fichier extract.py pour extraire les informations demandées dans le cadre d'une Pipeline ETL

from utils.log_config import configure_logger
from utils.requests_utils import get_request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor


class Extract:
    """
    Classe Extractor en POO

    Modules :

    Constructeur : __init__(self, url="https://books.toscrape.com") : Constructeur de la class
    get_all_categories(self) : Extract toutes les catégories du site "https://books.toscrape.com"
    get_all_books_in_categories(self, category_urls) : Extracte tout les livres présent dans la "category_url"
    get_book_info(self, url) : Extract les informations du livre "url"

    """

    def __init__(self, site_url="https://books.toscrape.com") -> None:
        self.site_url = site_url
        self.log = configure_logger("extract")  # Configuration du logger

    def get_all_category(self):
        category_urls = []
        try:
            # Appel de la fonction get_request() du fichier requests_utils
            response = get_request(self.site_url)
            if response:
                # Utilisation de html.parser pour le parsing HTML
                soup = BeautifulSoup(response.text, "html.parser")

                # Récupération des liens de toutes les catégories dans la navigation avec la classe "nav-list" par méthode css-selector
                category_links = soup.select("ul.nav.nav-list ul li a")

                # Mise en forme des URLs par urljoin
                category_urls = [
                    urljoin(self.site_url, link["href"]) for link in category_links
                ]
                self.log.info(f"Il y a {len(category_urls)} catégories à scrapper")

        except Exception as e:
            self.log.critical(
                f"Une erreur s'est produite lors de l'extraction des catégories : {e}"
            )
        return category_urls

    def get_all_books_in_category(self, category_url):
        self.category_url = category_url

        all_books_urls = (
            []
        )  # Table pour stocker les liens de tous les livres dans la catégorie

        self.log.info(
            f"Analyse et récupérations des URLs des livres de la catégorie - URL : {self.category_url}"
        )
        while self.category_url:  # boucle pour les pages suivantes
            try:
                response = get_request(self.category_url)
                soup = BeautifulSoup(response.text, "html.parser")

                book_links = soup.select(
                    "ol.row h3 a[href]"
                )  # Récupération de tous les liens des livres présents dans la catégorie

                for link in book_links:
                    book_url = urljoin(self.category_url, link["href"])
                    all_books_urls.append(book_url)

                # Recherche de pages suivante
                next_link = soup.find("li", class_="next")

                if next_link:
                    self.category_url = urljoin(
                        self.category_url, next_link.find("a")["href"]
                    )
                else:
                    self.category_url = None

            except Exception as e:
                self.log.critical(
                    f"Erreur lors de la récupération des livres dans la catégorie. Détails : {e}"
                )
                break

        return all_books_urls

    def get_book_info(self, book_url):
        self.book_url = book_url

        try:
            self.log.info(
                f" Récupération des informations du livre - url : {self.book_url}"
            )
            response = get_request(self.book_url)
            if response:
                soup = BeautifulSoup(response.text, "html.parser")

                # Définition des variables pour chaque information nécessaire
                book_infos = {
                    "Product page URL": self.book_url,
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
                    "Product Description": (
                        soup.select_one("#product_description + p").text.strip()
                        if soup.select_one("#product_description + p")
                        else None
                    ),
                    "Category": soup.select_one(
                        "ul.breadcrumb li:nth-child(3)"
                    ).text.strip(),
                    "Rating": soup.select_one("div.product_main p.star-rating")[
                        "class"
                    ][1],
                    "Image URL": urljoin(
                        "https://books.toscrape.com/",
                        soup.select_one("div.item.active img")["src"],
                    ),
                }
        except Exception as e:
            self.log.error(
                f"Erreur lors de la récupération des informations du livre {self.book_url}. Détails : {e}"
            )

        return book_infos
