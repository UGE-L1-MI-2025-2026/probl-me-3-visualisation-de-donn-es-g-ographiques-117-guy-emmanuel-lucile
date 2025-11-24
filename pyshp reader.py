import shapefile
import os

path = os.getcwd()
fichier_texte = (
    path + "/departements-20180101-shp/departements-20180101.shp"
)
shape = shapefile.Reader(fichier_texte)
#first feature of the shapefile
feature = shape.shapeRecords()[0]
first = feature.shape.__geo_interface__
print(first) # (GeoJSON format)