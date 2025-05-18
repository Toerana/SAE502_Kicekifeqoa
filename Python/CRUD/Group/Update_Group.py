import requests

url = "https://kicekifeqoa.alwaysdata.net/api.php"

def update_group(id_group, name=None,):
    """
    Met à jour un groupe en utilisant l'API.

    Paramètres:
    - id_group (int) : ID du groupe.
    - name (str) : nouveau nom du groupe.

    Retourne:
    - Message de succès ou d'erreur.
    """

    post_data = {
        'table': 'Group',
        'action': 'update',
        'data': {},
        'column': "id_group",
        'value': id_group
    }

    # Ajouter les champs à mettre à jour
    if name:
        post_data['data']['name'] = name

    # Vérifier que des champs sont à mettre à jour
    if not post_data['update_data']:
        return "Aucun champ à mettre à jour."

    # Envoyer la requête PUT à l'API
    try:
        response = requests.put(url, json=post_data)
        if response.status_code == 200:
            return f"Groupe avec ID {id_group} mis à jour avec succès."
        else:
            return f"Erreur lors de la mise à jour : {response.status_code} - {response.text}"
    except requests.RequestException as e:
        return f"Erreur de connexion à l'API : {e}"

