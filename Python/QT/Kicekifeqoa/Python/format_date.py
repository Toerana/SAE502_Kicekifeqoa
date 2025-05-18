from datetime import datetime  # Importation de la classe `datetime` du module `datetime` pour manipuler les dates.

# Fonction pour valider le format d'une date et la convertir au format requis.
def validate_date_format(date_str):
    try:
        # Tente de convertir la chaîne `date_str` du format "jj/mm/aaaa" au format "aaaa-mm-jj 00:00:00"
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d 00:00:00")
    except ValueError:
        # En cas d'erreur de format, lève une exception avec un message expliquant le format attendu
        raise ValueError(f"Format de date invalide : {date_str}. Utilisez le format jj/mm/aaaa.")

# Fonction pour vérifier la cohérence des dates
def check_dates_consistency(end_date):
    # Convertit la date de fin `end_date` au format `datetime` attendu "%Y-%m-%d 00:00:00"
    end = datetime.strptime(end_date, "%Y-%m-%d 00:00:00")


# Fonction pour lire une date au format "aaaa-mm-jj hh:mm:ss" et la convertir en "jj/mm/aaaa"
def read_date_format(date_str):
    try:
        # Tente de convertir `date_str` du format "aaaa-mm-jj hh:mm:ss" au format "jj/mm/aaaa"
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
    except ValueError:
        # En cas d'erreur de format, affiche un message d'erreur et retourne la chaîne initiale
        print(f"Erreur de format de date pour {date_str}")
        return date_str
