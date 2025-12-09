import shapefile
import os

import fltk
from fltk import *
from convert import coords_to_pixels
from description_lieu import HISTOIRES_DETAILLEES, affiche_histoire, HISTOIRE_TAG
from legende import init_dates, handle_survol


# Ce dictionnaire stockera : {ID_OBJET_CERCLE_FLTK: "Nom_du_Lieu"}
objets_lieux = {}
# Stocke : {ID_OBJET_POLYGON_FLTK: "Code_INSEE_Departement"}
objets_departements = {} 


# parametres
path = os.getcwd()
fichier_shp = path + "/departements-20180101-shp/departements-20180101.shp"

largeur_total, hauteur_total = 1200, 1000
largeur_legende = 200
largeur_carte = largeur_total - largeur_legende

# lecture du shapefile
sf = shapefile.Reader(fichier_shp)
records = sf.records()
all_shapes = sf.shapes()

depart:dict = {}
france_shapes:list = []
# Pour associer l'objet shapefile au code INSEE
depart_shapes_to_code = {} 

for shape, record in zip(all_shapes, records):
    code = record['code_insee']
    if code.isdigit() and 1 <= int(code) <= 95:
        depart[int(code)] = shape 
        france_shapes.append(shape)
        depart_shapes_to_code[shape] = code 
    elif code in ["2A", "2B"]:
        depart[code] = shape 
        france_shapes.append(shape)
        depart_shapes_to_code[shape] = code 

# bbox global
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

# NOUVEAU: Historique des BBox et Zoom. Commence avec la vue France entière.
historique_zoom = [(bbox_actuel.copy(), zoom_level)]


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


# Conversion et stockage des points du shapefile (sans dessin)
shapes_pixels_initial = []
for s in france_shapes:
    shape_parts_pixels = []
    if len(s.parts) == 1:
        pts_wgs84 = s.points
        raw_pts = coords_to_pixels(pts_wgs84, bbox_fr, largeur_carte, hauteur_total, marge=20)
        pts = normalize_pts(raw_pts)
        shape_parts_pixels.append(pts)
    else:
        for i in range(len(s.parts)):
            start = s.parts[i]
            end = s.parts[i + 1] if i + 1 < len(s.parts) else len(s.points)
            part_points = s.points[start:end]

            raw_pts = coords_to_pixels(part_points, bbox_fr, largeur_carte, hauteur_total, marge=20)
            pts = normalize_pts(raw_pts)
            shape_parts_pixels.append(pts)
    shapes_pixels_initial.append((shape_parts_pixels, s))


# Calcul de l'enveloppe pour info 
all_x = []
all_y = []
for shape_parts, _ in shapes_pixels_initial:
    for part in shape_parts:
        for x, y in part:
            all_x.append(x)
            all_y.append(y)

if not all_x or not all_y:
    all_x = [0]
    all_y = [0]

min_x, max_x = min(all_x), max(all_x)
min_y, max_y = min(all_y), max(all_y)

print(f"Dimensions carte en pixels: largeur={max_x-min_x:.1f}, hauteur={max_y-min_y:.1f}")

def dessiner_departements(shapes_data, bbox, tag_depart="carte"):
    """
    Fonction utilitaire pour dessiner les départements.
    """
    global objets_departements
    
    objets_departements.clear() 

    for shape_parts_pixels, s in shapes_data:
        code_insee = depart_shapes_to_code.get(s)
        
        if code_insee is None:
            continue
            
        # Re-calculer les pixels car la BBox (le zoom) a pu changer
        shapes_parts_zoom = []
        if len(s.parts) == 1:
            raw_pts = coords_to_pixels(s.points, bbox, largeur_carte, hauteur_total, marge=20)
            shapes_parts_zoom.append(normalize_pts(raw_pts))
        else:
            for i in range(len(s.parts)):
                start = s.parts[i]
                end = s.parts[i + 1] if i + 1 < len(s.parts) else len(s.points)
                part_points = s.points[start:end]
                
                raw_pts = coords_to_pixels(part_points, bbox, largeur_carte, hauteur_total, marge=20)
                shapes_parts_zoom.append(normalize_pts(raw_pts))


        # Dessiner toutes les parties du shape
        for part in shapes_parts_zoom:
            flat_pts = []
            for x, y in part:
                flat_pts.extend([x, y])
            
            poly_id = polygone(flat_pts, remplissage="#dddddd", couleur="#888888", epaisseur=1, tag=tag_depart)
            
            objets_departements[poly_id] = code_insee


