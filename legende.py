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
                # efface l'ancien texte et rectangle
                if LAST_HOVER:
                    efface("hover_date")
                LAST_HOVER = None

                # affiche le nouveau
                x = abscisse_souris() - 1
                y = ordonnee_souris() - 20
                texte_str = f"{nom} : {date}"

                # calcul dynamique de la largeur basé sur la longueur du texte
                # environ 8 pixels par caractère pour taille=14
                largeur_texte = len(texte_str) * 9
                hauteur_texte = 20
                padding = 8

                # dessine le rectangle de fond d'abord
                rectangle(
                    x - padding, y - 2,
                    x + largeur_texte + padding, y + hauteur_texte,
                    remplissage="#f0f0f0",  # blanc doux
                    couleur="#888888",  # bordure grise
                    epaisseur=1,
                    tag="hover_date"
                )

                # dessine le texte par-dessus
                LAST_HOVER = texte(
                    x, y,
                    texte_str,
                    couleur="red",
                    taille=14,
                    tag="hover_date",
                    ancrage="nw"
                )
                LAST_OBJ = obj
            return

    # si on ne survole plus rien → on enlève le texte et le rectangle
    if LAST_HOVER:
        efface("hover_date")
        LAST_HOVER = None
        LAST_OBJ = None
