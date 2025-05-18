from PySide6.QtCore import QObject, Slot
from Python.CRUD.Task.Delete_Task import delete_task
from Python.CRUD.Subtask.Delete_Subtask import delete_subtask

class TaskHandler(QObject):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.task_id = ""
        self.delete_info = ""

    @Slot(str)
    def set_task_id(self, taskid):
        if taskid.strip():
            self.task_id = taskid
            print(f"Debug: Tâche sélectionnée ID: {self.task_id}")
        else:
            print("Erreur : L'id de la tâche ne peut pas être vide.")

    @Slot()
    def validate_delete_info(self):
        try:
            if not self.task_id:
                raise ValueError("Aucune tâche n'est sélectionnée")

            # Vérification du format YY.XX pour les sous-tâches
            if "." in self.task_id:
                subtask_id, main_task = self.task_id.split(".")
                subtask_id = subtask_id.strip()
                main_task = main_task.strip()

                print(f"Debug: Identifiant de la sous-tâche: {subtask_id}")
                print(f"Debug: Identifiant de la tâche principale: {main_task}")

                delete_subtask("Subtask", "id_subtask", subtask_id)
                print(f"Deleted Subtask: {subtask_id}")
            else:
                # Supprimer toutes les sous-tâches associées avant de supprimer la tâche
                delete_subtask("Subtask", "id_affected_task", self.task_id)
                print(f"Deleted all subtasks associated with Task: {self.task_id}")

                # Ensuite, supprimer la tâche principale
                delete_task("Task", "id_task", self.task_id)
                print(f"Deleted Task: {self.task_id}")

        except ValueError as e:
            print(f"Erreur de validation : {e}")

