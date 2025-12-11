from urllib import request,parse
import datetime
import locale
import re
from meteofrance_api import MeteoFranceClient
import pytz
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
picto ={
    "":"pictogramme metéo/Belles Eclaircies.jpg",
    "":"pictogramme metéo/Brouillards Givrants.jpg",
    "Bancs de Brouillard":"pictogramme metéo/Brumes ou Brouillards.jpg",
    "Pluie faible":"pictogramme metéo/Couvert, Bruines ou Pluies.jpg",
    "Couvert":"pictogramme metéo/Couvert.jpg",
    "":"pictogramme metéo/Couvert, Neige Faible.jpg",
    "":"pictogramme metéo/Couvert, Pluies Modérées ou fortes.jpg",
    "":"pictogramme metéo/Neige Modérée ou Forte.jpg",
    "":"pictogramme metéo/Orages Isolés.jpg",
    "":"pictogramme metéo/Orages.jpg",
    "Eclaircies":"pictogramme metéo/Soleil.jpg",
    "":"pictogramme metéo/Soleil Voilé.jpg",
    "Très nuageux":"pictogramme metéo/Très Nuageux, Courtes Eclaircies.jpg",
    "Pluie":"pictogramme metéo/Variable avec Averses.jpg",
    "":"pictogramme metéo/Variable, Averses de Neige.jpg",
    "":"pictogramme metéo/Variable ou Nuageux.jpg"
        
        }
client = MeteoFranceClient()
TIMEZONE =pytz.timezone('Europe/Paris')

date = "%A %d %B %Y - %H:%M:%S"
def meteo_lieu(lat,lont):
    prev = client.get_forecast(48.865205,2.509142)
    now =prev.daily_forecast
    f= {}
    z = 0
    for i in now:

        utc_dt = datetime.datetime.fromtimestamp(i["dt"], tz=pytz.utc)
        local_dt = utc_dt.astimezone(TIMEZONE)
        jour = local_dt.strftime(date)
        p = f"j{f"+{z}" if z != 0 else ""}"
        f[p] = i["weather12H"]["desc"]

        z +=1

    return f

def selection_picto(jour:int,lon,lat):
    """
   Args:
        jour:le jour de la prévision voulue aujourd'hui a 15 jour aprés soit 0 a 14
        lon, lat : postion du lieu de la prévis
        

    Returns:
        pred

    """
    indice = f"j{f"+{jour}" if jour != 0 else ""}"
    a = meteo_lieu(lon,lat)
    va_in = a[indice]
    res =picto[va_in]


    return res


tes =selection_picto(0,48.865205,2.509142)
print(tes)