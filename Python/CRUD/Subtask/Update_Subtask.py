import requests

url = "https://kicekifeqoa.alwaysdata.net/api.php"

def update_subtask(id_subtask, id_affected_task=None, name=None, end_date=None, checked=None):
    """
    Met à jour une sous-tâche en utilisant l'API.

    Paramètres:
    - id_subtask (int) : ID de la sous-tâche.
    - id_affected_task (int) : ID de la tâche affectée.
    - name (str) : nouveau nom.
    - end_date (str) : nouvelle date de fin au format 'YYYY-MM-DD HH:MM:SS'.
    - checked (int) : état de vérification (1 pour vérifié, 0 pour non vérifié).

    Retourne:
    - Message de succès ou d'erreur.
    """

    # Construire les données pour la requête POST
    post_data = {
        'table': 'Subtask',
        'action': 'update',
        'data': {},
        'column': "id_subtask",
        'value': id_subtask
    }

    # Ajouter les champs à mettre à jour
    if id_affected_task:
        post_data['data']['id_affected_task'] = id_affected_task
    if name:
        post_data['data']['name'] = name
    if end_date:
        post_data['data']['end_date'] = end_date
    if checked is not None:
        post_data['data']['checked'] = checked

    # Vérifier que des champs sont à mettre à jour
    if not post_data['data']:
        return "Aucun champ à mettre à jour."

    # Envoyer la requête POST à l'API
    try:
        response = requests.post(url, json=post_data)
        if response.status_code == 200:
            return f"Sous-tâche avec ID {id_subtask} mise à jour avec succès."
        else:
            return f"Erreur lors de la mise à jour : {response.status_code} - {response.text}"
    except requests.RequestException as e:
        return f"Erreur de connexion à l'API : {e}"

# Test
#print(update_subtask(12, name="Nouvelle Sous-Tâche", end_date="2024-10-20 15:30:00", checked=1))
