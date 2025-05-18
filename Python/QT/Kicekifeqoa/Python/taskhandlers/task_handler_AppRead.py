from PySide6.QtCore import QObject, Slot, Signal
from Python.CRUD.Task.Read_Task import get_data
from Python.CRUD.Subtask.Read_Subtask import get_data as get_subtask_data
from Python.QT.Kicekifeqoa.Python.format_date import read_date_format

class TaskHandlerAppRead(QObject):
    # Signaux pour transmettre les tâches filtrées au QML
    tasksFetchedPriority2 = Signal(list, arguments=['tasks'])
    tasksFetchedPriority1 = Signal(list, arguments=['tasks'])
    tasksFetchedPriority0 = Signal(list, arguments=['tasks'])
    tasksFetchedChecked = Signal(list, arguments=['tasks'])

    def __init__(self, engine):
        # Initialise le gestionnaire avec le moteur QML
        super(TaskHandlerAppRead, self).__init__()
        self.engine = engine

    @Slot(int)
    def fetchTasks(self, user_id):
        # Récupère et émet les tâches par priorité et statut d'achèvement
        tasks_priority2 = self.get_tasks_from_api(user_id=user_id, priority_filter=2, exclude_checked=True)
        tasks_priority1 = self.get_tasks_from_api(user_id=user_id, priority_filter=1, exclude_checked=True)
        tasks_priority0 = self.get_tasks_from_api(user_id=user_id, priority_filter=0, exclude_checked=True)
        tasks_checked = self.get_tasks_from_api(user_id=user_id, checked_filter=1)
        subtasks = self.get_subtasks_from_api(exclude_checked=False)

        # Groupe les sous-tâches avec leurs tâches parentes
        grouped_priority2 = self.group_tasks_with_subtasks(tasks_priority2, subtasks)
        grouped_priority1 = self.group_tasks_with_subtasks(tasks_priority1, subtasks)
        grouped_priority0 = self.group_tasks_with_subtasks(tasks_priority0, subtasks)
        grouped_checked = self.group_tasks_with_subtasks(tasks_checked, subtasks)

        # Émet les tâches groupées via les signaux
        self.tasksFetchedPriority2.emit(grouped_priority2)
        self.tasksFetchedPriority1.emit(grouped_priority1)
        self.tasksFetchedPriority0.emit(grouped_priority0)
        self.tasksFetchedChecked.emit(grouped_checked)

    def get_tasks_from_api(self, user_id=None, priority_filter=None, checked_filter=None, exclude_checked=False):
        # Récupère les tâches depuis l'API avec filtres sur priorité et statut d'achèvement
        response = get_data(
            "Task_has_Users",
            columns="Task.*",
            join_table="Task",
            join_condition="Task_has_Users.task_id = Task.id_task",
            filter_column="Task_has_Users.user_id",
            filter_value=user_id
        )

        if isinstance(response, str) and response.startswith("Erreur"):
            print(f"Erreur lors de la récupération des tâches : {response}")
            return []

        filtered_tasks = response

        # Filtre par priorité si applicable
        if priority_filter is not None:
            filtered_tasks = [task for task in filtered_tasks if task['priority'] == priority_filter]

        # Exclut les tâches cochées si demandé
        if exclude_checked:
            filtered_tasks = [task for task in filtered_tasks if task['checked'] != 1]

        # Filtre par tâches cochées si applicable
        if checked_filter is not None:
            filtered_tasks = [task for task in filtered_tasks if task['checked'] == checked_filter]

        # Formate les tâches pour l'affichage
        return [{
            "id_task": task['id_task'],
            "name": task['name'],
            "end_date": read_date_format(task['end_date']),
            "checked": task['checked'],
            "priority": task['priority'],
            "tag": task['tag']
        } for task in filtered_tasks]

    def get_subtasks_from_api(self, exclude_checked=False):
        # Récupère les sous-tâches et les informations des tâches parentes
        subtasks_response = get_subtask_data("Subtask", columns="id_subtask, id_affected_task, name, end_date, checked")
        tasks_response = get_data("Task", columns="id_task, priority")
        task_users_response = get_data("Task_has_Users", columns="task_id, user_id")

        # Gère les erreurs de récupération
        if isinstance(subtasks_response, str) and subtasks_response.startswith("Erreur"):
            print(f"Erreur lors de la récupération des sous-tâches : {subtasks_response}")
            return []
        if isinstance(tasks_response, str) and tasks_response.startswith("Erreur"):
            print(f"Erreur lors de la récupération des tâches parentes : {tasks_response}")
            return []
        if isinstance(task_users_response, str) and task_users_response.startswith("Erreur"):
            print(f"Erreur lors de la récupération des utilisateurs assignés : {task_users_response}")
            return []

        # Associe les priorités aux tâches parentes
        task_priorities = {task['id_task']: task['priority'] for task in tasks_response}

        # Associe les utilisateurs aux tâches parentes
        task_users = {}
        for relation in task_users_response:
            task_id = relation['task_id']
            user_id = relation['user_id']
            if task_id not in task_users:
                task_users[task_id] = []
            task_users[task_id].append(user_id)

        # Filtre les sous-tâches cochées si demandé
        if exclude_checked:
            subtasks_response = [subtask for subtask in subtasks_response if subtask['checked'] != 1]

        # Formate les sous-tâches avec héritage des priorités et utilisateurs
        return [{
            "id_task": float(f"{subtask['id_subtask']}.{subtask['id_affected_task']}"),
            "id_task_str": f"{subtask['id_subtask']}.{subtask['id_affected_task']}",
            "name": f"↳ {subtask['name']}",
            "end_date": read_date_format(subtask['end_date']),
            "checked": subtask['checked'],
            "priority": task_priorities.get(subtask['id_affected_task'], None),
            "tag": "",
            "parent_id": subtask['id_affected_task'],
            "users": task_users.get(subtask['id_affected_task'], [])
        } for subtask in subtasks_response]

    def group_tasks_with_subtasks(self, tasks, subtasks):
        # Groupe les sous-tâches avec leurs tâches parentes
        subtasks_by_parent = {}
        for subtask in subtasks:
            parent_id = subtask['parent_id']
            if parent_id not in subtasks_by_parent:
                subtasks_by_parent[parent_id] = []
            subtasks_by_parent[parent_id].append(subtask)

        # Ajoute les sous-tâches aux tâches parentes
        grouped_tasks = []
        for task in tasks:
            grouped_tasks.append(task)
            if task['id_task'] in subtasks_by_parent:
                grouped_tasks.extend(subtasks_by_parent[task['id_task']])

        return grouped_tasks
