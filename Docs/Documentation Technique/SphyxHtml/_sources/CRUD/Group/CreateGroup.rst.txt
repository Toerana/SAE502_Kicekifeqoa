Create Group
========================

Ce module permet de gérer la création de groupes dans une base de données MySQL via une API PHP. Il inclut des fonctions pour vérifier l'existence de doublons avant l'insertion et pour fermer proprement les connexions à la base de données.

Fonctions
---------

.. function:: close_connection_BDD(conn, cursor)

   Ferme proprement la connexion à la base de données.

   :param conn: L'objet de connexion MySQL.
   :type conn: mysql.connector.connection.MySQLConnection
   :param cursor: L'objet curseur associé à la connexion.
   :type cursor: mysql.connector.cursor.MySQLCursor

   **Exemple d'utilisation :**

   .. code-block:: python

      close_connection_BDD(conn, cursor)

.. function:: verification_doublon_group(name_Group, cursor)

   Vérifie si un groupe portant le nom spécifié existe déjà dans la base de données.

   :param name_Group: Le nom du groupe à vérifier.
   :type name_Group: str
   :param cursor: L'objet curseur pour exécuter la requête SQL.
   :type cursor: mysql.connector.cursor.MySQLCursor

   :return: Retourne ``True`` si le groupe n'existe pas (pas de doublon), ``False`` si le groupe existe déjà, et ``None`` en cas d'erreur.
   :rtype: bool ou None

   **Exemple d'utilisation :**

   .. code-block:: python

      if verification_doublon_group("GroupName", cursor):
          print("Le groupe est disponible.")
      else:
          print("Le groupe existe déjà.")

.. function:: create_group(name, table, data)

   Crée un nouveau groupe dans la base de données via une requête POST envoyée à une API PHP, après avoir vérifié qu'il n'existe pas déjà.

   :param name: Le nom du groupe à créer.
   :type name: str
   :param table: Le nom de la table dans laquelle insérer le groupe.
   :type table: str
   :param data: Les données du groupe sous forme de dictionnaire.
   :type data: dict

   Cette fonction envoie une requête POST à l'API et ferme ensuite la connexion à la base de données.

   **Exemple d'utilisation :**

   .. code-block:: python

      data = {
          'name': 'Nouveau Groupe',
          'description': 'Description du groupe'
      }
      create_group("Nouveau Groupe", "Group", data)

Variables Globales
------------------

.. data:: url

   URL de l'API PHP pour les requêtes POST et DELETE.

   :type: str

   **Valeur :** ``"https://kicekifeqoa.alwaysdata.net/api.php"``

.. data:: config

   Configuration de connexion à la base de données MySQL.

   :type: dict

   **Exemple :**

   .. code-block:: python

      {
          'user': '379269_admin',
          'password': 'Kicekifeqoa123*',
          'host': 'mysql-kicekifeqoa.alwaysdata.net',
          'database': 'kicekifeqoa_todolist',
      }


Exemple Complet
---------------

.. code-block:: python

   from mysql.connector import connection, Error
   import requests

   # Configuration de la connexion
   config = {
       'user': '379269_admin',
       'password': 'Kicekifeqoa123*',
       'host': 'mysql-kicekifeqoa.alwaysdata.net',
       'database': 'kicekifeqoa_todolist',
   }

   # Connexion à la base de données
   conn = connection.MySQLConnection(**config)
   cursor = conn.cursor()

   # Créer un groupe si aucun doublon n'existe
   data = {
       'name': 'Nouveau Groupe',
       'description': 'Description du groupe'
   }
   create_group("Nouveau Groupe", "Group", data)
