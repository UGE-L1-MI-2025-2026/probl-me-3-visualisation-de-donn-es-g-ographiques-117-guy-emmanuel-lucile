from urllib import request,parse
import datetime
import locale
import re
from meteofrance_api import MeteoFranceClient
import pytz
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
picto ={
    "Belles Éclaircies": "pictogramme metéo/Belles Eclaircies.jpg",
    "Bancs de Brouillard": "pictogramme metéo/Brouillards Givrants.jpg", 
    "Brouillard": "pictogramme metéo/Brumes ou Brouillards.jpg",
    "Pluie": "VariableavecAverses.jpg", 
    "Pluie faible": "pictogramme metéo/Couvert, Bruines ou Pluies.jpg",
    "Couvert": "pictogramme metéo/Couvert.jpg",
    # Clés probables non confirmées :
     "Couvert, Neige faible": "pictogramme metéo/Couvert, Neige Faible.jpg",
     "Pluie forte": "pictogramme metéo/Couvert, Pluies Modérées ou fortes.jpg",
     "Neige forte": "pictogramme metéo/Neige Modérée ou Forte.jpg",
     "Orages Isolés": "pictogramme metéo/Orages Isolés.jpg",
     "Orages": "pictogramme metéo/Orages.jpg",
     "Ciel Voilé": "pictogramme metéo/Soleil Voilé.jpg",
     "Averses de Neige": "pictogramme metéo/Variable, Averses de Neige.jpg",
     "Averses de Neige": "pictogramme metéo/Variable, Averses de Neige.jpg",
     "Variable": "pictogramme metéo/Variable ou Nuageux.jpg",
    #fin
    "Eclaircies": "pictogramme metéo/Soleil.jpg",
    "Ciel clair": "pictogramme metéo/Soleil.jpg", 
    # ,
    "Très nuageux": "pictogramme metéo/Très Nuageux, Courtes Eclaircies.jpg",
    "Averses faibles": "pictogramme metéo/Variable avec Averses.jpg", 
    "Averses": "pictogramme metéo/Variable avec Averses.jpg"
}

client = MeteoFranceClient()
TIMEZONE =pytz.timezone('Europe/Paris')

date = "%A %d %B %Y - %H:%M:%S"
def meteo_lieu(lat,lont):
    prev = client.get_forecast(lat,lont)
    now =prev.daily_forecast
    f= {}
    z = 0
    for i in now:

        utc_dt = datetime.datetime.fromtimestamp(i["dt"], tz=pytz.utc)
        local_dt = utc_dt.astimezone(TIMEZONE)
        jour = local_dt.strftime(date)
        p = f"j{f"+{z}" if z != 0 else ""}"
        try:
            f[p] = i["weather12H"]["desc"]
        except KeyError:
            continue

        z +=1

    return f

def selection_picto(jour:int,lat,lon):
    """
   Args:
        jour:le jour de la prévision voulue aujourd'hui a 15 jour aprés soit 0 a 14
        lon, lat : postion du lieu de la prévis
        

    Returns:
        pred

    """
    indice = f"j{f"+{jour}" if jour != 0 else ""}"
    a = meteo_lieu(lat,lon)
    va_in = a[indice]
    res = ""
    try:
        res =picto[va_in]
    except KeyError as e:
        print(f"erreur clé :{e}") 
        res = 'pictogramme metéo/inconnud.jp'


    return res

test = selection_picto(0 ,2.3327, 48.8339)
print(test)