import shapefile
import os

import fltk
from fltk import *
from convert import coords_to_pixels
from description_lieu import HISTOIRES_DETAILLEES, affiche_histoire, HISTOIRE_TAG

# Ce dictionnaire stockera : {ID_OBJET_CERCLE_FLTK: "Nom_du_Lieu"}
objets_lieux = {}

# Paramètres
path = os.getcwd()
fichier_shp = path + "/departements-20180101-shp/departements-20180101.shp"

largeur_total, hauteur_total = 1200, 1000
largeur_legende = 200
largeur_carte = largeur_total - largeur_legende

# Lecture du shapefile
sf = shapefile.Reader(fichier_shp)
records = sf.records()
all_shapes = sf.shapes()


depart = {}
france_shapes = []
for shape, record in zip(all_shapes, records):
    code = record['code_insee']
    if code.isdigit() and 1 <= int(code) <= 95:
        depart[int(code)] = shape
        france_shapes.append(shape)
    elif code in ["2A", "2B"]:
        depart[code] = shape
        france_shapes.append(shape)

# Bounding box globale
lon_min = min(s.bbox[0] for s in france_shapes)
lat_min = min(s.bbox[1] for s in france_shapes)
lon_max = max(s.bbox[2] for s in france_shapes)
lat_max = max(s.bbox[3] for s in france_shapes)
bbox_fr = [lon_min, lat_min, lon_max, lat_max]

zoom_level = 1.0
centre_lon = (lon_min + lon_max) / 2
centre_lat = (lat_min + lat_max) / 2
bbox_actuel = bbox_fr.copy()
print(f"Bbox France: lon [{lon_min:.2f}, {lon_max:.2f}], lat [{lat_min:.2f}, {lat_max:.2f}]")


def normalize_pts(pts):
    """Normalise une liste de points pour coords_to_pixels"""
    if not pts:
        return []
    if isinstance(pts[0], (list, tuple)):
        return [(float(a), float(b)) for a, b in pts]
    it = list(map(float, pts))
    if len(it) % 2 != 0:
        it = it[:-1]
    return list(zip(it[0::2], it[1::2]))


# Convertir tous les shapes en pixels
shapes_pixels = []
for s in france_shapes:
    if len(s.parts) == 1:
        # Cas simple: un seul polygone
        pts_wgs84 = s.points  # Garder les coordonnées WGS84
        raw_pts = coords_to_pixels(pts_wgs84, bbox_fr, largeur_carte, hauteur_total, marge=20)
        pts = normalize_pts(raw_pts)
        shapes_pixels.append([pts])
    else:
        # Cas complexe: plusieurs parties (îles)
        parts_list = []
        for i in range(len(s.parts)):
            start = s.parts[i]
            end = s.parts[i + 1] if i + 1 < len(s.parts) else len(s.points)
            part_points = s.points[start:end]

            raw_pts = coords_to_pixels(part_points, bbox_fr, largeur_carte, hauteur_total, marge=20)
            pts = normalize_pts(raw_pts)
            parts_list.append(pts)
        shapes_pixels.append(parts_list)

# Calcul de l'enveloppe pour info (mais plus besoin de centrer manuellement)
all_x = []
all_y = []
for shape_parts in shapes_pixels:
    for part in shape_parts:
        for x, y in part:
            all_x.append(x)
            all_y.append(y)

if not all_x or not all_y:
    all_x = [0]
    all_y = [0]

min_x, max_x = min(all_x), max(all_x)
min_y, max_y = min(all_y), max(all_y)

print(f"Dimensions carte en pixels: largeur={max_x - min_x:.1f}, hauteur={max_y - min_y:.1f}")


