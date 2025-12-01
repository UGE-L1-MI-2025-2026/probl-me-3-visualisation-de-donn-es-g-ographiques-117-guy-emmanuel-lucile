# carte_france_lieux.py
import shapefile
import os
from fltk import *
from convert import coords_to_pixels

# ---------- paramètres ----------
path = os.getcwd()
fichier_shp = path + "/departements-20180101-shp/departements-20180101.shp"

largeur_total, hauteur_total = 1200, 1000
largeur_legende = 200
largeur_carte = largeur_total - largeur_legende
scale_boost = 0.9  # zoom plus fort

# ---------- lecture du shapefile ----------
sf = shapefile.Reader(fichier_shp)
records = sf.records()
all_shapes = sf.shapes()

# Filtrer uniquement la France métropolitaine (01-95 + Corse 2A/2B)
france_shapes = []
for shape, record in zip(all_shapes, records):
    code = record['code_insee']
    if code.isdigit() and 1 <= int(code) <= 95:
        france_shapes.append(shape)
    elif code in ["2A", "2B"]:
        france_shapes.append(shape)

# ---------- bbox global ----------
lon_min = min(s.bbox[0] for s in france_shapes)
lat_min = min(s.bbox[1] for s in france_shapes)
lon_max = max(s.bbox[2] for s in france_shapes)
lat_max = max(s.bbox[3] for s in france_shapes)
bbox_fr = [lon_min, lat_min, lon_max, lat_max]

# ---------- helper ----------
def normalize_pts(pts):
    if not pts:
        return []
    if isinstance(pts[0], (list, tuple)):
        return [(float(a), float(b)) for a, b in pts]
    it = list(map(float, pts))
    if len(it) % 2 != 0:
        it = it[:-1]
    return list(zip(it[0::2], it[1::2]))

# ---------- Convertir tous les shapes en pixels ----------
shapes_pixels = []
for s in france_shapes:
    raw_pts = coords_to_pixels(s.points, bbox_fr, largeur_carte, hauteur_total)
    pts = normalize_pts(raw_pts)
    pts = [(x * scale_boost, y * scale_boost) for x, y in pts]
    shapes_pixels.append(pts)

# ---------- Calcul de l'enveloppe pour centrer ----------
all_x = [x for shape in shapes_pixels for x, _ in shape] if shapes_pixels else [0]
all_y = [y for shape in shapes_pixels for _, y in shape] if shapes_pixels else [0]
min_x, max_x = min(all_x), max(all_x)
min_y, max_y = min(all_y), max(all_y)

offset_x = ((largeur_carte) - (max_x - min_x)) / 2 - min_x
offset_y = (hauteur_total - (max_y - min_y)) / 2 - min_y

# ---------- Prépare la fenêtre ----------
cree_fenetre(largeur_total, hauteur_total, redimension=False)

# ---------- Dessine les départements ----------
for pts in shapes_pixels:
    pts_centered = [(x + offset_x, y + offset_y) for x, y in pts]
    polygone(pts_centered)

# ---------- Lieux spécifiques ----------
lieux = [
    {"nom": "Catacombes", "pos": (2.3327, 48.8339), "couleur": "black"},  # Paris
    {"nom": "Bunker Gare de l'Est", "pos": (2.3690, 48.8760), "couleur": "gray"},
    {"nom": "les thermes verts", "pos": (3.07, 45.77), "couleur": "black"},  # Clermont-Ferrand
    {"nom": "Station fantôme Croix-Rouge", "pos": (2.3226, 48.8333), "couleur": "darkred"},  # Paris
    {"nom": "Hôpital abandonné", "pos": (4.8357, 45.7640), "couleur": "green"},  # Lyon
    {"nom": "Cimetière abandonné", "pos": (1.4442, 43.6045), "couleur": "purple"},  # Toulouse
    {"nom": "École abandonnée", "pos": (-0.5792, 44.8378), "couleur": "blue"},  # Bordeaux
    {"nom": "sanatorium", "pos": (2.4901, 49.3172), "couleur": "darkred"},  # Paris


]

for p in lieux:
    raw = coords_to_pixels([p["pos"]], bbox_fr, largeur_carte, hauteur_total)
    pts = normalize_pts(raw)
    if not pts:
        continue
    x, y = pts[0]
    x = x * scale_boost + offset_x
    y = y * scale_boost + offset_y
    cercle(x, y, 6, couleur=p["couleur"], remplissage=p["couleur"])
    texte(x + 8, y - 4, p["nom"], taille=12)

# ---------- Légende ----------
x_legende = largeur_carte + 40
y_depart = 80
espacement = 60

texte(x_legende - 20, 40, "LÉGENDE", taille=16)

elements_legende = [
    {"nom": "catacombe", "couleur": "black"},
    {"nom": "Stations ", "couleur": "darkred"},
    {"nom": "Bunker ", "couleur": "gray"},
    {"nom": "hopital", "couleur": "green"},
    {"nom": "cimetière", "couleur": "purple"},
    {"nom": "ecole", "couleur": "blue"},
]

for i, elem in enumerate(elements_legende):
    y = y_depart + i * espacement
    cercle(x_legende, y, 10, couleur=elem["couleur"], remplissage=elem["couleur"])
    texte(x_legende + 40, y - 6, elem["nom"], taille=14)

# ---------- final ----------
mise_a_jour()
attend_ev()
