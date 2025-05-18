Update Group
=======================

Ce module permet de mettre à jour un groupe dans une base de données via une requête à une API PHP.

Fonctions
---------

.. function:: update_group(id_group, name=None)

   Met à jour un groupe en utilisant l'API.

   :param id_group: Identifiant du groupe à mettre à jour.
   :type id_group: int
   :param name: Nouveau nom du groupe (optionnel).
   :type name: str, optionnel

   :return: Un message indiquant le succès ou l'échec de l'opération.
   :rtype: str

   **Exemples d'utilisation :**

   Mettre à jour le nom du groupe avec l'ID 1 :

   .. code-block:: python

      result = update_group(1, name="Nouveau Nom du Groupe")
      print(result)

   Si aucun champ à mettre à jour n'est spécifié :

   .. code-block:: python

      result = update_group(1)
      print(result)

   **Messages de retour possibles :**

   - ``"Groupe avec ID <id_group> mis à jour avec succès."``
   - ``"Erreur lors de la mise à jour : <code d'erreur> - <message d'erreur>"``
   - ``"Aucun champ à mettre à jour."``
   - ``"Erreur de connexion à l'API : <description de l'erreur>"``

Variables Globales
------------------

.. data:: url

   URL de l'API PHP utilisée pour les requêtes de mise à jour.

   :type: str

   **Valeur :** ``"https://kicekifeqoa.alwaysdata.net/api.php"``
