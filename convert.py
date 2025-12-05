import math

# CONVERSION WGS 84 -> PIXELS

def coords_to_pixels(points, bbox, largeur_fenetre, hauteur_fenetre, marge=20):
    """
    Convertit des coordonnées WGS 84 en pixels pour affichage.

    Args:
        points: Liste de tuples (longitude, latitude) en degrés
        bbox: [lon_min, lat_min, lon_max, lat_max]
        largeur_fenetre: Largeur de la fenêtre en pixels
        hauteur_fenetre: Hauteur de la fenêtre en pixels
        marge: Marge en pixels

    Returns:
        Liste plate [x1, y1, x2, y2, ...] de coordonnées en pixels
    """
    lon_min, lat_min, lon_max, lat_max = bbox

    # Dimensions utiles (avec marges, pour faire le dessin dans notre fenetre)
    largeur_utile = largeur_fenetre - 2 * marge
    hauteur_utile = hauteur_fenetre - 2 * marge

    # Calcul des échelles (il faut utiliser chaque degré pour chaque pixel qu'on a)
    echelle_x = largeur_utile / (lon_max - lon_min)
    echelle_y = hauteur_utile / (lat_max - lat_min)

    # Utiliser la même échelle pour garder les proportions
    echelle = min(echelle_x, echelle_y)

    # Conversion des points
    pixels = []
    for lon, lat in points:
        # Conversion longitude -> x
        x = marge + (lon - lon_min) * echelle

        # Conversion latitude -> y (attention : y inversé car lat augmente vers le haut)
        y = hauteur_fenetre - marge - (lat - lat_min) * echelle

        pixels.extend([x, y])

    return pixels


# PROJECTION DE MERCATOR

def wgs84_to_mercator(lon, lat):
    """
    Convertit des coordonnées WGS 84 en projection de Mercator.

    La projection de Mercator est une projection cylindrique qui préserve
    les angles mais déforme les aires (exagère les zones proches des pôles).

    Args:
        lon: Longitude en degrés (-180 à 180)
        lat: Latitude en degrés (-85.05 à 85.05)

    Returns:
        Tuple (x, y) en coordonnées Mercator (en mètres)
    """
    # Rayon de la Terre en mètres (WGS 84)
    R = 6378137.0

    # Limite de latitude pour éviter la singularité aux pôles
    lat = max(min(lat, 85.05), -85.05)

    # Conversion en radians
    lon_rad = math.radians(lon)
    lat_rad = math.radians(lat)

    # Formules de Mercator
    x = R * lon_rad
    y = R * math.log(math.tan(math.pi / 4 + lat_rad / 2))

    return (x, y)


def mercator_to_wgs84(x, y):
    """
    Convertit des coordonnées Mercator en WGS 84.

    Args:
        x: Coordonnée x en mètres
        y: Coordonnée y en mètres

    Returns:
        Tuple (longitude, latitude) en degrés
    """
    # Rayon de la Terre en mètres
    R = 6378137.0

    # Conversion inverse
    lon_rad = x / R
    lat_rad = 2 * math.atan(math.exp(y / R)) - math.pi / 2

    # Conversion en degrés
    lon = math.degrees(lon_rad)
    lat = math.degrees(lat_rad)

    return (lon, lat)


def coords_to_pixels_mercator(points, bbox, largeur_fenetre, hauteur_fenetre, marge=20):
    """
    Convertit des coordonnées WGS 84 en pixels en utilisant la projection Mercator.

    Cette fonction applique d'abord la projection Mercator, puis convertit en pixels.
    Utile pour avoir un rendu plus réaliste des distances horizontales.

    Args:
        points: Liste de tuples (longitude, latitude) en degrés
        bbox: [lon_min, lat_min, lon_max, lat_max] en degrés
        largeur_fenetre: Largeur de la fenêtre en pixels
        hauteur_fenetre: Hauteur de la fenêtre en pixels
        marge: Marge en pixels

    Returns:
        Liste plate [x1, y1, x2, y2, ...] de coordonnées en pixels
    """
    lon_min, lat_min, lon_max, lat_max = bbox

    # Conversion de la bbox en Mercator
    bbox_merc_min = wgs84_to_mercator(lon_min, lat_min)
    bbox_merc_max = wgs84_to_mercator(lon_max, lat_max)

    x_min, y_min = bbox_merc_min
    x_max, y_max = bbox_merc_max

    # Dimensions utiles
    largeur_utile = largeur_fenetre - 2 * marge
    hauteur_utile = hauteur_fenetre - 2 * marge

    # Échelles
    echelle_x = largeur_utile / (x_max - x_min)
    echelle_y = hauteur_utile / (y_max - y_min)
    echelle = min(echelle_x, echelle_y)

    # Conversion des points
    pixels = []
    for lon, lat in points:
        # D'abord en Mercator
        x_merc, y_merc = wgs84_to_mercator(lon, lat)

        # Puis en pixels
        x = marge + (x_merc - x_min) * echelle
        y = hauteur_fenetre - marge - (y_merc - y_min) * echelle

        pixels.extend([x, y])

    return pixels


