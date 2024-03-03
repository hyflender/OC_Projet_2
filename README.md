<div align="center" id="top"> 
<img alt="Logo" src="https://scrape-it.cloud/assets/cache_image/assets/blog_img/web-scraping-with-python_1280x533_301.webp">
</div>

<h1 align="center">Projet n°2 de OpenClassRoom Anthony PIAUGEARD</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/hyflender/OC_Projet_2?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/hyflender/OC_Projet_2?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/hyflender/OC_Projet_2?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/hyflender/OC_Projet_2?color=56BEB8">

</p>

# Scraping de livres

Ce script Python utilise BeautifulSoup et requests pour extraire des informations sur les livres d'un site web de vente de livres. Les informations extraites incluent les catégories, les détails des livres (tels que le titre, le prix, la disponibilité, etc.), et les images associées.

## Prérequis

- Python 3.x
- Modules Python requis (installez-les via `pip install -r requirements.txt`) :
    - requests
    - bs4 (BeautifulSoup)
    - pandas
    - SQLAlchemy


## Installation

1. Clonez le dépôt :

- `git clone https://github.com/hyflender/OC_Projet_2.git`
- `cd OC_Projet_2`

2. Initialiser et activer votre environnement virtuel :

- Windows Powershell :

```powershell
py -m venv env
py ./env/Scripts/Activate
```

- Linux/macOS :
```bash
python3 -m venv env
source env/bin/activate
```

3. Installez les dépendances :

- `pip install -r requirements.txt`

4. Exécutez le script principal :

- `python main.py`

## Fonctionnalités

- **Extraction** : Récupération des URLs de toutes les catégories et des informations de tous les livres.
- **Transformation** : Nettoyage et structuration des données extraites.
- **Chargement** : Sauvegarde des informations dans des fichiers CSV et téléchargement des images des livres.

## Structure du projet

- `main.py` : Point d'entrée du script.
- `requirements.txt` : Dépendances du projet.
- `downloads/` : Dossier de sauvegarde des données CSV et des images.
- `etl/` : Modules d'extraction, transformation, et chargement.
- `utils/` : Fonctions utilitaires.

## Avertissement

Ce script est destiné à des fins éducatives et d'apprentissage. Respectez toujours les conditions d'utilisation du site web que vous scrapez.