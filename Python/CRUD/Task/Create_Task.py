from mysql.connector import (connection)
import requests
import json

# URL de ton API PHP
url = "https://kicekifeqoa.alwaysdata.net/api.php"

# Configuration de la connexion
config = {
    'user': '379269_admin',
    'password': 'Kicekifeqoa123*',
    'host': 'mysql-kicekifeqoa.alwaysdata.net',
    'database': 'kicekifeqoa_todolist',
}

# Connexion à la base de donnée
conn = connection.MySQLConnection(**config)
cursor = conn.cursor()

def close_connection_BDD(conn,cursor):
    cursor.close()
    conn.close()

def create_task(table, data):
    try:
        post_data = {
            'table': table,
            'action': 'insert',
            'data': data
        }
        response = requests.post(url, json=post_data)
        close_connection_BDD(conn, cursor)
    except Exception as e:
        print(f"Erreur : {e}")
        return None

def add_recup(data):
    """
    Ajoute des données dans une table et récupère l'ID généré.

    :param data: Un dictionnaire avec le nom de la table comme clé
                 et un autre dictionnaire contenant les colonnes/valeurs à insérer.
    :example:
        data = {"Users": {"name": "John Doe", "email": "john.doe@example.com"}}
    """
    post_data = {
        'table': list(data.keys())[0],  # Récupère le nom de la table (clé du dictionnaire)
        'action': 'add_recup',  # Action à effectuer : ajouter et récupérer l'ID
        'data': list(data.values())[0]  # Récupère les données associées à la table
    }

    response = requests.post(url, json=post_data)
    close_connection_BDD(conn, cursor)
    if response.status_code == 200:
        result = response.json()
        return result.get('id')
    else:
        print(f"Erreur : {response.status_code} - {response.text}")
        return None