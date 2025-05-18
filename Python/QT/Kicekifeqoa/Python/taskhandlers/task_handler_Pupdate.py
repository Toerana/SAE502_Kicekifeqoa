from PySide6.QtCore import QObject, Slot, Signal
from Python.CRUD.Task.Update_Task import update_task, fetch_task
from Python.CRUD.Task.Read_Task import get_task
from Python.QT.Kicekifeqoa.Python.format_date import read_date_format

class TaskHandler(QObject):
    # Signal pour informer le QML en cas de succès
    validationSuccess = Signal()

    # Signal pour transmettre les données de la tâche au QML
    taskFetched = Signal(dict)

    def __init__(self, engine):
        # Initialise les attributs par défaut
        super().__init__()
        self.engine = engine
        self.task_id = ""
        self.task_name = ""
        self.task_priority = 0
        self.tags = []
        self.end_date = None
        self.checked = 0

    @Slot(str)
    def fetch_task_by_id(self, task_id):
        # Récupère une tâche par ID et envoie les données au QML
        try:
            task_data = get_task(id_task=task_id)

            if isinstance(task_data, list) and len(task_data) > 0:
                task = task_data[0]
                self.task_id = task_id
                self.task_name = task.get("name", "")
                self.task_priority = task.get("priority", 0)
                self.tags = task.get("tag", "").split(",") if task.get("tag") else []
                print(f"Tags récupérés : {self.tags}")

                # Formatage de la date de fin
                raw_end_date = task.get("end_date", None)
                self.end_date = read_date_format(raw_end_date) if raw_end_date else None
                self.checked = task.get("checked", 0)

                # Envoie les informations de la tâche au QML
                self.taskFetched.emit({
                    "task_id": self.task_id,
                    "task_name": self.task_name,
                    "task_priority": self.task_priority,
                    "tag": self.tags,
                    "end_date": self.end_date,
                    "checked": self.checked
                })
            else:
                print(f"Aucune tâche trouvée avec l'ID : {task_id}")
        except Exception as e:
            print(f"Erreur lors de la récupération de la tâche : {e}")

    @Slot(str)
    def update_task_name(self, updatetaskname):
        # Met à jour le nom de la tâche si non vide
        if updatetaskname.strip():
            self.task_name = updatetaskname
        else:
            print("Erreur : Le nom de la tâche ne peut pas être vide.")

    @Slot(int)
    def update_task_priority(self, updatepriority):
        # Met à jour la priorité de la tâche si valide (0, 1, 2)
        if updatepriority in [0, 1, 2]:
            self.task_priority = updatepriority
        else:
            print("Erreur : Priorité invalide.")

    @Slot(str)
    def add_tag(self, tagname):
        # Ajoute un tag si non vide
        if tagname.strip():
            if not isinstance(self.tags, list):
                self.tags = []
            self.tags.append(tagname)
            self._update_tags_in_qml()
        else:
            print("Erreur : Tag invalide.")

    @Slot()
    def remove_last_tag(self):
        # Supprime le dernier tag de la liste
        if self.tags:
            self.tags.pop()
            self._update_tags_in_qml()

    def _update_tags_in_qml(self):
        # Met à jour les tags dans le modèle QML
        root_object = self.engine.rootObjects()[0]
        root_object.setProperty("tagsListModel", self.tags)

    def _update_users_in_qml(self):
        # Met à jour les utilisateurs dans le modèle QML (non utilisé ici)
        root_object = self.engine.rootObjects()[0]
        root_object.setProperty("usersListModel", self.users)

    @Slot(str)
    def update_end_date(self, updateenddate):
        # Met à jour la date de fin après validation
        try:
            self.end_date = self._validate_date_format(updateenddate)
        except ValueError as e:
            print(f"Erreur : {e}")

    def _validate_date_format(self, date_str):
        # Valide le format de la date
        from Python.QT.Kicekifeqoa.Python.format_date import validate_date_format
        return validate_date_format(date_str)

    def _check_dates_consistency(self):
        # Vérifie la cohérence des dates
        if self.end_date:
            from Python.QT.Kicekifeqoa.Python.format_date import check_dates_consistency
            check_dates_consistency(self.end_date)

    @Slot(int)
    def task_completed(self, status):
        # Met à jour le statut d'achèvement de la tâche
        self.checked = status

    @Slot()
    def validate_update_info(self):
        # Valide et enregistre les mises à jour de la tâche
        try:
            # Vérifie d'abord les conditions de validation
            if not self.task_name.strip():
                raise ValueError("Le nom de la tâche est obligatoire.")
            if not self.end_date.strip():
                raise ValueError("La date de fin est obligatoire.")
            self._check_dates_consistency()

            # Si les validations passent, appelle update_task
            response = update_task(
                id_task=self.task_id,
                name=self.task_name,
                end_date=self.end_date,
                checked=self.checked,
                priority=self.task_priority,
                tag=", ".join(self.tags)
            )

            # Vérifie la réponse après l'appel à update_task
            if "succès" in response.lower():
                print("Mise à jour réussie :", response)
                self.validationSuccess.emit()
            else:
                print("Erreur lors de la mise à jour :", response)

        except ValueError as ve:
            # Affiche l'erreur de validation
            print("Erreur de validation :", ve)
        except Exception as e:
            # Gère les erreurs inattendues
            print("Erreur inattendue :", e)
