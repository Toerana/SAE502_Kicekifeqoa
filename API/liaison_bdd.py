"""
Module permettant d'interagir avec une API PHP pour gérer des données dans une base de données.

Ce module propose plusieurs fonctions permettant de récupérer, ajouter, mettre à jour, supprimer et compter des données dans une base de données via une API PHP exposée à l'URL suivante :
https://kicekifeqoa.alwaysdata.net/api.php.

Les fonctions permettent de :
- Récupérer des données (avec ou sans filtres et jointures).
- Ajouter de nouvelles données dans une table.
- Mettre à jour des données existantes.
- Supprimer des données d'une table.
- Compter les occurrences d'une valeur dans une table.
- Ajouter des données et récupérer l'ID généré pour l'enregistrement ajouté.

Les fonctions utilisent la méthode `requests` pour envoyer des requêtes HTTP à l'API, et chaque opération renvoie des réponses sous forme de données JSON.

Exemples d'utilisation sont fournis pour chaque fonction afin de faciliter l'intégration dans un projet.

Fonctions disponibles :
1. `get_data`: Récupérer des données depuis une table avec des options de filtrage et de jointure.
2. `add_data`: Ajouter des données dans une table.
3. `update_data`: Mettre à jour des données dans une table.
4. `delete_data`: Supprimer des données d'une table.
5. `count_data`: Compter le nombre d'occurrences d'une valeur spécifique dans une table.
6. `add_recup`: Ajouter des données dans une table et récupérer l'ID généré de l'enregistrement ajouté.

Exemples d'utilisation sont également fournis pour démontrer l'utilisation de ces fonctions.
"""

import requests
import json

# URL de ton API PHP
url = "https://kicekifeqoa.alwaysdata.net/api.php"


def get_data(table, columns='*', filter_column=None, filter_value=None, join_table=None, join_condition=None):
    """
    Récupère des données depuis une table de la base de données.

    :param table: Nom de la table à interroger.
    :type table: str
    :param columns: Colonnes à récupérer (par défaut '*').
    :type columns: str
    :param filter_column: Colonne à utiliser pour appliquer un filtre (optionnel).
    :type filter_column: str, optional
    :param filter_value: Valeur à filtrer dans la colonne (optionnel).
    :type filter_value: str, optional
    :param join_table: Table à joindre (optionnel).
    :type join_table: str, optional
    :param join_condition: Condition de jointure (optionnel).
    :type join_condition: str, optional
    :return: Aucune, affiche les données récupérées ou une erreur.
    :rtype: None
    """
    params = {'table': table, 'columns': columns}

    # Ajouter les filtres s'ils sont spécifiés
    if filter_column and filter_value:
        params['filter_column'] = filter_column
        params['filter_value'] = filter_value

    # Ajouter la jointure si elle est spécifiée
    if join_table and join_condition:
        params['join_table'] = join_table
        params['join_condition'] = join_condition

    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Données récupérées :")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Erreur : {response.status_code} - {response.text}")

def add_data(table, data):
    """
    Ajoute des données dans une table.

    :param table: Nom de la table dans laquelle insérer les données.
    :type table: str
    :param data: Données à insérer dans la table sous forme de dictionnaire.
    :type data: dict
    :return: Aucune, affiche la réponse JSON.
    :rtype: None
    """
    post_data = {
        'table': table,
        'action': 'insert',
        'data': data
    }
    response = requests.post(url, json=post_data)
    print(response.json())

def update_data(table, data, column, value):
    """
    Met à jour des données dans une table.

    :param table: Nom de la table dans laquelle mettre à jour les données.
    :type table: str
    :param data: Dictionnaire contenant les nouvelles valeurs à appliquer.
    :type data: dict
    :param column: Colonne à utiliser pour rechercher la ligne à mettre à jour.
    :type column: str
    :param value: Valeur à rechercher dans la colonne spécifiée.
    :type value: str
    :return: Aucune, affiche la réponse JSON.
    :rtype: None
    """
    post_data = {
        'table': table,
        'action': 'update',
        'data': data,
        'column': column,
        'value': value
    }
    response = requests.post(url, json=post_data)
    print(response.json())

def delete_data(table, column, value):
    """
    Supprime des données d'une table en fonction d'une colonne et d'une valeur spécifiée.

    :param table: Nom de la table où supprimer les données.
    :type table: str
    :param column: Colonne à utiliser pour rechercher la ligne à supprimer.
    :type column: str
    :param value: Valeur à rechercher dans la colonne spécifiée pour supprimer la ligne.
    :type value: str
    :return: Aucune, affiche la réponse JSON.
    :rtype: None
    """
    post_data = {
        'table': table,
        'column': column,
        'value': value
    }
    response = requests.delete(url, json=post_data)
    print(response.json())