def appliquer_zoom(facteur_zoom: float, centre_lon: float, centre_lat: float):
    """
    Recalcule la BBox et redessine la carte entière avec le nouveau niveau de zoom.

    Arguments:
        facteur_zoom (float): Le nouveau facteur d'échelle.
        centre_lon (float): Longitude du nouveau centre de la vue.
        centre_lat (float): Latitude du nouveau centre de la vue.
    """
    global zoom_level, bbox_actuel

    # Dimensions originales de la carte en WGS84
    lon_range_orig = lon_max - lon_min
    lat_range_orig = lat_max - lat_min

    # Nouvelles dimensions de la vue (rétrécissement/élargissement)
    lon_range_zoom = lon_range_orig / facteur_zoom
    lat_range_zoom = lat_range_orig / facteur_zoom

    # Calcul de la nouvelle BBox centrée
    new_lon_min = centre_lon - lon_range_zoom / 2
    new_lon_max = centre_lon + lon_range_zoom / 2
    new_lat_min = centre_lat - lat_range_zoom / 2
    new_lat_max = centre_lat + lat_range_zoom / 2

    bbox_actuel = [new_lon_min, new_lat_min, new_lon_max, new_lat_max]
    zoom_level = facteur_zoom

    # --- Phase de Redessin ---

    # 1. Effacer tout ce qui est lié à la carte et aux points
    efface("carte")
    efface("lieu")
    efface("legende_point")

    # 2. Re-conversion des shapes (départements) en pixels
    shapes_pixels_zoom = []
    for s in france_shapes:
        if len(s.parts) == 1:
            raw_pts = coords_to_pixels(s.points, bbox_actuel, largeur_carte, hauteur_total, marge=20)
            shapes_pixels_zoom.append([normalize_pts(raw_pts)])
        else:
            parts_list = []
            for i in range(len(s.parts)):
                start = s.parts[i]
                end = s.parts[i + 1] if i + 1 < len(s.parts) else len(s.points)
                part_points = s.points[start:end]

                raw_pts = coords_to_pixels(part_points, bbox_actuel, largeur_carte, hauteur_total, marge=20)
                parts_list.append(normalize_pts(raw_pts))
            shapes_pixels_zoom.append(parts_list)

    # Dessiner les départements avec les nouvelles coordonnées
    for shape_parts in shapes_pixels_zoom:
        for part in shape_parts:
            flat_pts = []
            for x, y in part:
                flat_pts.extend([x, y])
            polygone(flat_pts, remplissage="#dddddd", couleur="#888888", epaisseur=1, tag="carte")

    # Dessiner les lieux avec les nouvelles coordonnées
    for p in lieux:
        raw = coords_to_pixels([p["pos"]], bbox_actuel, largeur_carte, hauteur_total, marge=20)
        pts = normalize_pts(raw)

        if not pts:
            continue
        x, y = pts[0]

        point_id = cercle(
            x, y, 6,
            couleur=p["couleur"],
            remplissage=p["couleur"],
            tag=f"lieu point_{p['nom'].replace(' ', '_')}"
        )

        # Mise à jour (ou recréation) de l'association ID d'objet FLTK -> Nom du lieu
        # Note : ceci est crucial car l'ID FLTK change à chaque recréation !
        objets_lieux[point_id] = p["nom"]

        # Dessin du texte
        texte(x + 8, y - 4, p["nom"], taille=12, tag="legende_point")

    mise_a_jour()


# Prépare la fenêtre
cree_fenetre(largeur_total, hauteur_total, redimension=False)

# Dessine les départements
for shape_parts in shapes_pixels:
    for part in shape_parts:
        flat_pts = []
        for x, y in part:
            flat_pts.extend([x, y])
        polygone(flat_pts, remplissage="#dddddd", couleur="#888888", epaisseur=1, tag="carte")

# Lieux spécifiques
lieux = [
    {"nom": "Catacombes", "pos": (2.3327, 48.8339), "couleur": "black"},
    {"nom": "les thermes verts", "pos": (3.07, 45.77), "couleur": "black"},
    {"nom": "Hopital abandonne", "pos": (4.8357, 45.7640), "couleur": "green"},
    {"nom": "Cimetiere abandonne", "pos": (1.4442, 43.6045), "couleur": "purple"},
    {"nom": "Ecole abandonnee", "pos": (-0.5792, 44.8378), "couleur": "blue"},
    {"nom": "Hopital psychiatrique de Bargeme", "pos": (6.50, 43.75), "couleur": "darkgreen"},
    {"nom": "Fort de Cognelot", "pos": (5.41, 47.82), "couleur": "orange"},
    {"nom": "Goussainville Vieux-Pays", "pos": (2.47, 49.03), "couleur": "purple"},
    {"nom": "Mine Cap Garonne", "pos": (6.03, 43.10), "couleur": "gold"},
    {"nom": "Sucrerie de Francieres", "pos": (2.61, 49.43), "couleur": "darkblue"},
    {"nom": "Chateau Pont-Remy", "pos": (1.90, 50.05), "couleur": "darkred"},
    {"nom": "Fort de la Latte", "pos": (-2.30, 48.65), "couleur": "brown"},
    {"nom": "Base Lann-Bihoue", "pos": (-3.44, 47.76), "couleur": "darkgray"},
    {"nom": "Ferme fortifiee Montmartin", "pos": (-1.36, 49.22), "couleur": "purple"},
    {"nom": "Ancien Hopital Dreffeac", "pos": (-2.05, 47.50), "couleur": "darkred"},
    {"nom": "Chateau Mothe-Chandeniers", "pos": (0.03, 46.99), "couleur": "gold"},
    {"nom": "Fort Lupin", "pos": (-0.99, 45.87), "couleur": "darkblue"},
    {"nom": "Ancienne Gare Luxe", "pos": (0.13, 45.89), "couleur": "darkorange"},
]

