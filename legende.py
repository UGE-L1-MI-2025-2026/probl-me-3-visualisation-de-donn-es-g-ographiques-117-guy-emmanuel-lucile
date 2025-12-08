# affiche_date_survol.py
from fltk import *
import time

LAST_HOVER = None
LAST_OBJ = None

def init_dates(lieux):
    """
    Transforme la liste des lieux [{nom, pos, couleur}, ...]
    → dict { "NomLieu" : "Date" }
    """
    dates = {
        "Catacombes": "1786",
        "les thermes verts": "~1950",
        "Hopital abandonne": "~1990",
        "Cimetiere abandonne": "~1920",
        "Ecole abandonnee": "~1980",
        "Hopital psychiatrique de Bargeme": "~1970",
        "Fort de Cognelot": "~1880",
        "Goussainville Vieux-Pays": "1970",
        "Mine Cap Garonne": "~1960",
        "Sucrerie de Francieres": "~1955",
        "Chateau Pont-Remy": "~1950",
        "Fort de la Latte": "~1940",
        "Base Lann-Bihoue": "~2000",
        "Ferme fortifiee Montmartin": "~1800",
        "Ancien Hopital Dreffeac": "~1995",
        "Chateau Mothe-Chandeniers": "1932",
        "Fort Lupin": "~1950",
        "Ancienne Gare Luxe": "~1970",
    }

    # on ne retourne QUE les dates utiles
    final = {}
    for p in lieux:
        nom = p["nom"]
        if nom in dates:
            final[nom] = dates[nom]
    return final


def handle_survol(objets_lieux, dates_lieux):
    global LAST_HOVER, LAST_OBJ

    survol = liste_objets_survoles()

    for obj in survol:
        if obj in objets_lieux:
            nom = objets_lieux[obj]
            date = dates_lieux.get(nom, None)

            if date is None:
                return

            if LAST_OBJ != obj:
                # efface l'ancien texte
                if LAST_HOVER:
                    efface(LAST_HOVER)
                LAST_HOVER = None

                # affiche le nouveau
                x = abscisse_souris()
                y = ordonnee_souris() - 20
                LAST_HOVER = texte(
                    x, y,
                    f"{nom} : {date}",
                    couleur="red",
                    taille=14,
                    tag="hover_date"
                )
                LAST_OBJ = obj
            return

    # si on ne survole plus rien → on enlève le texte
    if LAST_HOVER:
        efface(LAST_HOVER)
        LAST_HOVER = None
        LAST_OBJ = None
