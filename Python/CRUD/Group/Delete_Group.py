import mysql.connector
from mysql.connector import (connection)
import requests
import json

# URL de ton API PHP
url = "http://kicekifeqoa.alwaysdata.net/api.php"

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

def delete_group(table, column, value):
    post_data = {
        'table': table,
        'column': column,
        'value': value
    }
    response = requests.delete(url, json=post_data)
    close_connection_BDD(conn, cursor)

