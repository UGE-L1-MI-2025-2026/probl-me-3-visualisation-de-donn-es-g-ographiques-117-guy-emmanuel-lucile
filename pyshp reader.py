import shapefile
import os
from fltk import *
from convert import coords_to_pixels

path = os.getcwd()
fichier_texte = (
    path + "/departements-20180101-shp/departements-20180101.shp"
)

sf = shapefile.Reader(fichier_texte)

records = sf.records() # il y a 102 departements

france_shape = sf.shapes()

lon_min_fr = min(shape.bbox[0] for shape in france_shape)
lat_min_fr = min(shape.bbox[1] for shape in france_shape)
lon_max_fr = max(shape.bbox[2] for shape in france_shape)
lat_max_fr = max(shape.bbox[3] for shape in france_shape)

bbox_fr = [lon_min_fr, lat_min_fr, lon_max_fr, lat_max_fr]

largeur, hauteur = 1000, 1000
cree_fenetre(largeur, hauteur)

for i, shape in enumerate(france_shape):
    points = coords_to_pixels(shape.points, bbox_fr, largeur, hauteur)
    polygone(points)

attend_ev()
