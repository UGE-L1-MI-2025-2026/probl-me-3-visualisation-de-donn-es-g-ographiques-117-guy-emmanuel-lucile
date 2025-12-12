import csv

COLOR_MAP = [
    (0,   "#0000ff"),   
    (5,   "#4169e1"),   
    (10,  "#87ceeb"),   
    (15,  "#90ee90"),   
    (20,  "#ffff00"),   
    (25,  "#ffa500"),   
    (30,  "#ff6347"),   
    (float('inf'), "#ff0000"), # Le cas 'else'
]

def get_couleur(temp):
    """
    Retourne la couleur de manière compacte en utilisant next().
    """
    if temp is None:
        return "#cccccc"

    # Cherche la couleur (c) pour la première paire (t, c) où temp < t est vrai.
    # Le second argument de next est la valeur par défaut si la recherche échoue (sécurité).
    return next((c for t, c in COLOR_MAP if temp < t), "#ff0000")

def charger_temperatures(fichier_csv, date):
    """
    Charge les températures pour une date donnée depuis le fichier CSV
    """
    temperatures = {}

    # Ouvrir le fichier CSV
    with open(fichier_csv, 'r', encoding='utf-8-sig') as f:
        # Lire le CSV avec DictReader (utilise la première ligne comme noms de colonnes)
        lecteur = csv.DictReader(f, delimiter=';')

        # Parcourir chaque ligne du CSV
        for ligne in lecteur:
            date_csv = ligne['Date']
            code_dep = ligne['Code INSEE département']

            # Normaliser le code département: enlever les zéros devant
            # '01' -> '1', '02' -> '2', etc.
            if code_dep.isdigit():
                code_dep = str(int(code_dep))

            # Si c'est la bonne date, on récupère la température
            if date_csv == date:
                try:
                    temp = float(ligne['TMoy (°C)'])
                    temperatures[code_dep] = temp
                except (ValueError, KeyError):
                    # Si on n'arrive pas à lire la température, on continue
                    continue

    return temperatures

def charger_temperatures_max(fichier_csv, date):
    """
    Charge les températures pour une date donnée depuis le fichier CSV
    """
    temperatures = {}

    # Ouvrir le fichier CSV
    with open(fichier_csv, 'r', encoding='utf-8-sig') as f:
        # Lire le CSV avec DictReader (utilise la première ligne comme noms de colonnes)
        lecteur = csv.DictReader(f, delimiter=';')

        # Parcourir chaque ligne du CSV
        for ligne in lecteur:
            date_csv = ligne['Date']
            code_dep = ligne['Code INSEE département']

            # Normaliser le code département: enlever les zéros devant
            # '01' -> '1', '02' -> '2', etc.
            if code_dep.isdigit():
                code_dep = str(int(code_dep))

            # Si c'est la bonne date, on récupère la température
            if date_csv == date:
                try:
                    temp = float(ligne['TMoy (°C)'])
                    temperatures[code_dep] = temp
                except (ValueError, KeyError):
                    # Si on n'arrive pas à lire la température, on continue
                    continue

    return temperatures

def coloriage(lst_temp:dict):
    col = {}

    for dep,temp in lst_temp.items():
        col[dep] =get_couleur(temp)
    
    return col





