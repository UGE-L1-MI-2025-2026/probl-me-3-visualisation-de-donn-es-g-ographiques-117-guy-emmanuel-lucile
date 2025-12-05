import json
import math


# ============ LECTURE DES LIEUX ============

def charger_lieux_depuis_json(fichier):
    """
    Charge les lieux depuis un fichier JSON
    Retourne une liste de lieux
    """
    with open(fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Si le JSON a une cle "lieux"
    if 'lieux' in data:
        return data['lieux']

    # Sinon retourne data directement (si c'est deja une liste)
    return data


def sauvegarder_lieux_en_json(lieux, fichier):
    """
    Sauvegarde la liste des lieux dans un fichier JSON
    """
    data = {'lieux': lieux}
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def charger_lieux_depuis_csv(fichier):
    """
    Charge les lieux depuis un fichier CSV
    Format: nom,longitude,latitude,couleur,description
    """
    lieux = []

    with open(fichier, 'r', encoding='utf-8') as f:
        # Sauter l'en-tete
        premiere_ligne = f.readline()

        # Lire chaque ligne
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue

            # Separer par virgule
            parties = ligne.split(',')

            if len(parties) >= 4:
                nom = parties[0]
                longitude = float(parties[1])
                latitude = float(parties[2])
                couleur = parties[3]
                description = parties[4] if len(parties) > 4 else ""

                lieu = {
                    'nom': nom,
                    'pos': (longitude, latitude),
                    'couleur': couleur,
                    'description': description
                }
                lieux.append(lieu)

    return lieux


def sauvegarder_lieux_en_csv(lieux, fichier):
    """
    Sauvegarde les lieux dans un fichier CSV
    """
    with open(fichier, 'w', encoding='utf-8') as f:
        # En-tete
        f.write("nom,longitude,latitude,couleur,description\n")

        # Chaque lieu
        for lieu in lieux:
            lon, lat = lieu['pos']
            desc = lieu.get('description', '').replace(',', ';')
            ligne = f"{lieu['nom']},{lon},{lat},{lieu['couleur']},{desc}\n"
            f.write(ligne)


# ============ GESTION DES LIEUX ============

def ajouter_lieu(liste_lieux, nom, latitude, longitude, couleur, description=""):
    """
    Ajoute un nouveau lieu abandonne a la liste
    """
    nouveau_lieu = {
        'nom': nom,
        'pos': (longitude, latitude),
        'couleur': couleur,
        'description': description
    }
    liste_lieux.append(nouveau_lieu)
    return liste_lieux


def filtrer_par_couleur(liste_lieux, couleur):
    """
    Filtre les lieux par couleur (type de lieu)
    """
    resultat = []
    for lieu in liste_lieux:
        if lieu['couleur'] == couleur:
            resultat.append(lieu)
    return resultat


def filtrer_par_zone(liste_lieux, lon_min, lat_min, lon_max, lat_max):
    """
    Filtre les lieux dans une zone geographique
    """
    resultat = []
    for lieu in liste_lieux:
        lon, lat = lieu['pos']
        if lon_min <= lon <= lon_max and lat_min <= lat <= lat_max:
            resultat.append(lieu)
    return resultat


# ============ CALCULS POUR VISUALISATION ============

def calculer_rayon_cercle(valeur, valeur_max, rayon_max=20):
    """
    Calcule le rayon d'un cercle pour la visualisation
    L'aire du cercle est proportionnelle a la valeur
    """
    if valeur <= 0 or valeur_max <= 0:
        return 0

    rapport = valeur / valeur_max
    rayon = math.sqrt(rapport) * rayon_max
    return rayon


def obtenir_couleur_type_lieu(type_lieu):
    """
    Retourne la couleur selon le type de lieu abandonne
    """
    couleurs = {
        'hopital': 'green',
        'ecole': 'blue',
        'bunker': 'gray',
        'catacombes': 'black',
        'sanatorium': 'darkred',
        'cimetiere': 'purple',
        'station': 'darkred'
    }

    type_lower = type_lieu.lower()
    for cle in couleurs:
        if cle in type_lower:
            return couleurs[cle]

    return 'orange'


def compter_lieux_par_type(liste_lieux):
    """
    Compte le nombre de lieux par couleur (type)
    Retourne un dictionnaire {couleur: nombre}
    """
    compteur = {}
    for lieu in liste_lieux:
        couleur = lieu['couleur']
        if couleur in compteur:
            compteur[couleur] = compteur[couleur] + 1
        else:
            compteur[couleur] = 1

    return compteur


# ============ RECHERCHE ============

def chercher_lieu_par_nom(liste_lieux, nom):
    """
    Cherche un lieu par son nom
    Retourne le premier lieu trouve ou None
    """
    for lieu in liste_lieux:
        if nom.lower() in lieu['nom'].lower():
            return lieu
    return None


def trouver_lieu_proche(liste_lieux, lon, lat, distance_max=0.1):
    """
    Trouve les lieux proches d'un point
    distance_max en degres (environ 0.1 degre = 11 km)
    """
    proches = []
    for lieu in liste_lieux:
        lieu_lon, lieu_lat = lieu['pos']

        # Calcul simple de distance
        dist = math.sqrt((lon - lieu_lon)**2 + (lat - lieu_lat)**2)

        if dist <= distance_max:
            proches.append(lieu)

    return proches


def trouver_lieu_au_clic(liste_lieux, x_clic, y_clic, positions_pixels, tolerance=15):
    """
    Trouve le lieu clique sur la carte

    positions_pixels: dict {nom_lieu: (x_pixel, y_pixel)}
    tolerance: distance en pixels pour considerer un clic
    """
    for lieu in liste_lieux:
        nom = lieu['nom']
        if nom in positions_pixels:
            x_lieu, y_lieu = positions_pixels[nom]

            # Distance euclidienne
            dist = math.sqrt((x_clic - x_lieu)**2 + (y_clic - y_lieu)**2)

            if dist <= tolerance:
                return lieu

    return None


# ============ STATISTIQUES ============

def obtenir_statistiques(liste_lieux):
    """
    Retourne des statistiques sur les lieux
    """
    if not liste_lieux:
        return {
            'total': 0,
            'par_type': {},
            'annee_plus_ancienne': None,
            'annee_plus_recente': None
        }

    stats = {
        'total': len(liste_lieux),
        'par_type': compter_lieux_par_type(liste_lieux)
    }

    # Chercher les annees d'abandon
    annees = []
    for lieu in liste_lieux:
        if 'annee_abandon' in lieu:
            annees.append(lieu['annee_abandon'])

    if annees:
        stats['annee_plus_ancienne'] = min(annees)
        stats['annee_plus_recente'] = max(annees)
    else:
        stats['annee_plus_ancienne'] = None
        stats['annee_plus_recente'] = None

    return stats


# ============ EXEMPLE D'UTILISATION ============

if __name__ == "__main__":
    print("=== Module de traitement des donnees - Lieux abandonnes ===\n")

    # Test: charger depuis JSON
    try:
        lieux = charger_lieux_depuis_json('exemple.json')
        print(f"Charge {len(lieux)} lieux depuis JSON")

        # Afficher quelques infos
        for lieu in lieux[:3]:
            lon, lat = lieu['pos']
            print(f"  - {lieu['nom']} ({lat:.4f}, {lon:.4f}) - {lieu['couleur']}")

        # Statistiques
        stats = obtenir_statistiques(lieux)
        print(f"\nStatistiques:")
        print(f"  Total: {stats['total']}")
        print(f"  Par type: {stats['par_type']}")
        if stats['annee_plus_ancienne']:
            print(f"  Periode: {stats['annee_plus_ancienne']} - {stats['annee_plus_recente']}")

        # Test filtre par couleur
        hopitaux = filtrer_par_couleur(lieux, 'green')
        print(f"\nHopitaux abandonnes: {len(hopitaux)}")

    except FileNotFoundError:
        print("Fichier exemple.json non trouve")
        print("Creez-le d'abord ou utilisez un autre fichier")
