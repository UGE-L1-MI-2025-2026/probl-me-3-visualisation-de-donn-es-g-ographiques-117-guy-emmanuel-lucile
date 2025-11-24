import shapefile
import os

path = os.getcwd()
fichier_texte = (
    path + "/departements-20180101-shp/departements-20180101.shp"
)
sf = shapefile.Reader(fichier_texte)
records = sf.records()
print(records)
seine_et_marne = sf.shape(47)
print(seine_et_marne.bbox)
print(seine_et_marne.points)