def appliquer_zoom(new_zoom_level:float, centre_lon:float, centre_lat:float, enregistrer_historique=True):
    """
    Recalcule la BBox et redessine la carte entière avec le nouveau niveau de zoom.
    """
    global zoom_level, bbox_actuel, historique_zoom
    
    # Enregistrer l'état actuel AVANT le changement si c'est un zoom avant
    if enregistrer_historique and (new_zoom_level > zoom_level):
        historique_zoom.append((bbox_actuel.copy(), zoom_level))
    # Ne pas enregistrer si on est déjà revenu à la vue France entière et qu'on fait un zoom arrière
    elif enregistrer_historique and new_zoom_level < 1.0:
        return
        
    # Dimensions originales de la carte en WGS84
    lon_range_orig = lon_max - lon_min
    lat_range_orig = lat_max - lat_min
    
    # Nouvelles dimensions de la vue
    lon_range_zoom = lon_range_orig / new_zoom_level
    lat_range_zoom = lat_range_orig / new_zoom_level
    
    # Calcul de la nouvelle BBox centrée
    new_lon_min = centre_lon - lon_range_zoom / 2
    new_lon_max = centre_lon + lon_range_zoom / 2
    new_lat_min = centre_lat - lat_range_zoom / 2
    new_lat_max = centre_lat + lat_range_zoom / 2
    
    bbox_actuel = [new_lon_min, new_lat_min, new_lon_max, new_lat_max]
    zoom_level = new_zoom_level
    
    # --- Phase de Redessin ---
    efface("carte")
    efface("lieu")
    efface("legende_point")
    efface("code_departement_gros") 

    # Re-dessin des départements avec la NOUVELLE BBOX
    dessiner_departements(shapes_pixels_initial, bbox_actuel)
        
    # Dessiner les lieux
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
        
        objets_lieux[point_id] = p["nom"] 
        texte(x + 8, y - 4, p["nom"], taille=12, tag="legende_point")

    mise_a_jour()
    
# Prepare la fenetre
cree_fenetre(largeur_total, hauteur_total, redimension=False)

# Dessine les departements
dessiner_departements(shapes_pixels_initial, bbox_fr)


# Lieux specifiques
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
    {"nom": "Ancien Hopital Dreffeac", "pos": (-2.05, 47.50), "couleur": "green"},
    {"nom": "Chateau Mothe-Chandeniers", "pos": (0.03, 46.99), "couleur": "gold"},
    {"nom": "Fort Lupin", "pos": (-0.99, 45.87), "couleur": "darkblue"},
    {"nom": "Ancienne Gare Luxe", "pos": (0.13, 45.89), "couleur": "darkorange"},
]
dates_lieux = init_dates(lieux)


# Dessiner les lieux
for p in lieux:
    raw = coords_to_pixels([p["pos"]], bbox_fr, largeur_carte, hauteur_total, marge=20)
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

    objets_lieux[point_id] = p["nom"]
    texte(x + 8, y - 4, p["nom"], taille=12, tag="legende_point")

# Legende
x_legende = largeur_carte + 40
y_depart = 80
espacement = 60

