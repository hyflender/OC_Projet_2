![](https://scrape-it.cloud/assets/cache_image/assets/blog_img/web-scraping-with-python_1280x533_301.webp)

Projet n°2 de OpenClassRoom Anthony PIAUGEARD

# Scraping de livres

Ce script Python utilise BeautifulSoup et requests pour extraire des informations sur les livres d'un site web de vente de livres. Les informations extraites incluent les catégories, les détails des livres (tels que le titre, le prix, la disponibilité, etc.), et les images associées.

## Prérequis

- Python 3.x
- Modules Python requis (installez-les via `pip install -r requirements.txt`) :

requests
bs4 (BeautifulSoup)

## Comment utiliser le script

1. Clonez le dépôt :

git clone https://github.com/hyflender/OC_Projet_2.git
cd OC_Projet_2

2. Installez les dépendances :

pip install -r requirements.txt

3. Exécutez le script principal :

python main.py

## Fonctionnalités

- get_all_categories(url): Fonction pour récupérer les URLs de toutes les catégories du site.
- get_all_books_in_category(category_urls): Fonction pour récupérer les informations de tous les livres dans chaque catégorie.
- book_info(url): Fonction pour récupérer les détails d'un livre spécifique.
- save_data(category, all_books_info): Fonction pour sauvegarder toutes les informations de tous les livres dans un fichier CSV.
- save_picture(category, all_books_info): Fonction pour télécharger et sauvegarder les images de chaque livre.

## Structure du projet

- main.py: Script principal à exécuter.
- requirements.txt: Liste des dépendances du projet.
- downloads/: Dossier où les données CSV et les images sont sauvegardées.

## Avertissement

Ce script est destiné à des fins éducatives et d'apprentissage. Respectez toujours les conditions d'utilisation du site web que vous scrapez.