# Analyse-des-publications-UPEC

![Logo Hal](ressources/images/hal_logo.png)

Ce projet vise à analyser les publications de l'UPEC enregistrées sur [la plateforme HAL](https://hal.science/)
en utilisant PySpark pour le traitement des données. Il inclut également des scripts de scraping pour collecter les données, ainsi que des graphiques et rapports générés à partir de l'analyse de ses données.

## Structure du Projet

Voici une description du dossier ressources, où sont indiqués les données produites et manipulés ainsi que des exemples et traces d'utilisation.

```
ressources/
├── data/ # Dossiers contenant les données brutes et traitées
│ ├── raw_data.csv # Données brutes extraites de la base de données
│ └── analysed_data.csv # Données analysées (vitesse de traitement PySpark)
│
├── images/ # Dossiers pour les images (logs, captures d'écran, etc.)
│
├── scripts/ # Scripts utilisés pour le scraping et l'analyse
│ ├── scraping.py # Script pour extraire les données de la base de données
│ └── analyse_pyspark.py # Script pour analyser les données avec PySpark
│
├── graphs/ # Graphiques générés à partir des données analysées
│ └── speed_analysis.png # Graphique montrant la vitesse de traitement PySpark
│
├── ia/ # Scripts utilisés pour le scraping et l'analyse
  └── modèle ia-20250212T150700Z-001.zip # Script pour extraire les données de la base de données
│
└── Rapport_Megadonnées-1.pdf # Rapport détaillant les résultats de l'analyse
```

## Données

Les données brutes sont trop volumineuses et ne peuvent pas être stockées dans ce git. Les scripts permettant de la réaliser sont disponibles dans le dossier ressource/scripts.

Pour ce projet, 2 methodes différents ont été réalisés pour crée la base de données. Le premier est un script faisant l'appel à l'API HAL.

Les données analysées, incluant les métriques de vitesse de traitement PySpark, sont disponibles dans `ressources/data/analysed_data.csv`.


## Scripts

- **`scraping.py`** : Ce script permet d'extraire les données de la base de données et de les sauvegarder dans `ressources/data/raw_data.csv`.
- **`analyse_pyspark.py`** : Ce script utilise PySpark pour analyser les données et générer les graphiques de performance. Les résultats sont sauvegardés dans `ressources/data/analysed_data.csv`.

## Intelligence Artificielle : Prédiction des Domaines de Recherche

Cette section décrit les fichiers et l'arborescence liés au modèle d'IA pour la prédiction des domaines de recherche spécifiques à HAL vers le Panel ERC.

### Arborescence du fichier ZIP

```
ia/
├── domaine.csv                  # Oracle de transcription entre les domaines de recherche HAL et le Panel ERC
├── date_propre.csv                 # Base de données sous format CSV
├── date_propre       # Base de données sous format Google Sheets
├── erc_panel_predictor.joblib   # Modèle d'IA entraîné pour la prédiction des domaines ERC
├── mlb.joblib               # Transforme les étiquettes multilabel en représentation binaire
├── tfidf.joblib             # Module de vectorisation TF-IDF pour le modèle
├── ERC.ipynb                # Notebook Jupyter pour l'entraînement du modèle
├── publications_with_predicted_erc.csv          # Prédictions des domaines ERC au format CSV
└── publications_with_predicted_erc # Prédictions des domaines ERC au format Google Sheets
``` 

Description des Fichiers

`domaine.csv` :
    Ce fichier sert d'oracle de transcription entre les domaines de recherche spécifiques à HAL et les domaines du Panel ERC. Il est utilisé pour mapper les domaines de HAL vers les catégories ERC.


`date_propre.csv` : Fichier CSV contenant les données nettoyées.

`data_google_sheets` : fichier vers la même base de données au format Google Sheets.

`erc_panel_predictor.joblib` :
    Ce fichier contient le modèle d'IA entraîné pour prédire les domaines du Panel ERC à partir des domaines de recherche HAL.

`mlb.joblib` : Transforme les étiquettes multilabel en une représentation binaire.

`tfidf.joblib` : Module de vectorisation TF-IDF utilisé pour prétraiter les données textuelles.

`Model Domains/ERC.ipynb` :
    Ce notebook Jupyter contient le code utilisé pour l'entraînement du modèle. Il inclut les étapes de prétraitement des données, d'entraînement du modèle et d'évaluation des performances.

`publications_with_predicted_erc.csv` : Fichier CSV contenant les prédictions des domaines ERC.

`publications_with_predicted_erc` : fichier avec les mêmes prédictions dans Google Sheets.

## Graphiques

Les graphiques générés à partir des données analysées sont stockés dans le dossier `ressources/graphs/`. Par exemple :
- `speed_analysis.png` : Graphique montrant la vitesse de traitement PySpark en fonction des différentes configurations.

## Rapport

Le rapport détaillant les résultats de l'analyse est disponible dans le fichier `ressources/Rapport_Megadonnées-1.pdf`. Il inclut :
- Une description des données.
- Les méthodes d'analyse utilisées.
- Les conclusions et observations.