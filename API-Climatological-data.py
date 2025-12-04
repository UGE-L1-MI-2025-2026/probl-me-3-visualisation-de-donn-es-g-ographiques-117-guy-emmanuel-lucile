from bs4 import BeautifulSoup
from urllib import request,parse
import datetime
import re

#truc jamais a faire mais flemme
FORMAT_ISO = "%Y-%m-%dT%H:%M:%SZ"
try:
    with open("apikey","r") as f:
        api_key = f.read().strip() 
except FileNotFoundError:
    print("\u274c FATALITÉ : Le fichier 'apikey' est introuvable")


def fectStation(departement:int,frequence,all:bool):
    liste_departements = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", 
    "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", 
    "2A", "2B", # Corse (corrigés pour le format d'API, souvent utilisés comme 20)
    "21", "22", "23", "24", "25", "26", "27", "28", "29", 
    "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", 
    "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", 
    "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", 
    "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", 
    "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", 
    "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", 
    "90", "91", "92", "93", "94", "95", 
    # Outre-mer (DOM-TOM)
    "971", # Guadeloupe
    "972", # Martinique
    "973", # Guyane
    "974", # La Réunion
    "976", # Mayotte
    "975", # Saint-Pierre-et-Miquelon (Collectivité d'outre-mer)
    "99"   # Autres collectivités (Monaco n'étant pas un département)

]
    try:
        assert frequence in ["6min","heure",'quotidien']
    except:
        while frequence not in["6min","heure",'quotidien']:
            frequence = str(input("veuillez mettre une valeur [6min,heure,quotidien] svp: "))

    try:
        assert departement in liste_departements
    except:
        while str(departement) not in liste_departements:
            frequence = str(input("veuillez mettre une valeur [6min,heure,quotidien] svp: "))

    global api_key




    return






def min6(
    id_station:int,
    dateDebut:str = "2000-01-01T05:06:00Z",
    datefin:str ="2000-02-01T05:06:00Z"
     
):
    try:
        dt_debut =         datetime.datetime.strptime(dateDebut, FORMAT_ISO)
        dt_fin =         datetime.datetime.strptime(datefin, FORMAT_ISO)

        if dt_debut >= dt_fin:
            raise ValueError("L'ORDRE EST VIOLé : la date de début doit étre strictement antérieure à la date de fin.")

    except ValueError as e:
        print(f"\u274c FATALITé DE FORMAT/ORDRE : {e}. Format voulu : {FORMAT_ISO}")
        return None 

    global api_key

    
    serveur = "https://public-api.meteofrance.fr/public/DPClim/v1"
    ressource = ""
    # AAAA-MM-JJThh:mm:00Z. 
    service = "/commande-station/infrahoraire-6m"
    url = f"{serveur}{service}?id-station={id_station}&date-deb-periode={parse.quote(dateDebut)}&date-fin-periode={parse.quote(datefin)}{ressource}&apikey={parse.quote(api_key)}"
    return url

def minquotidien(
    id_station: int,
    # Correction s�mantique: donn�es quotidiennes => minuit (T00:00:00Z)
    dateDebut: str = "2000-01-01T00:00:00Z",
    datefin: str = "2000-02-01T00:00:00Z"
) -> str | None:
    
    try:
        dt_debut =         datetime.datetime.strptime(dateDebut, FORMAT_ISO)
        dt_fin =         datetime.datetime.strptime(datefin, FORMAT_ISO)
        
        if dt_debut >= dt_fin:
            raise ValueError("L'ORDRE EST VIOLé : la date de début doit étre strictement antérieure à la date de fin.")
            
    except ValueError as e:
        print(f"\u274c FATALITé DE FORMAT/ORDRE : {e}. Format voulu : {FORMAT_ISO}")
        return None 
    
    global api_key

    
    serveur = "https://public-api.meteofrance.fr/public/DPClim/v1"
    service = "/commande-station/quotidienne"
    
    url = (
        f"{serveur}{service}"
        f"?id-station={id_station}"
        f"&date-deb-periode={parse.quote(dateDebut)}"
        f"&date-fin-periode={parse.quote(datefin)}"
        f"&apikey={parse.quote(api_key)}" 
    )
    return url

def telecharge(code):
    res = ""
    serveur = "https://public-api.meteofrance.fr/public/DPClim/v1"
    comande = "/commande/fichier"
 
    global api_key


    url = f"{serveur}{comande}id-cmde={code}&apikey={api_key}"
    res =request.urlopen(url)

    res =BeautifulSoup(res.read())


    



    return res

url = minquotidien(77339001)
def code(url):
    t=request.urlopen(url)
    b = t.read()
    k=BeautifulSoup(b,features="html.parser")
    j = eval(str(k))
    print(j["elaboreProduitAvecDemandeResponse"]["return"])
    return j["elaboreProduitAvecDemandeResponse"]["return"]


print(url)
c =code(url)

telecharge(c)