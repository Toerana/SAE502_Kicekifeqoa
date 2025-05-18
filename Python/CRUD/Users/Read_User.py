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

def get_users(id_user=None,email=None):
    """
    Permet de récupérer les information d'un ou plusieurs utilisateur
    Si aucun paramètre n'est entrée retourne TOUT les utilisateur (peu recoomander)
    Si id_user est entrer retourne un seul utilisateur
    Si plusieur utilisateurs coresspondes au paramètres retourne plusieurs utilisateurs
    paramètres:
    id_user: int
    email: str
    Retourne une liste de dictionaire
    Si aucune correspondance trouver avec tout les pramètres entrer retourne 'no existing links'
    """
    if id_user != None:
        data = get_data("Users", filter_column="id_user", filter_value=id_user)
        if data != []:
            return data
        else:
            return 'no existing links'
    elif email != None:
        data = get_data("Users", filter_column="email", filter_value=email)
        if data != []:
            return data
        else:
            return 'no existing links'
    else:
        return get_data("Users")
def get_users_group(id_user=None):
    """
    Retourne le ou les groupes auquels apartien un ou plusieurs utilisateurs
    Attention si un utilisateur est dans plusieurs groupes il est présent plusieur fois (1 dictionaire par groupe)
    Si aucun paramètre n'est entrée retourne la table Group_has_Users
    :param id_user: int
    :return: liste de dictionaire avec pour clé id_user,group_id,name
    ex [{'id_user': 3, 'group_id': 2, 'name': 'IT'},]
    """
    if id_user != None:
        data = get_data("Group_has_Users",columns="Users.id_user,Group_has_Users.group_id",filter_column="user_id",
                        filter_value=id_user,join_table="Users",join_condition="Users.id_user = Group_has_Users.user_id")
        if data != []:
            data_to_return = []
            for user in data:
                group_data = get_data("Group",columns="name",filter_column="id_group",filter_value=user["group_id"])
                user['name'] = ((group_data[0])['name'])
                data_to_return.append(user)
            return data_to_return
        else:
            return 'no existing links'
    else:
        return get_data("Group_has_Users")
def get_users_task(id_user=None):
    """
    Retourne la ou les taches auquels apartien un ou plusieurs utilisateurs
    Attention si un utilisateur est affecter a plusieur taches il est présent plusieur fois (1 dictionaire par tache)
    Si aucun paramètre n'est entrée retourne la table Task_has_Users
    :param id_user: int
    :return: liste de dictionaire avec pour clé id_user,task_id,name
    ex [{'id_user': 3, 'task_id': 160, 'name': 'Tache'},]
    """
    if id_user != None:
        data = get_data("Task_has_Users", columns="Users.id_user,Task_has_Users.task_id", filter_column="user_id",
                        filter_value=id_user, join_table="Users",join_condition="Users.id_user = Task_has_Users.user_id")
        if data != []:
            data_to_return = []
            for user in data:
                task_data = get_data("Task", columns="name", filter_column="id_task", filter_value=user["task_id"])
                user['name'] = ((task_data[0])['name'])
                data_to_return.append(user)
            return data_to_return
        else:
            return 'no existing links'
    else:
        return get_data("Task_has_Users")
def get_users_subtask(id_user=None):
    """
    Retourne la ou les sous-taches auquels apartien un ou plusieurs utilisateurs
    Attention si un utilisateur est affecter a plusieur sous-taches il est présent plusieur fois (1 dictionaire par sous-tache)
    Si aucun paramètre n'est entrée retourne la table Subtask_has_Users
    :param id_user: int
    :return: liste de dictionaire avec pour clé id_user,task_id,name
    ex [{'id_user': 3, 'subtask_id': 160, 'name': 'SousTache'},]
    """
    if id_user != None:
        data = get_data("Subtask_has_Users", columns="Users.id_user,Subtask_has_Users.subtask_id", filter_column="user_id",
                        filter_value=id_user, join_table="Users",join_condition="Users.id_user = Subtask_has_Users.user_id")
        if data != []:
            data_to_return = []
            for user in data:
                subtask_data = get_data("Subtask", columns="name", filter_column="id_subtask", filter_value=user["subtask_id"])
                user['name'] = ((subtask_data[0])['name'])
                data_to_return.append(user)
            return data_to_return
        else:
            return 'no existing links'
    else:
        return get_data("Task_has_Users")