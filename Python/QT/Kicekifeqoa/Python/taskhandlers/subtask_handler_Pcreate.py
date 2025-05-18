from PySide6.QtCore import QObject, Slot, Signal
from Python.CRUD.Subtask.Create_Subtask import create_subtask


class TaskHandler(QObject):
    # Signal pour informer le QML en cas de succès
    validationSuccess = Signal()

    # Initialise le gestionnaire de sous-tâches avec les attributs par défaut
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.task_id = ""
        self.task_name = ""
        self.end_date = None
        self.checked = 0

    @Slot(str)
    def define_parent_task_id(self, parenttaskid):
        # Définit l'ID de la tâche parente à partir de la chaîne donnée
        if parenttaskid.strip():
            self.parent_task_id = parenttaskid.split('.')[-1]
        else:
            print("Erreur : L'ID de la tâche parente ne peut pas être vide.")

    @Slot(str)
    def add_task_name(self, taskname):
        # Définit le nom de la sous-tâche si non vide
        if taskname.strip():
            self.task_name = taskname
        else:
            print("Erreur : Le nom de la tâche ne peut pas être vide.")

    @Slot(str)
    def add_end_date(self, enddate):
        # Définit et valide la date de fin de la sous-tâche
        try:
            self.end_date = self._validate_date_format(enddate)
        except ValueError as e:
            print(f"Erreur : {e}")

    def _validate_date_format(self, date_str):
        # Valide le format de la date fournie
        from Python.QT.Kicekifeqoa.Python.format_date import validate_date_format
        return validate_date_format(date_str)

    def _check_dates_consistency(self):
        # Vérifie la cohérence des dates
        if self.end_date:
            from Python.QT.Kicekifeqoa.Python.format_date import check_dates_consistency
            check_dates_consistency(self.end_date)

    @Slot(int)
    def task_completed(self, status):
        # Met à jour le statut d'achèvement de la sous-tâche (0 = non terminée, 1 = terminée)
        self.checked = status

    @Slot()
    def validate_info(self):
        # Valide les informations de la sous-tâche et la crée dans la base de données
        try:
            if not self.task_name:
                raise ValueError("Le nom de la tâche ne peut pas être vide.")
            if not self.end_date:
                raise ValueError("La date de fin doit être renseignée.")

            # Vérifie la cohérence des dates
            self._check_dates_consistency()

            # Crée la sous-tâche avec les informations collectées
            create_subtask("Subtask", {
                "id_affected_task": self.parent_task_id,
                "name": self.task_name,
                "end_date": self.end_date,
                "checked": self.checked,
            })

            self.validationSuccess.emit()
        except ValueError as e:
            print(f"Erreur de validation : {e}")
