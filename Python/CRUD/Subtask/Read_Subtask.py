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

def get_subtask(id_subtask=None,id_affected_task=None, name=None, end_date=None, checked=None,):
    """
    Permet de récupérer les information d'une ou plusieurs sous-taches en fonction des paramètres entrer
    Si aucun paramètres n'est entrer retourne TOUTES les sous-tache (Peu recommander)
    Si id_subtask est entrer retourne une seul sous-tache
    Si plusieur sous-taches coresspondes au paramètres retourne plusieurs sous-taches
    (ex name="toto"end_date="2020-12-30 15:30:00")

    paramètres:
    id_subtask: int
    id_affected_subtask: int
    name : str
    end_date : str format YYYY-MM-JJ HH:mm:SS
    checked : int (1 ou 0)

    retourne une liste de dictionaire (key = nom colone, value = valeur)
    ex {'id_subtask':135}
    Si aucune correspondance trouver avec tout les pramètres entrer retourne 'no existing links'
    """
    if id_subtask != None:
        return get_data("Subtask",filter_column="id_subtask",filter_value=id_subtask)
    else:
        columns = {
            "id_subtask": id_subtask,
            "id_affected_task": id_affected_task,
            "name": name,
            "end_date": end_date,
            "checked": checked
        }
        filters = {col: value for col, value in columns.items() if value is not None}
        if len(filters) == 1:
            col, val = next(iter(filters.items()))
            data = get_data("Subtask", filter_column=col, filter_value=val)
            if data != []:
                return data
            else:
                return 'no existing links'
        elif len(filters) == 2:
            list =[]
            filter_col, filter_val = zip(*filters.items())
            data = get_data("Subtask",filter_column=filter_col[0],filter_value=filter_val[0])
            for task in data:
                if (task[filter_col[1]] == filter_val[1]):
                    list.append(task)
            if list != []:
                return list
            else:
                return "no existing links"
        elif len(filters) == 3:
            list =[]
            filter_col, filter_val = zip(*filters.items())
            data = get_data("Subtask", filter_column=filter_col[0], filter_value=filter_val[0])
            for task in data:
                if (task[filter_col[1]] == filter_val[1]) and (task[filter_col[2]] == filter_val[2]):
                    list.append(task)
            if list != []:
                return list
            else:
                return "no existing links"
        elif len(filters) == 4:
            list =[]
            filter_col, filter_val = zip(*filters.items())
            data = get_data("Subtask", filter_column=filter_col[0], filter_value=filter_val[0])
            for task in data:
                if (task[filter_col[1]] == filter_val[1]) and (task[filter_col[2]] == filter_val[2]) and (task[filter_col[3]] == filter_val[3]):
                    list.append(task)
            if list != []:
                return list
            else:
                return "no existing links"
        else:
            return get_data("Subtask")