# UTILITAIRES

def calculate_bbox(points):
    """
    Calcule la bounding box d'une liste de points.

    Args:
        points: Liste de tuples (longitude, latitude)

    Returns:
        [lon_min, lat_min, lon_max, lat_max]
    """
    if not points:
        return [0, 0, 0, 0]

    lons = [p[0] for p in points]
    lats = [p[1] for p in points]

    return [min(lons), min(lats), max(lons), max(lats)]


def haversine_distance(lon1, lat1, lon2, lat2):
    """
    Calcule la distance en kilomètres entre deux points sur Terre.
    Utilise la formule de Haversine.

    Args:
        lon1, lat1: Coordonnées du premier point (degrés)
        lon2, lat2: Coordonnées du second point (degrés)

    Returns:
        Distance en kilomètres
    """
    # Rayon de la Terre en km
    R = 6371.0

    # Conversion en radians
    lon1_rad = math.radians(lon1)
    lat1_rad = math.radians(lat1)
    lon2_rad = math.radians(lon2)
    lat2_rad = math.radians(lat2)

    # Différences
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # Formule de Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c
    return distance


def is_point_in_france_metro(lon, lat):
    """
    Vérifie approximativement si un point est en France métropolitaine.

    Args:
        lon: Longitude en degrés
        lat: Latitude en degrés

    Returns:
        True si le point est probablement en France métropolitaine
    """
    # Bounding box approximative de la France métropolitaine
    # Longitude: de -5° (Bretagne) à 10° (Alpes)
    # Latitude: de 41° (Corse) à 51° (Nord)
    return -5 <= lon <= 10 and 41 <= lat <= 51


# EXEMPLE D'UTILISATION

# Ce bloc s'execute seulement quand on lance ce fichier directement
# (pas quand on l'import dans un autre fichier)
# Il sert a tester les fonctions du module pour verifier qu'elles marchent bien

if __name__ == "__main__":
    print("=== Module de conversion de coordonnées ===\n")

    # Test 1: Conversion Mercator avec Paris
    paris_lon, paris_lat = 2.3522, 48.8566
    print(f"Paris: ({paris_lon}, {paris_lat})")

    x_merc, y_merc = wgs84_to_mercator(paris_lon, paris_lat)
    print(f"En Mercator: ({x_merc:.2f}, {y_merc:.2f}) metres")

    # Verification: conversion inverse
    lon_back, lat_back = mercator_to_wgs84(x_merc, y_merc)
    print(f"Retour WGS84: ({lon_back:.4f}, {lat_back:.4f})")

    # Test 2: Calcul de distance
    marseille_lon, marseille_lat = 5.3698, 43.2965
    distance = haversine_distance(paris_lon, paris_lat, marseille_lon, marseille_lat)
    print(f"\nDistance Paris-Marseille: {distance:.2f} km")

    # Test 3: Bounding box
    points = [(2.0, 48.0), (3.0, 49.0), (2.5, 48.5)]
    bbox = calculate_bbox(points)
    print(f"\nBbox de {len(points)} points: {bbox}")

    # Test 4: Conversion en pixels (pour affichage sur fenetre 800x600)
    pixels_wgs = coords_to_pixels(points, bbox, 800, 600)
    print(f"\nPixels (WGS84): {pixels_wgs[:6]}...")

    pixels_merc = coords_to_pixels_mercator(points, bbox, 800, 600)
    print(f"Pixels (Mercator): {pixels_merc[:6]}...")

    print("\nModule pret a l'emploi")
    print("Utilisez coords_to_pixels() pour WGS84 simple")
    print("Utilisez coords_to_pixels_mercator() pour projection Mercator")
