from urllib import request,parse
import datetime
import re
import meteofrance_api
 


bil = meteofrance_api.client.MeteoFranceClient
picto ={"brouillard":"pictogramme metéo/brouillard.png",
        "couvert":"pictogramme metéo/couvert.png",
        "nuageux":"pictogramme metéo/trés_nuageux.png",
        "neige":"pictogramme metéo/neiged.png",
        "pluie":"pictogramme metéo/pluie.png",
        "soileil":"pictogramme metéo/soleil.png"
        }
meteo = bil()
k = meteo.get_warning_full
prev = meteo.get_forecast(48.865205,2.509142)
now =prev.daily_forecast
d =prev.forecast

print(k.image_url)
for i in d:
    print(i,"\n")



FORMAT_ISO = "%Y-%m-%dT%H:%M:%SZ"
def mete0_lieu(lat,lont):
    prev = meteo.get_forecast(48.865205,2.509142)
    now =prev.daily_forecast


