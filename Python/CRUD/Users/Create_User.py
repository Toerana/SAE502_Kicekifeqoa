import re
import dns.resolver
import requests
from Python.CRUD.Users.Read_User import get_users
import bcrypt

url = "https://kicekifeqoa.alwaysdata.net/api.php"


def verfication_doublon_email(E_mail):
    # Requête BDD pour vérifier l'existence de l'email
    result = get_users(email=E_mail)

    # Si le résultat est 'no existing links', l'email n'existe pas
    if result == 'no existing links':
        return [True,'Mail OK']  # L'email n'existe pas, donc il est disponible
    else:
        return [False,"Mail Exist"]  # L'email existe déjà

def compliance_password(Password) :
    if len(Password) < 8:
        return [False, "Pass <8"]
    if len(Password) > 72:
        #limitation de bcrypt a 72 octet
        return [False, "Pass >72"]
    if not re.search(r"[A-Z]", Password):
        return [False, "Pass Uppercase"]
    if not re.search(r"[a-z]", Password):
        return [False, "Pass Lowercase"]
    if not re.search(r"[0-9]", Password):
        return [False, "Pass Number"]
    if not re.search(r"[!@#$%^&*(),.?{}|<>]", Password):
        return [False, "Pass Special"]
    return [True,'Pass OK']


def is_valid_email(email):
    # Vérification du format de l'email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(regex, email):
        return [False, "Mail NOK"]

    # Vérification de l'existence du domaine
    domain = email.split('@')[-1]
    try:
        # Vérifier les enregistrements MX du domaine
        dns.resolver.resolve(domain, 'MX')
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return [False, "Mail NOK"]
    return [True, "Mail OK"]

def hash_password(password):
    # Génére un salt et hash le mot de passe
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def create_user (E_mail,Password):
    """
    Crée un nouvel utilisateur après vérification des critères de validité.

    Args:
        email (str): Adresse email de l'utilisateur.
        password (str): Mot de passe de l'utilisateur.
        url (str): URL de l'API pour l'insertion de données.

    Returns:
        list: [bool, str] - Indique si l'opération a réussi et un message de confirmation ou d'erreur.
    """
    validity_test =[
    is_valid_email(E_mail),
    verfication_doublon_email(E_mail),
    compliance_password(Password)
    ]
    for test in validity_test:
        if test[0] == False:
            return test
    hashed_password = hash_password(Password)
    hashed_password_str = hashed_password.decode("utf-8") # transforme le format bytes en str
    data =  {
            "email": E_mail,
            "password": hashed_password_str,
    }
    post_data = {
        'table': 'Users',
        'action': 'insert',
        'data': data
    }
    try:
        response = requests.post(url, json=post_data)
        response.raise_for_status()  # Vérifie si la requête a réussi
    except requests.exceptions.RequestException as e:
        return [False, f"Erreur lors de l'envoi de la requête : {e}"]

    return [True, 'User OK']


