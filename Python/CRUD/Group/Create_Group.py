import mysql.connector
from mysql.connector import (connection)
from mysql.connector import Error
from datetime import datetime
import json
import requests

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

def verification_doublon_group(name_Group, cursor):
    # Vérifier le type et afficher l'argument pour le débogage
    # Requête SQL pour vérifier l'existence du groupe
    query = "SELECT COUNT(*) FROM `Group` WHERE name = %s"
    try:
        # Exécution de la requête avec un tuple
        cursor.execute(query, (name_Group,))  # (name_Group,) pour passer en tant que tuple
        # Récupérer le résultat
        result = cursor.fetchone()
        # Vérifier si le résultat est valide
        if result is not None and result[0] is not None:
            # Si le résultat est 0, le name_Group n'existe pas
            if result[0] == 0:
                return True  # Le name_Group n'existe pas, donc il est disponible
            else:
                print("Le groupe existe déjà.")
                return False  # Le name_Group existe déjà
        else:
            print("Aucun résultat trouvé.")
            return True  # Le groupe n'existe pas
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'exécution de la requête : {err}")
        return None  # Indiquer qu'il y a eu une erreur

def create_group(name, table, data):
    try:
        if verification_doublon_group(name,cursor):
            post_data = {
                'table': table,
                'action': 'insert',
                'data': data
            }
            response = requests.post(url, json=post_data)
            print(response.json())
            close_connection_BDD(conn, cursor)

    except Error as e:
        print(f"Erreur lors de l'insertion : {e}")

