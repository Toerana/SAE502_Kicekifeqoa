import requests
import dns.resolver
import re
import bcrypt
from Python.CRUD.Users.Read_User import get_users

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

def update_user(id_user, email=None, password=None,):
    """
    Met à jour un utilisateur en utilisant l'API.

    Paramètres:
    - id_user (int) : ID de l'utilisateur.
    - email (str) : nouvel email.
    - password (str) : nouveau mot de passe.

    Retourne:
    - Message de succès ou d'erreur.
    """
    if password and email:
        # Validation des champs
        validity_test =[
        is_valid_email(email),
        verfication_doublon_email(email),
        compliance_password(password)
        ]
        for test in validity_test:
            if test[0] == False:
                return test
    elif email: #Vérification format et validité mail
        validity_test =[
        is_valid_email(email),
        verfication_doublon_email(email),
        ]
        for test in validity_test:
            if test[0] == False:
                return test
    elif password: #Verification de la sécurité du mot de passe
        test = compliance_password(password)
        if test[0] == False:
            return test
    elif (password and email) == None:
        # Erreur si aucun arguments n'est entrée
        return [False, "No update data"]

    # Construire les données pour la requête POST
    post_data = {
        'table': 'Users',
        'action': 'update',
        'data': {},
        'column': "id_user",
        'value': id_user
    }
    if email:
        post_data['data']['email'] = email
    if password:
        hashed_password = hash_password(password)
        hashed_password_str = hashed_password.decode("utf-8")  # transforme le format bytes en str
        post_data['data']['password'] = hashed_password_str

    # Envoyer la requête POST à l'API
    try:
        print(post_data)
        response = requests.post(url, json=post_data)
        if response.status_code == 200:
            return [True, 'User OK']
        else:
            return [False,f"Erreur lors de la mise à jour : {response.status_code} - {response.text}"]
    except requests.RequestException as e:
        return [False,f"Erreur de connexion à l'API : {e}"]
