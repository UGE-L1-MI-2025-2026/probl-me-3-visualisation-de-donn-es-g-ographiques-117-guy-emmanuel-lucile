import shapefile
import os
from fltk import *

path = os.getcwd()
fichier_texte = (
    path + "/departements-20180101-shp/departements-20180101.shp"
)
sf = shapefile.Reader(fichier_texte)
records = sf.records()
#print(records)
seine_et_marne = sf.shape(47)
#print(seine_et_marne.bbox)
#print(seine_et_marne.points)

cree_fenetre(500,500)

rectangle(0,0, 250, 250)


