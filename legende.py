# zoom_departement.py
from pyshp_reader import depart, bbox_fr, largeur_carte, hauteur_total, coords_to_pixels, polygone, efface, mise_a_jour

def zoom_sur_departement(code_departement: str, marge: int = 20, facteur_zoom: float = 1.5):
    """
    Zoom sur un département donné.
    
    Args:
        code_departement (str): code INSEE du département (ex: "75" ou "2A")
        marge (int): marge en pixels autour du département
        facteur_zoom (float): facteur de zoom pour agrandir le département
    """
    if code_departement not in depart:
        print(f"Département {code_departement} non trouvé")
        return

    shape = depart[code_departement]
    # Calcul de la bbox du département
    x_min, y_min, x_max, y_max = shape.bbox
    centre_lon = (x_min + x_max) / 2
    centre_lat = (y_min + y_max) / 2
    lon_range = (x_max - x_min) * facteur_zoom
    lat_range = (y_max - y_min) * facteur_zoom

    # Nouvelle bbox centrée sur le département
    bbox_zoom = [
        centre_lon - lon_range / 2,
        centre_lat - lat_range / 2,
        centre_lon + lon_range / 2,
        centre_lat + lat_range / 2
    ]

    # Efface la carte
    efface("carte")

    # Re-dessine le département en grand
    if len(shape.parts) == 1:
        pts = coords_to_pixels(shape.points, bbox_zoom, largeur_carte, hauteur_total, marge)
        polygone([coord for xy in pts for coord in xy], remplissage="#dddddd", couleur="#888888", epaisseur=2, tag="carte")
    else:
        for i in range(len(shape.parts)):
            start = shape.parts[i]
            end = shape.parts[i + 1] if i + 1 < len(shape.parts) else len(shape.points)
            pts = coords_to_pixels(shape.points[start:end], bbox_zoom, largeur_carte, hauteur_total, marge)
            polygone([coord for xy in pts for coord in xy], remplissage="#dddddd", couleur="#888888", epaisseur=2, tag="carte")

    mise_a_jour()
