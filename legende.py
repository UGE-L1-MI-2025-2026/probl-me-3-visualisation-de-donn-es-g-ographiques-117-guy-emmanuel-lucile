# legend_right.py
from fltk import cree_fenetre, cercle, texte, mise_a_jour, attend_fermeture

def dessiner_legende():
    largeur_fenetre = 800   # largeur totale de la fenêtre
    hauteur_fenetre = 600   # hauteur totale de la fenêtre
    largeur_legende = 200   # largeur réservée pour la légende à droite

    cree_fenetre(largeur_fenetre, hauteur_fenetre, redimension=False)

    # Position de départ pour la légende
    x_legende = largeur_fenetre - largeur_legende + 30  # un peu d'espace depuis le bord droit
    y_depart = 50
    espacement = 50

    # Éléments de la légende
    elements = [
        {"nom": "Hôpitaux", "couleur": "green"},
        {"nom": "Écoles", "couleur": "blue"},
        {"nom": "Parcs", "couleur": "red"},
        {"nom": "Maisons", "couleur": "orange"}
    ]

    for i, elem in enumerate(elements):
        y = y_depart + i * espacement
        cercle(x_legende, y, 15, couleur=elem["couleur"], remplissage=elem["couleur"])
        texte(x_legende + 40, y, elem["nom"], taille=15)

    mise_a_jour()
    attend_fermeture()

if __name__ == "__main__":
    dessiner_legende()
