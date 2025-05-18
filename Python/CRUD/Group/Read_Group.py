import requests

url = "https://kicekifeqoa.alwaysdata.net/api.php"

def get_data(table, columns='*', filter_column=None, filter_value=None, join_table=None, join_condition=None):
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
        return response.json()
    else:
        return(f"Erreur : {response.status_code} - {response.text}")


def get_group(id_group=None,name=None):
    """
    Permet de récupérer les information d'un ou plisueur groupe
    Si aucun paramètre n'est entrée retourne TOUT les groupes (peu recoomander)

    paramètres:
    id_group: int
    name: str

    Retourne une liste de dictionaire
    Si aucune correspondance trouver avec tout les pramètres entrer retourne 'no existing links'
    """
    if id_group != None:
        data = get_data("Group", filter_column="id_group", filter_value=id_group)
        if data != []:
            return data
        else:
            return 'no existing links'
    elif name != None:
        data = get_data("Group", filter_column="name", filter_value=name)
        if data != []:
            return data
        else:
            return 'no existing links'
    else:
        return get_data("Group")

def get_group_user(id_group):
    """
    Retourne une liste de TOUT les utilisateur apparetenant a un groupe

    :param id_group: int
    :return: Liste int des id d'utilisateur
    """
    user_list =[]
    data = get_data("Group_has_Users", columns="Users.id_user", filter_column="group_id",
                    filter_value=id_group, join_table="Users",join_condition="Users.id_user = Group_has_Users.user_id")
    for user in data:
        user_list.append(user['id_user'])
    return user_list


def get_group_task(id_group):
    """
    Retourne une liste de TOUTES les taches affecter a un groupe

    :param id_group: int
    :return: Liste int des id de taches
    """
    task_list = []
    data = get_data("Task_has_Group", columns="Task.id_task", filter_column="group_id",
                    filter_value=id_group, join_table="Task", join_condition="Task.id_task = Task_has_Group.task_id")
    for task in data:
        task_list.append(task['id_task'])
    return task_list