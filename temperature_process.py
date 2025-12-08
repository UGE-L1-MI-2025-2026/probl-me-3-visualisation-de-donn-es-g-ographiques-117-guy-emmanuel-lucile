import json
import csv


def charger_temperatures_csv(fichier, date):
    """
    Charge les températures pour une date donnée depuis CSV

    Format CSV attendu:
    date,departement,temperature_moy
    2018-07-01,75,26.5
    2018-07-01,77,27.2
    """
    temperatures_jour = {}

    with open(fichier, 'r', encoding='utf-8') as f:
        # Sauter l'en-tête
        premiere_ligne = f.readline()

        # Lire chaque ligne
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue

            # Séparer par virgule
            parties = ligne.split(',')

            if len(parties) >= 3:
                date_csv = parties[0]
                dep_code = parties[1]
                temp = float(parties[2])

                if date_csv == date:
                    temperatures_jour[dep_code] = temp

    return temperatures_jour


def obtenir_dates_disponibles_csv(fichier):
    """
    Retourne la liste des dates disponibles dans le fichier CSV
    """
    dates = set()

    with open(fichier, 'r', encoding='utf-8') as f:
        # Sauter l'en-tête
        premiere_ligne = f.readline()

        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue

            parties = ligne.split(',')
            if len(parties) >= 1:
                dates.add(parties[0])

    return sorted(list(dates))


def charger_temperatures_json(fichier, date):
    """
    Charge les températures pour une date donnée depuis JSON
    """

    with open(fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)

    temperatures_jour = {}

    for entry in data['temperatures']:
        if entry['date'] == date:
            dep_code = entry['departement']

            temp = entry['temperature_moy']

            temperatures_jour[dep_code] = temp

    return temperatures_jour


def obtenir_dates_disponibles_json(fichier):
    """
    Retourne la liste des dates disponibles dans le fichier JSON
    """

    with open(fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)

    dates = set()

    for entry in data['temperatures']:
        dates.add(entry['date'])

    return sorted(list(dates))

def charger_temperatures(fichier, date):
    """
    Charge les températures automatiquement (détecte JSON ou CSV)
    """
    if fichier.endswith('.json'):
        return charger_temperatures_json(fichier, date)
    elif fichier.endswith('.csv'):
        return charger_temperatures_csv(fichier, date)
    else:
        raise TypeError("ERROR: Format de fichier non supporté. Utilisez .json ou .csv")

def obtenir_dates_disponibles(fichier):
    """
    Retourne les dates disponibles (détecte JSON ou CSV)
    """
    if fichier.endswith('.json'):
        return obtenir_dates_disponibles_json(fichier)
    elif fichier.endswith('.csv'):
        return obtenir_dates_disponibles_csv(fichier)
    else:
        raise TypeError("ERROR: Format de fichier non supporté. Utilisez .json ou .csv")


def obtenir_couleur_temperature(temp):
    """
    Retourne un code couleur hexadécimal selon la température en Celcius
    """
    # Échelle de couleurs: bleu (froid) -> rouge (chaud)
    if temp < 0:
        return "#0000ff"  # Bleu foncé
    elif temp < 10:
        return "#4169e1"  # Bleu
    elif temp < 15:
        return "#87ceeb"  # Bleu clair
    elif temp < 20:
        return "#90ee90"  # Vert clair
    elif temp < 25:
        return "#ffff00"  # Jaune
    elif temp < 30:
        return "#ffa500"  # Orange
    else:
        return "#ff0000"  # Rouge



def creer_legende_temperatures():
    """
    Retourne les informations pour dessiner une légende des températures
    """
    legende = [
        {"temperature": "< 0°C", "couleur": "#0000ff"},
        {"temperature": "0-10°C", "couleur": "#4169e1"},
        {"temperature": "10-15°C", "couleur": "#87ceeb"},
        {"temperature": "15-20°C", "couleur": "#90ee90"},
        {"temperature": "20-25°C", "couleur": "#ffff00"},
        {"temperature": "25-30°C", "couleur": "#ffa500"},
        {"temperature": "> 30°C", "couleur": "#ff0000"}
    ]
    return legende


# ============ EXEMPLE D'UTILISATION ============

if __name__ == "__main__":

    # Créer un fichier de test
    exemple_data = {
        "temperatures": [
            {"date": "2018-07-01", "departement": "75", "temperature_moy": 26.5},
            {"date": "2018-07-01", "departement": "77", "temperature_moy": 27.2},
            {"date": "2018-07-01", "departement": "01", "temperature_moy": 24.8},
            {"date": "2018-07-02", "departement": "75", "temperature_moy": 27.1},
            {"date": "2018-07-02", "departement": "77", "temperature_moy": 27.8}
        ]
    }

    # Sauvegarder l'exemple
    with open('exemple_temperatures.json', 'w', encoding='utf-8') as f:
        json.dump(exemple_data, f, indent=2, ensure_ascii=False)

    # Test 1: Chargement
    print("Test 1: Chargement des températures")
    temps = charger_temperatures_json('exemple_temperatures.json', '2018-07-01')
    print(f"Températures pour le 2018-07-01:")
    for dep, temp in temps.items():
        print(f"  Département {dep}: {temp}°C")

    # Test 2: Couleurs
    print("\nTest 2: Couleurs par température")
    for temp in [-5, 5, 15, 25, 35]:
        couleur = obtenir_couleur_temperature(temp)
        print(f"  {temp}°C -> {couleur}")

    # Test 3: Dates disponibles
    print("\nTest 3: Dates disponibles")
    dates = obtenir_dates_disponibles('exemple_temperatures.json')
    print(f"  Dates: {dates}")

    # Test 4: Légende
    print("\nTest 4: Légende")
    legende = creer_legende_temperatures()
    for elem in legende:
        print(f"  {elem['temperature']}: {elem['couleur']}")