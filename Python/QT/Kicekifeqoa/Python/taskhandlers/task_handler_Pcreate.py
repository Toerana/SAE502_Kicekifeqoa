from PySide6.QtCore import QObject, Slot, Signal
from Python.CRUD.Task.Create_Task import add_recup
from Python.CRUD.Task_has_Users.Create_Task_has_Users import create_task_user_association

class TaskHandler(QObject):
    # Signal pour informer le QML en cas de succès
    validationSuccess = Signal()

    # Initialise le gestionnaire de tâches avec les attributs par défaut
    def __init__(self, engine, TaskHandlerLogin):
        super().__init__()
        self.engine = engine
        self.login_handler = TaskHandlerLogin
        self.task_name = ""
        self.task_priority = 0
        self.tags = []
        self.users = []
        self.end_date = None
        self.checked = 0
        self.user_id = None

    @Slot(str)
    def add_task_name(self, taskname):
        # Ajoute le nom de la tâche si non vide
        if taskname.strip():
            self.task_name = taskname
        else:
            print("Erreur : Le nom de la tâche ne peut pas être vide.")

    @Slot(int)
    def add_task_priority(self, priority):
        # Ajoute la priorité si elle est valide (0, 1 ou 2)
        if priority in [0, 1, 2]:
            self.task_priority = priority
        else:
            print("Erreur : Priorité invalide.")

    @Slot(str)
    def add_tag(self, tag):
        # Ajoute un tag si non vide
        if tag.strip():
            self.tags.append(tag)
            self._update_tags_in_qml()
        else:
            print("Erreur : Tag invalide.")

    @Slot()
    def remove_last_tag(self):
        # Supprime le dernier tag de la liste
        if self.tags:
            self.tags.pop()
            self._update_tags_in_qml()

    @Slot(str)
    def add_user(self, user):
        # Ajoute un utilisateur si non vide
        if user.strip():
            self.users.append(user)
            self._update_users_in_qml()
        else:
            print("Erreur : Utilisateur invalide.")

    @Slot()
    def remove_last_user(self):
        # Supprime le dernier utilisateur de la liste
        if self.users:
            self.users.pop()
            self._update_users_in_qml()

    def _update_tags_in_qml(self):
        # Met à jour le modèle des tags dans le QML
        root_object = self.engine.rootObjects()[0]
        root_object.setProperty("tagsListModel", self.tags)

    def _update_users_in_qml(self):
        # Met à jour le modèle des utilisateurs dans le QML
        root_object = self.engine.rootObjects()[0]
        root_object.setProperty("usersListModel", self.users)

    @Slot(str)
    def add_end_date(self, enddate):
        # Ajoute une date de fin après validation
        try:
            self.end_date = self._validate_date_format(enddate)
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
    def validate_info(self):
        # Valide les informations de la tâche et les enregistre
        try:
            # Récupère l'ID utilisateur depuis le gestionnaire de login
            self.user_id = self.login_handler.get_user_id()

            # Vérifie si le nom et la date de fin sont renseignés
            if not self.task_name:
                raise ValueError("Le nom de la tâche ne peut pas être vide.")
            if not self.end_date:
                raise ValueError("La date de fin doit être renseignée.")
            self._check_dates_consistency()

            # Formate les tags en une seule chaîne
            formatted_tags = ", ".join(self.tags)

            # Prépare les données pour créer une nouvelle tâche
            data = {
                "Task": {
                    "name": self.task_name,
                    "end_date": self.end_date,
                    "checked": self.checked,
                    "priority": self.task_priority,
                    "tag": formatted_tags
                }
            }

            # Ajoute la tâche et récupère son ID
            id_task = add_recup(data)

            # Associe l'utilisateur à cette tâche
            create_task_user_association("Task_has_Users", {
                "task_id": id_task,
                "user_id": self.user_id,
            })

            # Associe le compte admin (ID 1) à cette tâche
            create_task_user_association("Task_has_Users", {
                "task_id": id_task,
                "user_id": 1,
            })

            self.validationSuccess.emit()

            # Réinitialise les attributs après la création de la tâche
            self.task_name = ""
            self.task_priority = 0
            self.tags = []
            self.users = []
            self.end_date = None
            self.checked = 0

        except ValueError as e:
            print(f"Erreur de validation : {e}")
