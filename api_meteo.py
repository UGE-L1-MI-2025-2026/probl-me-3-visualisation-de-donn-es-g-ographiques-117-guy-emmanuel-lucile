from urllib import request,parse
import datetime
import locale
import re
from meteofrance_api import MeteoFranceClient
import pytz
 
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
picto ={"brouillard":"pictogramme metéo/brouillard.png",
        "couvert":"pictogramme metéo/couvert.png",
        "nuageux":"pictogramme metéo/trés_nuageux.png",
        "neige":"pictogramme metéo/neiged.png",
        "pluie":"pictogramme metéo/pluie.png",
        "soileil":"pictogramme metéo/soleil.png"
        "198310":,

        }
client = MeteoFranceClient()
TIMEZONE =pytz.timezone('Europe/Paris')


date = "%A %d %B %Y � %H:%M:%S"
def meteo_lieu(lat,lont):
    prev = client.get_forecast(48.865205,2.509142)
    now =prev.daily_forecast
    f= {}
    z = 0
    for i in now:

        utc_dt = datetime.datetime.fromtimestamp(i["dt"], tz=pytz.utc)
        local_dt = utc_dt.astimezone(TIMEZONE)
        jour = local_dt.strftime(date)
        f[f"j{f"+{z}" if z != 0 else ""}"] = i["weather12H"]["desc"]

        z +=1

    return f

def selection_picto():
    chemin = ""




    return chemin


print(meteo_lieu(48.865205,2.509142))