def count_data(table, filter_column, filter_value):
    """
    Compte le nombre d'occurrences de données dans une table avec un filtre spécifique.

    :param table: Nom de la table où effectuer le comptage.
    :type table: str
    :param filter_column: Colonne à utiliser pour appliquer un filtre.
    :type filter_column: str
    :param filter_value: Valeur à filtrer dans la colonne spécifiée.
    :type filter_value: str
    :return: Aucune, affiche le nombre d'occurrences.
    :rtype: None
    """
    params = {
        'table': table,
        'filter_column': filter_column,
        'filter_value': filter_value
    }
    response = requests.request("COUNT", url, params=params)
    if response.status_code == 200:
        print("Nombre d'occurrences :")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Erreur : {response.status_code} - {response.text}")

def add_recup(data):
    """
    Ajoute des données dans une table et récupère l'ID généré.

    :param data: Un dictionnaire avec le nom de la table comme clé
                 et un autre dictionnaire contenant les colonnes/valeurs à insérer.
    :type data: dict
    :return: ID généré de l'élément inséré, ou None en cas d'erreur.
    :rtype: int or None
    :example:
        data = {"Users": {"name": "John Doe", "email": "john.doe@example.com"}}
    """
    post_data = {
        'table': list(data.keys())[0],  # Récupère le nom de la table (clé du dictionnaire)
        'action': 'add_recup',  # Action à effectuer : ajouter et récupérer l'ID
        'data': list(data.values())[0]  # Récupère les données associées à la table
    }

    response = requests.post(url, json=post_data)
    if response.status_code == 200:
        result = response.json()
        print("Données ajoutées avec succès.")
        return result.get('id')
    else:
        print(f"Erreur : {response.status_code} - {response.text}")
        return None

# Exemples d'utilisation
"""
Exemples d'utilisation des fonctions de l'API.

Ces exemples montrent comment interagir avec l'API pour récupérer, ajouter, mettre à jour, supprimer des données et compter les occurrences dans une base de données.

1. Récupérer toutes les colonnes d'une table
   Récupère toutes les colonnes d'une table spécifique.

   Exemple :
       get_data("Group")

2. Récupérer des colonnes spécifiques
   Récupère une ou plusieurs colonnes spécifiques d'une table.

   Exemple :
       get_data("Users", "email")

3. Récupérer des colonnes spécifiques avec un filtre sur une valeur
   Récupère des colonnes spécifiques avec un filtre sur une valeur donnée dans une colonne.

   Exemple :
       get_data("Task", filter_column="checked", filter_value="1")

4. Récupérer toutes les informations liées à une valeur spécifique
   Récupère toutes les informations liées à une valeur spécifique dans une colonne donnée.

   Exemple :
       get_data("Users", "*", filter_column="id_user", filter_value="1")

5. Récupérer des données avec une jointure
   Effectue une jointure entre plusieurs tables et récupère des données liées à une condition spécifique.

   Exemple :
       get_data("Task_has_Users", "Task.name,Users.email", 
                 join_table="Task,Users", 
                 join_condition="Task_has_Users.task_id = Task.id_task,Task_has_Users.user_id = Users.id_user", 
                 filter_column="Users.id_user", filter_value="1")

6. Ajouter des données dans une table
   Ajoute de nouvelles données dans une table spécifiée.

   Exemple :
       add_data("test", {"alpha": "tic", "beta": "fax"})

7. Mettre à jour des données dans une table
   Met à jour des données existantes dans une table en fonction d'une colonne et d'une valeur spécifiques.

   Exemple :
       update_data("test", {"beta": "test"}, "beta", "fax")

8. Supprimer des données
   Supprime des données d'une table en fonction d'une colonne et d'une valeur spécifiques.

   Exemple :
       delete_data("test", "beta", "fax")

9. Compter les occurrences dans une table
   Compte le nombre d'occurrences d'une valeur donnée dans une colonne spécifique d'une table.

   Exemple :
       count_data("Group", "name", "ouioui")

10. Ajouter des données et récupérer l'ID généré
    Ajoute des données dans une table et récupère l'ID généré pour l'enregistrement ajouté.

    Exemple :
        data = {"Task": {"name": "Test", "end_date": "2024/13/22"}}
        generated_id = add_recup(data)
        print(f"ID généré : {generated_id}")
        # L'ID est maintenant dans la variable generated_id
"""


