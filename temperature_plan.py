import shapefile
import os
import csv

import fltk
from fltk import *
from convert import coords_to_pixels


def charger_temperatures(fichier_csv, date):
    """
    Charge les températures pour une date donnée depuis le fichier CSV
    """
    temperatures = {}

    # Ouvrir le fichier CSV
    with open(fichier_csv, 'r', encoding='utf-8-sig') as f:
        # Lire le CSV avec DictReader (utilise la première ligne comme noms de colonnes)
        lecteur = csv.DictReader(f, delimiter=';')

        # Parcourir chaque ligne du CSV
        for ligne in lecteur:
            date_csv = ligne['Date']
            code_dep = ligne['Code INSEE département']

            # Normaliser le code département: enlever les zéros devant
            # '01' -> '1', '02' -> '2', etc.
            if code_dep.isdigit():
                code_dep = str(int(code_dep))

            # Si c'est la bonne date, on récupère la température
            if date_csv == date:
                try:
                    temp = float(ligne['TMoy (°C)'])
                    temperatures[code_dep] = temp
                except (ValueError, KeyError):
                    # Si on n'arrive pas à lire la température, on continue
                    continue

    return temperatures


def couleur_selon_temperature(temp):
    """
    Retourne une couleur en fonction de la température
    """
    if temp is None:
        return "#cccccc"  # Gris si pas de données

    # Échelle de couleurs du froid au chaud
    if temp < 0:
        return "#0000ff"  # Bleu foncé
    elif temp < 5:
        return "#4169e1"  # Bleu
    elif temp < 10:
        return "#87ceeb"  # Bleu clair
    elif temp < 15:
        return "#90ee90"  # Vert clair
    elif temp < 20:
        return "#ffff00"  # Jaune
    elif temp < 25:
        return "#ffa500"  # Orange
    elif temp < 30:
        return "#ff6347"  # Rouge-orange
    else:
        return "#ff0000"  # Rouge


def normaliser_points(points):
    """
    Transforme une liste de points en format utilisable par fltk
    """
    if not points:
        return []

    # Si c'est déjà une liste de tuples, on convertit juste en float
    if isinstance(points[0], (list, tuple)):
        return [(float(x), float(y)) for x, y in points]

    # Sinon c'est une liste plate [x1, y1, x2, y2, ...], on la découpe
    liste_float = list(map(float, points))

    # S'assurer qu'on a un nombre pair de valeurs
    if len(liste_float) % 2 != 0:
        liste_float = liste_float[:-1]

    # Créer des tuples (x, y)
    return list(zip(liste_float[0::2], liste_float[1::2]))

# Chemins des fichiers
repertoire_actuel = os.getcwd()
fichier_shapefile = repertoire_actuel + "/departements-20180101-shp/departements-20180101.shp"
fichier_temperatures = "temperature-quotidienne-departementale.csv"

# Dimensions de la fenêtre
largeur_fenetre = 1200
hauteur_fenetre = 800
largeur_legende = 200
largeur_carte = largeur_fenetre - largeur_legende

print("Lecture du shapefile des départements...")
sf = shapefile.Reader(fichier_shapefile)
enregistrements = sf.records()
toutes_les_formes = sf.shapes()

# Dictionnaire pour stocker les formes par code département
code_vers_forme = {}
formes_france = []

# Parcourir tous les départements
for forme, enregistrement in zip(toutes_les_formes, enregistrements):
    code = enregistrement['code_insee']

    # Garder seulement la France métropolitaine
    if code.isdigit() and 1 <= int(code) <= 95:
        code_normalise = str(int(code))  # Enlever le zéro devant
        code_vers_forme[code_normalise] = forme
        formes_france.append(forme)
    elif code in ["2A", "2B"]:  # Corse
        code_vers_forme[code] = forme
        formes_france.append(forme)
    elif code in ["69D", "69M"]:  # Rhône divisé depuis 2015
        code_vers_forme[code] = forme
        formes_france.append(forme)

print(f"Nombre de départements chargés: {len(code_vers_forme)}")

