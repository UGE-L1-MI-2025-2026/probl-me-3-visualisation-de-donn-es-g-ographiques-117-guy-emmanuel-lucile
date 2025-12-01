# description_lieu.py
from fltk import cree_fenetre, texte, mise_a_jour, attend_fermeture

def afficher_description(titre, description):
    largeur, hauteur = 400, 200
    cree_fenetre(largeur, hauteur, redimension=False)
    texte(20, 30, titre, taille=16)
    texte(20, 70, description, taille=12)
    mise_a_jour()
    attend_fermeture()