# Dessiner les lieux
for p in lieux:
    raw = coords_to_pixels([p["pos"]], bbox_fr, largeur_carte, hauteur_total, marge=20)
    pts = normalize_pts(raw)
    if not pts:
        continue
    x, y = pts[0]

    # Dessin du cercle et récupération de l'ID
    point_id = cercle(
        x, y, 6,
        couleur=p["couleur"],
        remplissage=p["couleur"],
        tag=f"lieu point_{p['nom'].replace(' ', '_')}"
    )

    # Stockage de l'association ID d'objet FLTK -> Nom du lieu
    objets_lieux[point_id] = p["nom"]

    # Dessin du texte
    texte(x + 8, y - 4, p["nom"], taille=12, tag="legende_point")

# Légende
x_legende = largeur_carte + 40
y_depart = 80
espacement = 60

texte(x_legende - 20, 40, "LEGENDE", taille=16, police="Helvetica Bold")

elements_legende = [
    {"nom": "catacombe", "couleur": "black"},
    {"nom": "Stations ", "couleur": "darkred"},
    {"nom": "Bunker ", "couleur": "gray"},
    {"nom": "hopital", "couleur": "green"},
    {"nom": "cimetiere", "couleur": "purple"},
    {"nom": "ecole", "couleur": "blue"},
]

for i, elem in enumerate(elements_legende):
    y = y_depart + i * espacement
    cercle(x_legende, y, 10, couleur=elem["couleur"], remplissage=elem["couleur"])
    texte(x_legende + 40, y - 6, elem["nom"], taille=14)

mise_a_jour()

lieu_clique_status = False
lieu_actuel = None

abscisse_souris()
ordonnee_souris()

# Boucle principale
while True:
    ev = donne_ev()

    if ev is not None:
        type_event = type_ev(ev)

        if type_event == "Quitte":
            break

        elif type_event == "ClicGauche":
            x = abscisse(ev)
            y = ordonnee(ev)

            # On vérifie si l'utilisateur a cliqué sur X
            if lieu_clique_status and (largeur_total - 50 < x < largeur_total and 0 < y < 50):
                efface(HISTOIRE_TAG)
                mise_a_jour()
                lieu_clique_status = False
                lieu_actuel = None
                continue

            # Clic par défaut sur le plan
            survoles = liste_objets_survoles()
            lieu_clique_nom = None

            for obj_id in survoles:
                if obj_id in objets_lieux:
                    lieu_clique_nom = objets_lieux[obj_id]
                    break

            if lieu_clique_nom:
                lieu_actuel = lieu_clique_nom
                lieu_clique_status = True
                affiche_histoire(lieu_clique_nom, largeur_total)

        elif type_event == "Touche":
            print(touche(ev))

            if touche(ev) == 'plus':
                # Zoom In
                zoom_factor_step = 1.2
                zoom_level *= zoom_factor_step
                appliquer_zoom(zoom_level, (bbox_actuel[0] + bbox_actuel[2]) / 2, (bbox_actuel[1] + bbox_actuel[3]) / 2)
            elif touche(ev) == 'minus':
                # Zoom Out
                zoom_factor_step = 1.2
                zoom_level = max(1.0, zoom_level / zoom_factor_step)
                appliquer_zoom(zoom_level, (bbox_actuel[0] + bbox_actuel[2]) / 2, (bbox_actuel[1] + bbox_actuel[3]) / 2)

    mise_a_jour()

ferme_fenetre()