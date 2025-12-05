import shapefile
import os
from fltk import *
from convert import coords_to_pixels
from description_lieu import HISTOIRES_DETAILLEES, affiche_histoire




# Ce dictionnaire stockera : {ID_OBJET_CERCLE_FLTK: "Nom_du_Lieu"}
objets_lieux = {}

# parametres
path = os.getcwd()
fichier_shp = path + "/departements-20180101-shp/departements-20180101.shp"

largeur_total, hauteur_total = 1200, 1000
largeur_legende = 200
largeur_carte = largeur_total - largeur_legende
scale_boost = 0.9

# lecture du shapefile
sf = shapefile.Reader(fichier_shp)
records = sf.records()
all_shapes = sf.shapes()

france_shapes = []
for shape, record in zip(all_shapes, records):
    code = record['code_insee']
    if code.isdigit() and 1 <= int(code) <= 95:
        france_shapes.append(shape)
    elif code in ["2A", "2B"]:
        france_shapes.append(shape)

# bbox global
lon_min = min(s.bbox[0] for s in france_shapes)
lat_min = min(s.bbox[1] for s in france_shapes)
lon_max = max(s.bbox[2] for s in france_shapes)
lat_max = max(s.bbox[3] for s in france_shapes)
bbox_fr = [lon_min, lat_min, lon_max, lat_max]


def normalize_pts(pts):
    if not pts:
        return []
    if isinstance(pts[0], (list, tuple)):
        return [(float(a), float(b)) for a, b in pts]
    it = list(map(float, pts))
    if len(it) % 2 != 0:
        it = it[:-1]
    return list(zip(it[0::2], it[1::2]))


# Convertir tous les shapes en pixels
# Correction de la gestion des polygones avec plusieurs parties (iles)
# Certains departements ont plusieurs parties (iles), il faut les separer correctement
shapes_pixels = []
for s in france_shapes:
    if len(s.parts) == 1:
        # Cas simple: un seul polygone
        raw_pts = coords_to_pixels(s.points, bbox_fr, largeur_carte, hauteur_total)
        pts = normalize_pts(raw_pts)
        pts = [(x * scale_boost, y * scale_boost) for x, y in pts]
        shapes_pixels.append([pts])
    else:
        # Cas complexe: plusieurs parties (iles)
        # s.parts contient les indices de debut de chaque partie
        parts_list = []
        for i in range(len(s.parts)):
            start = s.parts[i]
            end = s.parts[i + 1] if i + 1 < len(s.parts) else len(s.points)
            part_points = s.points[start:end]

            raw_pts = coords_to_pixels(part_points, bbox_fr, largeur_carte, hauteur_total)
            pts = normalize_pts(raw_pts)
            pts = [(x * scale_boost, y * scale_boost) for x, y in pts]
            parts_list.append(pts)
        shapes_pixels.append(parts_list)

# Calcul de l'enveloppe pour centrer
# Adaptation pour gerer les listes de parties
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

offset_x = ((largeur_carte) - (max_x - min_x)) / 2 - min_x
offset_y = (hauteur_total - (max_y - min_y)) / 2 - min_y

# Prepare la fenetre
cree_fenetre(largeur_total, hauteur_total, redimension=False)

# Dessine les departements
# Dessin de chaque partie separement
for shape_parts in shapes_pixels:
    for part in shape_parts:
        pts_centered = [(x + offset_x, y + offset_y) for x, y in part]
        # Convertir en liste plate pour polygone()
        flat_pts = []
        for x, y in pts_centered:
            flat_pts.extend([x, y])
        polygone(flat_pts, remplissage="#dddddd", couleur="#888888", epaisseur=1, tag="carte")

# Lieux specifiques
lieux = [
    {"nom": "Catacombes", "pos": (2.3327, 48.8339), "couleur": "black"},
    {"nom": "Bunker Gare de l'Est", "pos": (2.3690, 48.8760), "couleur": "gray"},
    {"nom": "les thermes verts", "pos": (3.07, 45.77), "couleur": "black"},
    {"nom": "Station fantome Croix-Rouge", "pos": (2.3226, 48.8333), "couleur": "darkred"},
    {"nom": "Hopital abandonne", "pos": (4.8357, 45.7640), "couleur": "green"},
    {"nom": "Cimetiere abandonne", "pos": (1.4442, 43.6045), "couleur": "purple"},
    {"nom": "Ecole abandonnee", "pos": (-0.5792, 44.8378), "couleur": "blue"},
    {"nom": "sanatorium", "pos": (2.4901, 49.3172), "couleur": "darkred"},
]

for p in lieux:
    raw = coords_to_pixels([p["pos"]], bbox_fr, largeur_carte, hauteur_total)
    pts = normalize_pts(raw)
    if not pts:
        continue
    x, y = pts[0]
    x = x * scale_boost + offset_x
    y = y * scale_boost + offset_y

    # Dessin du cercle et recuperation de l'ID
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

# Legende
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

while True:
    ev = donne_ev()

    if ev is not None:
        type_event = type_ev(ev)

        if type_event == "Quitte":
            break

        elif type_event == "ClicGauche":

            survoles = liste_objets_survoles()
            lieu_clique_nom = None

            # Cherche l'objet de lieu clique
            for obj_id in survoles:
                if obj_id in objets_lieux:
                    lieu_clique_nom = objets_lieux[obj_id]
                    break

            if lieu_clique_nom:
                # Affiche la page d'histoire (avec texte et image)
                affiche_histoire(lieu_clique_nom)
                # Une fois l'histoire affichee, la boucle attend un evenement "Quitte"
                # pour fermer la fenetre, car il n'y a plus de bouton de retour.

    mise_a_jour()

ferme_fenetre()