# Calculer la bounding box (rectangle englobant) de la France
lon_min = min(f.bbox[0] for f in formes_france)
lat_min = min(f.bbox[1] for f in formes_france)
lon_max = max(f.bbox[2] for f in formes_france)
lat_max = max(f.bbox[3] for f in formes_france)
bbox_france = [lon_min, lat_min, lon_max, lat_max]

# Charger les températures pour une date donnée
date_affichee = input("Saisir le date en format 'aaaa-mm-jj' de 2018-01-01 a 2025-11-30: \n")


temperatures = charger_temperatures(fichier_temperatures, date_affichee)


cree_fenetre(largeur_fenetre, hauteur_fenetre, redimension=False)

# Titre
texte(
    largeur_carte // 2, 30,
    f"Températures moyennes - {date_affichee}",
    taille=24,
    couleur="black",
    ancrage="center",
    police="Helvetica Bold"
)


# Parcourir tous les départements
for code, forme in code_vers_forme.items():
    # Normaliser pour 69D et 69M -> 69
    code_temp = '69' if code in ['69D', '69M'] else code

    # Récupérer la température de ce département
    temp = temperatures.get(code_temp)

    # Choisir la couleur selon la température
    couleur = couleur_selon_temperature(temp)

    # Dessiner le département (peut avoir plusieurs parties = îles)
    if len(forme.parts) == 1:
        # Cas simple: un seul polygone
        points_pixels = coords_to_pixels(
            forme.points,
            bbox_france,
            largeur_carte,
            hauteur_fenetre,
            marge=50
        )
        points_normalises = normaliser_points(points_pixels)

        # Créer une liste plate pour la fonction polygone
        liste_plate = []
        for x, y in points_normalises:
            liste_plate.append(x)
            liste_plate.append(y)

        # Dessiner le polygone
        polygone(
            liste_plate,
            remplissage=couleur,
            couleur="#333333",  # Bordure gris foncé
            epaisseur=1
        )

    else:
        # Cas complexe: plusieurs parties (îles, enclaves)
        for i in range(len(forme.parts)):
            debut = forme.parts[i]
            fin = forme.parts[i + 1] if i + 1 < len(forme.parts) else len(forme.points)
            points_partie = forme.points[debut:fin]

            points_pixels = coords_to_pixels(
                points_partie,
                bbox_france,
                largeur_carte,
                hauteur_fenetre,
                marge=50
            )
            points_normalises = normaliser_points(points_pixels)

            liste_plate = []
            for x, y in points_normalises:
                liste_plate.append(x)
                liste_plate.append(y)

            polygone(
                liste_plate,
                remplissage=couleur,
                couleur="#333333",
                epaisseur=1
            )


# Position de la légende à droite
x_legende = largeur_carte + 40
y_debut = 100
espacement = 60

# Titre de la légende
texte(x_legende - 20, 60, "LÉGENDE", taille=18, police="Helvetica Bold")

# Éléments de la légende
elements = [
    {"texte": "< 0°C", "couleur": "#0000ff"},
    {"texte": "0-5°C", "couleur": "#4169e1"},
    {"texte": "5-10°C", "couleur": "#87ceeb"},
    {"texte": "10-15°C", "couleur": "#90ee90"},
    {"texte": "15-20°C", "couleur": "#ffff00"},
    {"texte": "20-25°C", "couleur": "#ffa500"},
    {"texte": "25-30°C", "couleur": "#ff6347"},
    {"texte": "> 30°C", "couleur": "#ff0000"},
]

# Dessiner chaque élément de la légende
for i, element in enumerate(elements):
    y = y_debut + i * espacement

    # Rectangle coloré
    rectangle(
        x_legende - 15, y - 10,
        x_legende + 15, y + 10,
        couleur=element["couleur"],
        remplissage=element["couleur"]
    )

    # Texte
    texte(
        x_legende + 25, y - 6,
        element["texte"],
        taille=14,
        ancrage="w"
    )

mise_a_jour()

attend_fermeture()