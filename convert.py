

def coords_to_pixels(points, bbox, largeur_fenetre, hauteur_fenetre, marge=20):

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