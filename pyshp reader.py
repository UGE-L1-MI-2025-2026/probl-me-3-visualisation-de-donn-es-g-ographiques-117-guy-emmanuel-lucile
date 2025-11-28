import shapefile
import os

from fltk import *
from convert import coords_to_pixels

path = os.getcwd()
fichier_texte = (
    path + "/departements-20180101-shp/departements-20180101.shp"
)

sf = shapefile.Reader(fichier_texte)

all_records = sf.records() # il y a 102 départements
all_shapes = sf.shapes()

metro_shapes = []
metro_records = []

DOM_TOM = ['971', '972', '973', '974', '976']

for i in range(len(all_records)):
    code_dep = str(all_records[i][0])
    nom_dep = all_records[i][1]

    if code_dep not in DOM_TOM:
        metro_shapes.append(all_shapes[i])
        metro_records.append(all_records[i])

print(metro_shapes)

lon_min_fr = min(shape.bbox[0] for shape in metro_shapes)
lat_min_fr = min(shape.bbox[1] for shape in metro_shapes)
lon_max_fr = max(shape.bbox[2] for shape in metro_shapes)
lat_max_fr = max(shape.bbox[3] for shape in metro_shapes)

bbox_fr = [lon_min_fr, lat_min_fr, lon_max_fr, lat_max_fr]

largeur, hauteur = 1000, 1000
cree_fenetre(largeur, hauteur)

for i, shape in enumerate(metro_shapes):
    points = coords_to_pixels(shape.points, bbox_fr, largeur, hauteur)
    polygone(points)

mise_a_jour()
attend_ev()

