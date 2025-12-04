import fltk as af
from dataclasses import dataclass
import time


class _interaction:
    def __init__(self):
        self._ev = None
        self._action = None

    def update(self):
        self._ev = af.donne_ev()
        
    def type_action(self):
        self.update()
        self._action = af.type_ev(self._ev)
    
    @property
    def action(self):
        self.type_action()
        return self._action

    def clique_gauche(self):
        """ on verra aprés"""
        if self.action == "ClicGauche":
            x, y = af.abscisse(self._ev), af.ordonnee(self._ev)
            print(f"Clic gauche en ({x},{y})")
    def touche(self):
        if self.action == "Touche":
            match af.touche(self._ev):
                case "z":
                    pass
                case "s":
                    pass
                case "q":
                    pass
                case "d":
                    pass
                


    def quit(self):
        """
        detecte juste quand quitter
        """
        return self.action == 'Quitte'




def interaction():



    return
        
lst = [(x,y) for x,y in zip(list(range(100)),list(range(100)))]



def zoom_centre(
    liste_point, 
    scal: float, 
    centre_pivot: tuple[float, float] = (0.0, 0.0) #va etre la position de la souris sur ecran
):
    """
    Applique un zoom autour d'un point pivot (x_c, y_c).
    """
    x_c, y_c = centre_pivot
    
    for x, y in liste_point:
        # 1. Translation vers l'origine
        x_trans = x - x_c
        y_trans = y - y_c
        
        # 2. Mise à l'échelle (Zoom)
        x_zoom = x_trans * scal
        y_zoom = y_trans * scal
        
        # 3. Retour à la position (Translation inverse)
        x_final = x_zoom + x_c
        y_final = y_zoom + y_c
        
        yield (x_final, y_final)

p = zoom_centre(lst,0.5)




def animation():
    """
    les carte qui evoue avec le temp
    Docstring for animation
    juste a changer l'image precedente avec l'ancienne
    """



    return




"""
last = 0
#test
af.cree_fenetre(800,600)
b = _interaction()
while True:
    now =time.time()
    b.clique_gauche()
    
    af.mise_a_jour()

    if b.quit():
        break
    deltatime =  now- last
    last = now

        
af.ferme_fenetre()
"""