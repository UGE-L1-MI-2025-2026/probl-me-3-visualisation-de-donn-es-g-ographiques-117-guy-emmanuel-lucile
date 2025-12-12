# interaction.py
# Gère l'affichage du titre et de la description (texte) de l'histoire.

import fltk


# --- Constantes FLTK pour l'Overlay ---
HISTOIRE_TAG = "history_overlay"
HISTORY_BACKGROUND = "#856c6c" 
image=()

# --- Données d'Histoires (Chemins d'images conservés pour référence mais non utilisés) ---
HISTOIRES_DETAILLEES = {
    "Catacombes": {
        "nom": "Catacombes de Paris",
        "histoire": ("Anciennes carrières souterraines aménagées en ossuaire au XVIIIe siècle. Elles abritent les restes d'environ six millions de Parisiens."),
    },
    "les thermes verts": {
        "nom": "Les Thermes Verts (Clermont-Ferrand)",
        "histoire": ("Vestiges d'une ancienne station thermale réputée, aujourd'hui laissée à l'abandon. Le lieu est célèbre pour son architecture délabrée."),
        
    },
    "Hopital abandonne": {
        "nom": "Ancien Hôpital Militaire (Lyon)",
        "histoire": "Ses couloirs vides et ses salles d'opération laissées à l'abandon racontent des milliers d'histoires de vie et de mort.",
        
    },
    "Cimetiere abandonné": {
        "nom": "Nécropole Oubliée (Toulouse)",
        "histoire": "Un cimetière historique dont l'entretien a cessé. Les tombes sont envahies par la végétation.",
        
    },
    "Ecole abandonnée": {
        "nom": "Lycée Désaffecté (Bordeaux)",
        "histoire": "Fermée après un regroupement scolaire, cette grande école est un exemple de patrimoine éducatif figé dans le temps.",
        
    },
    "Hopital psychiatrique de Bargeme": {
        "nom": "Hôpital Psychiatrique de Bargème",
        "histoire": "Un ancien hôpital psychiatrique situé dans le sud de la France, connu pour son architecture imposante et son histoire troublée.",
        
    },
    "Fort de Cognelot": {
        "nom": "Fort de Cognelot",
        "histoire": "Un fort militaire du XIXe siècle situé en Bourgogne, aujourd'hui abandonné et envahi par la végétation.",
        
    },
    "Goussainville Vieux-Pays": {
        "nom": "Goussainville Vieux-Pays",
        "histoire": "Un village fantôme près de l'aéroport Charles de Gaulle, abandonné après des nuisances sonores excessives.",
        
    },
    "Mine Cap Garonne": {
        "nom": "Mine Cap Garonne",
        "histoire": "Une ancienne mine de charbon située dans le sud de la France, aujourd'hui abandonnée et ouverte aux explorateurs urbains.",
        
    },
    "Sucrerie de Francieres": {
        "nom": "Sucrerie de Franières",
        "histoire": "Une ancienne sucrerie située dans le nord de la France, abandonnée après la fermeture de l'industrie sucrière locale.",
        
    },
    "Chateau Pont-Remy": {
        "nom": "Château de Pont-Rémy",
        "histoire": "Un château historique situé en Picardie, aujourd'hui en ruines et entouré de légendes locales.",
        
    },
    "Fort de la Latte": {
        "nom": "Fort de la Latte",
        "histoire": "Un fort médiéval situé en Bretagne, célèbre pour son architecture impressionnante et son histoire militaire.",
        
    },
    "Base Lann-Bihoue": {
        "nom": "Base Aéronavale de Lann-Bihoué",
        "histoire": "Une ancienne base aéronavale en Bretagne, aujourd'hui partiellement abandonnée et utilisée pour des exercices militaires.",
        
    },
    "Ferme fortifiee Montmartin": {
        "nom": "Ferme Fortifiée de Montmartin",
        "histoire": "Une ferme médiévale fortifiée située en Normandie, aujourd'hui abandonnée et envahie par la végétation.",
        
    },
    "Ancien Hopital Dreffeac": {
        "nom": "Ancien Hôpital de Dréfféac",
        "histoire": "Un ancien hôpital situé en Bretagne, connu pour son architecture imposante et son histoire médicale.",
    
    },
    "Chateau Mothe-Chandeniers": {
        "nom": "Château de la Mothe-Chandeniers",
        "histoire": "Un château romantique en ruines situé dans la Vienne, célèbre pour son architecture pittoresque et son histoire fascinante.",
        
    },
    "Fort Lupin": {
        "nom": "Fort Lupin",
        "histoire": "Un fort côtier situé en Charente-Maritime, construit au XIXe siècle pour défendre la côte atlantique.",
        
    },
    "Ancienne Gare Luxe": {
        "nom": "Ancienne Gare de Luxe",
        "histoire": "Une gare désaffectée située en Nouvelle-Aquitaine, autrefois un point névralgique du transport ferroviaire régional.",
        
    },


}

# --- Fonction d'Affichage d'Histoire ---

def affiche_histoire(
    lieu_id: str, largeur
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
        couleur="#170707",
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
            fltk.rectangle(largeur - 50, 50, largeur, 0, tag=HISTOIRE_TAG, epaisseur=3)
            fltk.ligne(largeur - 45, 45, largeur - 5, 5, tag=HISTOIRE_TAG, epaisseur=2, couleur="red")
            fltk.ligne(largeur - 5, 45, largeur - 45, 5, tag=HISTOIRE_TAG, epaisseur=2, couleur="red")


            y_current += 25 # Espacement vertical