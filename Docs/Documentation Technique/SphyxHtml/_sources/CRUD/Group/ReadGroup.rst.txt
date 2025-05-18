Read Group
================

Ce module permet de récupérer des informations sur les groupes, les utilisateurs associés à des groupes, et les tâches assignées à des groupes via une API PHP.

Fonctions
---------

.. function:: get_data(table, columns='*', filter_column=None, filter_value=None, join_table=None, join_condition=None)

   Récupère des données d'une table spécifique via l'API.

   :param table: Nom de la table principale à interroger.
   :type table: str
   :param columns: Colonnes à récupérer (par défaut toutes les colonnes).
   :type columns: str, optionnel
   :param filter_column: Colonne pour appliquer un filtre.
   :type filter_column: str, optionnel
   :param filter_value: Valeur du filtre pour la colonne spécifiée.
   :type filter_value: str, optionnel
   :param join_table: Nom de la table pour effectuer une jointure.
   :type join_table: str, optionnel
   :param join_condition: Condition de jointure entre les tables.
   :type join_condition: str, optionnel

   :return: Les données récupérées sous forme de dictionnaire JSON ou un message d'erreur.
   :rtype: dict ou str

   **Exemple d'utilisation :**

   .. code-block:: python

      data = get_data("Group", columns="id_group, name", filter_column="id_group", filter_value=1)

.. function:: get_group(id_group=None, name=None)

   Récupère les informations d'un ou plusieurs groupes. Si aucun paramètre n'est spécifié, retourne tous les groupes.

   :param id_group: Identifiant du groupe.
   :type id_group: int, optionnel
   :param name: Nom du groupe.
   :type name: str, optionnel

   :return: Une liste de dictionnaires contenant les informations des groupes ou un message indiquant qu'aucune correspondance n'a été trouvée.
   :rtype: list ou str

   **Exemple d'utilisation :**

   .. code-block:: python

      groups = get_group(id_group=1)
      all_groups = get_group()

.. function:: get_group_user(id_group)

   Récupère une liste des utilisateurs appartenant à un groupe donné.

   :param id_group: Identifiant du groupe.
   :type id_group: int

   :return: Une liste des identifiants des utilisateurs associés au groupe.
   :rtype: list

   **Exemple d'utilisation :**

   .. code-block:: python

      users = get_group_user(1)

.. function:: get_group_task(id_group)

   Récupère une liste des tâches assignées à un groupe donné.

   :param id_group: Identifiant du groupe.
   :type id_group: int

   :return: Une liste des identifiants des tâches associées au groupe.
   :rtype: list

   **Exemple d'utilisation :**

   .. code-block:: python

      tasks = get_group_task(1)

Variables Globales
------------------

.. data:: url

   URL de l'API PHP utilisée pour les requêtes.

   :type: str

   **Valeur :** ``"https://kicekifeqoa.alwaysdata.net/api.php"``


Exemple Complet
---------------

.. code-block:: python

   # Récupérer tous les groupes
   all_groups = get_group()

   # Récupérer un groupe par son identifiant
   group = get_group(id_group=1)

   # Récupérer les utilisateurs d'un groupe spécifique
   users = get_group_user(1)

   # Récupérer les tâches assignées à un groupe spécifique
   tasks = get_group_task(1)