texte(x_legende - 30, 40, "LEGENDE", taille=16, police="Helvetica Bold")
texte(x_legende - 30, hauteur_total - 100, "Touches: (+) Zoom In, \n (-) Zoom Out", taille=12)
# NOUVEAU: Instruction pour la touche 'a'
texte(x_legende - 30, hauteur_total - 60, "(a) Zoom Précédent/ \n France", taille=12, couleur="blue")


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
while True:
    ev = donne_ev()

    if ev is not None:
        type_event = type_ev(ev)

        if type_event == "Quitte":
            break

        elif type_event == "ClicGauche":

            x = abscisse(ev)
            y = ordonnee(ev)

            # Gestion de la fermeture de l'histoire
            if lieu_clique_status and (largeur_total - 50 < x < largeur_total and 0 < y < 50):
                efface(HISTOIRE_TAG)
                mise_a_jour()
                lieu_clique_status = False
                lieu_actuel = None
                continue
            
            # --- Identification de l'objet cliqué ---
            survoles = liste_objets_survoles()
            lieu_clique_nom = None
            departement_clique_code = None 

            for obj_id in survoles:
                if obj_id in objets_lieux:
                    lieu_clique_nom = objets_lieux[obj_id]
                    break
                elif obj_id in objets_departements:
                    departement_clique_code = objets_departements[obj_id]
                    
            if lieu_clique_nom:
                # Clic sur un lieu -> Afficher histoire
                lieu_actuel = lieu_clique_nom
                lieu_clique_status = True
                affiche_histoire(lieu_clique_nom, largeur_total)
            
            # --- LOGIQUE DE ZOOM SUR DEPARTEMENT ---
            elif departement_clique_code:
                
                dept_key = int(departement_clique_code) if departement_clique_code.isdigit() else departement_clique_code
                dept_shape = depart.get(dept_key) 
                
                if dept_shape:
                    bbox = dept_shape.bbox
                    
                    dept_lon_min, dept_lat_min, dept_lon_max, dept_lat_max = bbox
                    
                    centre_lon = (dept_lon_min + dept_lon_max) / 2
                    centre_lat = (dept_lat_min + dept_lat_max) / 2
                    
                    lon_range_orig = lon_max - lon_min
                    lat_range_orig = lat_max - lat_min
                    
                    target_lon_range = dept_lon_max - dept_lon_min
                    target_lat_range = dept_lat_max - dept_lat_min
                    
                    zoom_x = lon_range_orig / target_lon_range if target_lon_range > 0 else zoom_level
                    zoom_y = lat_range_orig / target_lat_range if target_lat_range > 0 else zoom_level
                        
                    new_zoom = min(zoom_x, zoom_y)
                    new_zoom *= 0.90 # Marge de 10%
                    
                    appliquer_zoom(new_zoom, centre_lon, centre_lat)
                    
                efface(HISTOIRE_TAG)
                lieu_clique_status = False
                lieu_actuel = None


        elif type_event == "Touche":
            touche_pressee = touche(ev)
            
            if touche_pressee == 'plus':
                # Zoom In
                zoom_factor_step = 1.2
                new_zoom_level = zoom_level * zoom_factor_step
                appliquer_zoom(new_zoom_level, (bbox_actuel[0]+bbox_actuel[2])/2, (bbox_actuel[1]+bbox_actuel[3])/2)
                
            elif touche_pressee == 'minus':
                # Zoom Out
                zoom_factor_step = 1.2
                new_zoom_level = max(1.0, zoom_level / zoom_factor_step)
                # Si on revient à 1.0, on vide l'historique sauf l'état initial
                if new_zoom_level == 1.0:
                    historique_zoom = [historique_zoom[0]] 
                
                appliquer_zoom(new_zoom_level, (bbox_actuel[0]+bbox_actuel[2])/2, (bbox_actuel[1]+bbox_actuel[3])/2, enregistrer_historique=False)
            
            elif touche_pressee == 'a':
                # NOUVEAU: Zoom Précédent
                if len(historique_zoom) > 1:
                    # On retire l'état le plus récent (l'état actuel)
                    historique_zoom.pop() 
                    
                    # On récupère l'état précédent
                    prev_bbox, prev_zoom = historique_zoom[-1]
                    
                    # Déterminer le centre de la BBox précédente pour l'appliquer
                    prev_centre_lon = (prev_bbox[0] + prev_bbox[2]) / 2
                    prev_centre_lat = (prev_bbox[1] + prev_bbox[3]) / 2

                    # Appliquer le zoom SANS enregistrer à nouveau dans l'historique
                    appliquer_zoom(prev_zoom, prev_centre_lon, prev_centre_lat, enregistrer_historique=False)
                    
                else:
                    # Si l'historique ne contient que la vue France entière (longueur 1), 
                    # on s'assure qu'on y est
                    prev_bbox, prev_zoom = historique_zoom[0]
                    prev_centre_lon = (prev_bbox[0] + prev_bbox[2]) / 2
                    prev_centre_lat = (prev_bbox[1] + prev_bbox[3]) / 2
                    appliquer_zoom(prev_zoom, prev_centre_lon, prev_centre_lat, enregistrer_historique=False)
    
    handle_survol(objets_lieux, dates_lieux)

    mise_a_jour()

ferme_fenetre()