# carte_france_legende_fixed.py
import shapefile
import os
from fltk import *
from convert import coords_to_pixels

# ---------- paramètres ----------
path = os.getcwd()
fichier_shp = path + "/departements-20180101-shp/departements-20180101.shp"

# zone fenêtre
largeur_total, hauteur_total = 1200, 1000
largeur_legende = 200              # réserve à droite pour la légende
largeur_carte = largeur_total - largeur_legende

# zoom (change si nécessaire)
scale_boost = 2.0

# ---------- lecture du shapefile ----------
sf = shapefile.Reader(fichier_shp)
france_shapes = sf.shapes()

# ---------- bbox global (lon/lat) ----------
lon_min = min(s.bbox[0] for s in france_shapes)
lat_min = min(s.bbox[1] for s in france_shapes)
lon_max = max(s.bbox[2] for s in france_shapes)
lat_max = max(s.bbox[3] for s in france_shapes)
bbox_fr = [lon_min, lat_min, lon_max, lat_max]

# ---------- helper : normaliser le format de pts ----------
def normalize_pts(pts):
    """
    pts peut être :
     - une liste de couples [(x,y), (x,y), ...]
     - une liste plate [x0, y0, x1, y1, ...]
    Retourne une liste de couples [(x,y), ...]
    """
    if not pts:
        return []
    # cas liste de couples
    if isinstance(pts[0], (list, tuple)):
        return [(float(a), float(b)) for a, b in pts]
    # cas liste plate
    it = list(map(float, pts))
    if len(it) % 2 != 0:
        # si bizarre, tronque le dernier
        it = it[:-1]
    return list(zip(it[0::2], it[1::2]))

# ---------- Convertir tous les shapes en pixels (sans offset centering) ----------
shapes_pixels = []  # liste de listes de (x,y)
for s in france_shapes:
    raw_pts = coords_to_pixels(s.points, bbox_fr, largeur_carte, hauteur_total)
    pts = normalize_pts(raw_pts)
    # applique scale_boost (zoom)
    pts = [(x * scale_boost, y * scale_boost) for x, y in pts]
    shapes_pixels.append(pts)

# ---------- Calculer l'enveloppe (min/max) des shapes transformés ----------
all_x = [x for shape in shapes_pixels for x, _ in shape] if shapes_pixels else [0]
all_y = [y for shape in shapes_pixels for _, y in shape] if shapes_pixels else [0]
min_x, max_x = min(all_x), max(all_x)
min_y, max_y = min(all_y), max(all_y)

# calcule offsets pour centrer la carte dans la zone gauche (0..largeur_carte)
offset_x = ((largeur_carte) - (max_x - min_x)) / 2 - min_x
offset_y = (hauteur_total - (max_y - min_y)) / 2 - min_y

# ---------- Prépare la fenêtre FLTK ----------
cree_fenetre(largeur_total, hauteur_total, redimension=False)

# ---------- Dessine les polygones (départements) ----------
for pts in shapes_pixels:
    pts_centered = [(x + offset_x, y + offset_y) for x, y in pts]
    polygone(pts_centered)  # couleur par défaut ; on peut ajouter remplissage/couleur

# ---------- Points tests (lon, lat) → transformés en pixels et dessinés ----------
# points de test en lon/lat (WGS84)
points_test = [
    {"type": "hopital", "pos": (2.3522, 48.8566), "nom": "Hôpital Test"},   # Paris
    {"type": "ecole",   "pos": (4.8357, 45.7640), "nom": "École Test"},     # Lyon
    {"type": "parc",    "pos": (5.3698, 43.2965), "nom": "Parc Test"},      # Marseille
    {"type": "maison",  "pos": (3.8772, 43.6119), "nom": "Maison Test"}     # Montpellier
]

couleurs = {
    "hopital": "green",
    "ecole": "blue",
    "parc": "red",
    "maison": "orange"
}

# coords_to_pixels attend normalement une liste de points, on l'appelle donc avec [(lon,lat)]
for p in points_test:
    raw = coords_to_pixels([p["pos"]], bbox_fr, largeur_carte, hauteur_total)
    pts = normalize_pts(raw)
    if not pts:
        continue
    x, y = pts[0]
    # applique zoom et offset identiques à la carte
    x = x * scale_boost + offset_x
    y = y * scale_boost + offset_y
    cercle(x, y, 10, couleur=couleurs[p["type"]], remplissage=couleurs[p["type"]])
    texte(x + 12, y - 6, p["nom"], taille=12)

# ---------- Légende à droite ----------
x_legende = largeur_carte + 40
y_depart = 80
espacement = 60

texte(x_legende - 20, 40, "LÉGENDE", taille=16)

elements_legende = [
    {"nom": "Hôpitaux", "couleur": "green"},
    {"nom": "Écoles", "couleur": "blue"},
    {"nom": "Parcs", "couleur": "red"},
    {"nom": "Maisons", "couleur": "orange"}
]

for i, elem in enumerate(elements_legende):
    y = y_depart + i * espacement
    cercle(x_legende, y, 14, couleur=elem["couleur"], remplissage=elem["couleur"])
    texte(x_legende + 40, y - 6, elem["nom"], taille=14)

# ---------- final ----------
mise_a_jour()
attend_ev()
