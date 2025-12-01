# interaction.py
# Gère l'affichage du titre et de la description (texte) de l'histoire.

import fltk
from typing import Dict, Any

# --- Constantes FLTK pour l'Overlay ---
HISTOIRE_TAG = "history_overlay"
HISTORY_BACKGROUND = "#f0f0f0" 

# --- Données d'Histoires (Chemins d'images conservés pour référence mais non utilisés) ---
HISTOIRES_DETAILLEES = {
    "Catacombes": {
        "nom": "Catacombes de Paris",
        "histoire": ("Anciennes carrières souterraines aménagées en ossuaire au XVIIIe siècle. Elles abritent les restes d'environ six millions de Parisiens."),
        "image_path": "image/catacombes.gif" 
    },
    "Bunker Gare de l'Est": {
        "nom": "Bunker de la Gare de l'Est",
        "histoire": ("Ce bunker, construit sous la Gare de l'Est pendant la Seconde Guerre mondiale, servait de refuge et de poste de commandement pour la direction des chemins de fer."),
        "image_path": "image/bunker.gif"
    },
    "les thermes verts": {
        "nom": "Les Thermes Verts (Clermont-Ferrand)",
        "histoire": ("Vestiges d'une ancienne station thermale réputée, aujourd'hui laissée à l'abandon. Le lieu est célèbre pour son architecture délabrée."),
        "image_path": "image/thermes.gif"
    },
    "Station fantôme Croix-Rouge": {
        "nom": "Station Fantôme Croix-Rouge",
        "histoire": "Fermée depuis 1939 au début de la Seconde Guerre mondiale. Un véritable voyage dans le temps sous les rues de Paris.",
        "image_path": "image/croix_rouge.gif"
    },
    "Hôpital abandonné": {
        "nom": "Ancien Hôpital Militaire (Lyon)",
        "histoire": "Ses couloirs vides et ses salles d'opération laissées à l'abandon racontent des milliers d'histoires de vie et de mort.",
        "image_path": "image/hopital.gif"
    },
    "Cimetière abandonné": {
        "nom": "Nécropole Oubliée (Toulouse)",
        "histoire": "Un cimetière historique dont l'entretien a cessé. Les tombes sont envahies par la végétation.",
        "image_path": "image/cimetiere.gif"
    },
    "École abandonnée": {
        "nom": "Lycée Désaffecté (Bordeaux)",
        "histoire": "Fermée après un regroupement scolaire, cette grande école est un exemple de patrimoine éducatif figé dans le temps.",
        "image_path": "image/ecole.gif"
    },
    "sanatorium": {
        "nom": "Sanatorium de la Forêt Noire",
        "histoire": "Construit au début du XXe siècle pour traiter la tuberculose, il a été abandonné avec la découverte de traitements efficaces.",
        "image_path": "image/sanatorium.gif"
    },
}

# --- Fonction d'Affichage d'Histoire ---

def affiche_histoire(
    lieu_id: str
) -> None:
    """
    Affiche un overlay contenant uniquement le titre et la description.
    """
    
    histoire_data = HISTOIRES_DETAILLEES.get(lieu_id)
    if not histoire_data:
        return

    WINDOW_W = fltk.largeur_fenetre()
    WINDOW_H = fltk.hauteur_fenetre()
    
    # --- 1. Arrière-plan (couvre tout) ---
    fltk.rectangle(
        0, 0, WINDOW_W, WINDOW_H,
        remplissage=HISTORY_BACKGROUND,
        couleur=HISTORY_BACKGROUND, 
        tag=HISTOIRE_TAG,
        epaisseur=0
    )

    # --- 2. Titre (Centré en haut) ---
    fltk.texte(
        WINDOW_W // 2, 50, histoire_data['nom'],
        taille=30,
        ancrage="n", 
        couleur="#333333",
        tag=HISTOIRE_TAG,
        police="Helvetica Bold"
    )
    
    # --- 3. Texte de l'histoire (positionné sous le titre) ---
    y_text_start = 120 # Début du texte sous le titre
    texte_histoire = histoire_data['histoire']
    
    lignes = texte_histoire.split('. ')
    y_current = y_text_start
    
    for ligne in lignes:
        if ligne:
            text_to_draw = ligne if ligne.endswith('.') else ligne + '.'
            fltk.texte(
                WINDOW_W // 2, y_current,
                text_to_draw,
                taille=16,
                ancrage="n",
                couleur="black",
                tag=HISTOIRE_TAG
            )
            y_current += 25 # Espacement vertical