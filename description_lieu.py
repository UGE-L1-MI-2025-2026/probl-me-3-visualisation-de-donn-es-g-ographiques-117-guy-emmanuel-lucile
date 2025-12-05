# interaction.py
# Gère l'affichage du titre et de la description (texte) de l'histoire.

import fltk


# --- Constantes FLTK pour l'Overlay ---
HISTOIRE_TAG = "history_overlay"
HISTORY_BACKGROUND = "#f0f0f0" 
image=()

# --- Données d'Histoires (Chemins d'images conservés pour référence mais non utilisés) ---
HISTOIRES_DETAILLEES = {
    "Catacombes": {
        "nom": "Catacombes de Paris",
        "histoire": ("Anciennes carrières souterraines aménagées en ossuaire au XVIIIe siècle. Elles abritent les restes d'environ six millions de Parisiens."),
        "image_path": "image/catacombes.gif"
    },
    "les thermes verts": {
        "nom": "Les Thermes Verts (Clermont-Ferrand)",
        "histoire": ("Vestiges d'une ancienne station thermale réputée, aujourd'hui laissée à l'abandon. Le lieu est célèbre pour son architecture délabrée."),
        "image_path": "image/thermes.gif"
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
    "Hopital psychiatrique de Bargeme": {
        "nom": "Hôpital Psychiatrique de Bargème",
        "histoire": "Un ancien hôpital psychiatrique situé dans le sud de la France, connu pour son architecture imposante et son histoire troublée.",
        "image_path": "image/hopital_psychiatrique.gif"
    },
    "Fort de Cognelot": {
        "nom": "Fort de Cognelot",
        "histoire": "Un fort militaire du XIXe siècle situé en Bourgogne, aujourd'hui abandonné et envahi par la végétation.",
        "image_path": "image/fort_cognelot.gif"
    },
    "Goussainville Vieux-Pays": {
        "nom": "Goussainville Vieux-Pays",
        "histoire": "Un village fantôme près de l'aéroport Charles de Gaulle, abandonné après des nuisances sonores excessives.",
        "image_path": "image/goussainville.gif"
    },
    "Mine Cap Garonne": {
        "nom": "Mine Cap Garonne",
        "histoire": "Une ancienne mine de charbon située dans le sud de la France, aujourd'hui abandonnée et ouverte aux explorateurs urbains.",
        "image_path": "image/mine_cap_garonne.gif"
    },
    "Sucrerie de Francieres": {
        "nom": "Sucrerie de Franières",
        "histoire": "Une ancienne sucrerie située dans le nord de la France, abandonnée après la fermeture de l'industrie sucrière locale.",
        "image_path": "image/sucrerie_francieres.gif"
    },
    "Chateau Pont-Remy": {
        "nom": "Château de Pont-Rémy",
        "histoire": "Un château historique situé en Picardie, aujourd'hui en ruines et entouré de légendes locales.",
        "image_path": "image/chateau_pont_remy.gif"
    },
    "Fort de la Latte": {
        "nom": "Fort de la Latte",
        "histoire": "Un fort médiéval situé en Bretagne, célèbre pour son architecture impressionnante et son histoire militaire.",
        "image_path": "image/fort_de_la_latte.gif"
    },
    "Base Lann-Bihoue": {
        "nom": "Base Aéronavale de Lann-Bihoué",
        "histoire": "Une ancienne base aéronavale en Bretagne, aujourd'hui partiellement abandonnée et utilisée pour des exercices militaires.",
        "image_path": "image/base_lann_bihoue.gif"
    },
    "Ferme fortifiee Montmartin": {
        "nom": "Ferme Fortifiée de Montmartin",
        "histoire": "Une ferme médiévale fortifiée située en Normandie, aujourd'hui abandonnée et envahie par la végétation.",
        "image_path": "image/ferme_fortifiee_montmartin.gif"
    },
    "Ancien Hopital Dreffeac": {
        "nom": "Ancien Hôpital de Dréfféac",
        "histoire": "Un ancien hôpital situé en Bretagne, connu pour son architecture imposante et son histoire médicale.",
        "image_path": "image/ancien_hopital_dreffeac.gif"
    },
    "Chateau Mothe-Chandeniers": {
        "nom": "Château de la Mothe-Chandeniers",
        "histoire": "Un château romantique en ruines situé dans la Vienne, célèbre pour son architecture pittoresque et son histoire fascinante.",
        "image_path": "image/chateau_mothe_chandeniers.gif"
    },
    "Fort Lupin": {
        "nom": "Fort Lupin",
        "histoire": "Un fort côtier situé en Charente-Maritime, construit au XIXe siècle pour défendre la côte atlantique.",
        "image_path": "image/fort_lupin.gif"
    },
    "Ancienne Gare Luxe": {
        "nom": "Ancienne Gare de Luxe",
        "histoire": "Une gare désaffectée située en Nouvelle-Aquitaine, autrefois un point névralgique du transport ferroviaire régional.",
        "image_path": "image/ancienne_gare_luxe.gif"
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
            fltk.rectangle(largeur - 50, 50, largeur, 0, tag=HISTOIRE_TAG, epaisseur=3)
            fltk.ligne(largeur - 45, 45, largeur - 5, 5, tag=HISTOIRE_TAG, epaisseur=2, couleur="red")
            fltk.ligne(largeur - 5, 45, largeur - 45, 5, tag=HISTOIRE_TAG, epaisseur=2, couleur="red")


            y_current += 25 # Espacement vertical