# **Division du projet en trois parties**

## **PARTIE 1 : Traitement des données**
Responsable : *???*

**Responsabilités :**
- Lecture et traitement des fichiers Shapefile
- Parsing des fichiers CSV et JSON
- Conversion entre systèmes de coordonnées (WGS 84 ↔ Mercator)
- Traitement des données netCDF pour l'animation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## **PARTIE 2 : Visualisation statique**
Responsable : *???*

**Responsabilités :**
- Dessin des contours des départements avec `fltk`
- Création des schémas de couleurs et légendes
- Dessin des disques/cercles pour données localisées
- Gestion de la fenêtre et du viewport

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## **PARTIE 3 : Interactivité et animation**
Responsable : *???*

**Responsabilités :**
- Création des cartes animées (évolution temporelle)
- Gestion des événements (souris, clavier)
- Arguments en ligne de commande
- Navigation sur la carte (zoom, déplacement)
- Fichier principal d'intégration

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### **Points d'intégration**
- Partie 1 → Partie 2 : Données structurées pour la visualisation
- Partie 2 → Partie 3 : Fonctions de dessin pour l'animation
- Partie 1 → Partie 3 : Données filtrées par date/temps

### **Minimum requis**
1. Affichage d'au moins un type de carte (départements colorés)
2. Carte animée montrant l'évolution des données dans le temps

**Charge de travail estimée**
- Partie 1: ~40% (много форматов данных)
- Partie 2: ~30% (визуализация statique)
- Partie 3: ~30% (animation + intégration)

**Ordre recommandé**
1. Partie 1 commence en premier (fournit les données)
2. Partie 2 en parallèle après avoir les structures de données
3. Partie 3 commence après avoir les fonctions de base


### ****Bonus****

**1.** Programme paramétrable: 
    
Le programme dispose de plusieurs paramètres en ligne de commande qui permettent de modifier son fonctionnement.
Par exemple, il pourrait être possible de sélectionner :

        - des données différentes dans la même base (par exemple : autres - sports, températures moyennes ou minimum, précipitations, etc.),
        - des bases de données différentes (par exemple : restaurants, stations de train ou de métro, etc.),
        - un département, région, pays ou commune différente,  
        - des paramètres d'affichage (échelle des disques, couleurs, taille du texte, etc.). 

**2.** Interactivité

- Il est possible d'obtenir des informations supplémentaires en survolant ou en cliquant sur les éléments graphiques de la fenêtre.

- Il est également envisageable de déplacer la carte grâce à des touches du clavier, de zoomer ou dézoomer, etc.

- Enfin, dans le cas des données climatiques par exemple, on peut envisager de passer d'une date à une autre grâce aux flèches (en ajoutant 1 jour ou 1 an à la date courante par exemple), ou pourquoi pas de créer une animation pour tenter de visualiser l'évolution du climat en France sur une période plus longue.

**3.** Autre format
- autre format de données géographiques: GeoJSON