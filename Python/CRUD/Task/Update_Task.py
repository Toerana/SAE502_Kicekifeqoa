import requests

url = "https://kicekifeqoa.alwaysdata.net/api.php"


def fetch_task(id_task):
    """
    Récupère les détails d'une tâche existante en utilisant l'API.

    Paramètres:
    - id_task (int) : l'ID de la tâche à récupérer.

    Retourne:
    - Les données de la tâche ou un message d'erreur.
    """
    post_data = {
        'table': 'Task',
        'action': 'read',  # Action pour lire les données
        'column': 'id_task',
        'value': id_task
    }

    response = requests.post(url, json=post_data)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            return data['data'][0]  # Retourne les données de la tâche
        else:
            return f"Aucune tâche trouvée avec l'ID {id_task}."
    else:
        return f"Erreur lors de la récupération : {response.status_code} - {response.text}"


def update_task(id_task, name=None, end_date=None, checked=None, priority=None, tag=None):
    """
    Met à jour une tâche existante en utilisant l'API.
    
    Paramètres:
    - id_task (int) : l'ID de la tâche à mettre à jour.
    - name (str) : nouveau nom de la tâche.
    - end_date (str) : nouvelle date de fin au format 'YYYY-MM-DD HH:MM:SS'.
    - checked (int) : statut vérifié (1) ou non vérifié (0).
    - priority (int) : nouvelle priorité.
    - tag (str) : nouveau tag.
    
    Retourne:
    - Message de succès ou d'erreur.
    """
    post_data = {
        'table': 'Task',
        'action': 'update',
        'data': {},
        'column': "id_task",
        'value': id_task
    }

    # Champs à mettre à jour
    if name is not None:
        post_data['data']['name'] = name
    if end_date is not None:
        post_data['data']['end_date'] = end_date
    if checked is not None:
        post_data['data']['checked'] = checked
    if priority is not None:
        post_data['data']['priority'] = priority
    if tag is not None:
        post_data['data']['tag'] = tag

    if not post_data['data']:
        print("Aucun champ à mettre à jour.")
        return

    # Mise à jour avec PUT 
    response = requests.post(url, json=post_data)

    # Vérifier la réponse de l'API
    if response.status_code == 200:
        return f"Tâche avec ID {id_task} mise à jour avec succès."
    else:
        return f"Erreur lors de la mise à jour : {response.status_code} - {response.text}"
