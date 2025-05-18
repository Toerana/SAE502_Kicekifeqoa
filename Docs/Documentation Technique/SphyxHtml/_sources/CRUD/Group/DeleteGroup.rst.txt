Delete Group
========================

Ce module permet de se connecter à une base de données MySQL et de supprimer des groupes via une requête DELETE envoyée à une API PHP. Il inclut également une fonction pour fermer proprement les connexions à la base de données.

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

.. function:: delete_group(table, column, value)

   Supprime un groupe de la base de données en envoyant une requête DELETE à une API PHP.

   :param table: Nom de la table où se trouve le groupe à supprimer.
   :type table: str
   :param column: Colonne utilisée pour identifier le groupe à supprimer.
   :type column: str
   :param value: Valeur de la colonne pour identifier l'enregistrement à supprimer.
   :type value: str

   Cette fonction envoie une requête DELETE à l'API avec les informations spécifiées, puis ferme la connexion à la base de données.

   **Exemple d'utilisation :**

   .. code-block:: python

      delete_group("Group", "name", "TestGroup")


Variables Globales
------------------

.. data:: url

   URL de l'API PHP pour les requêtes DELETE.

   :type: str

   **Valeur :** ``"http://kicekifeqoa.alwaysdata.net/api.php"``

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

   from mysql.connector import connection
   import requests
   import json

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

   # Suppression d'un groupe
   delete_group("Group", "name", "TestGroup")
