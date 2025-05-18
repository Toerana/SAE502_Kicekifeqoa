from pathlib import Path
from PySide6.QtCore import QObject, Slot, Signal
import os
from Python.CRUD.Users.Read_User import  get_users
from Python.QT.Kicekifeqoa.Python.taskhandlers.task_handler_AppRead import TaskHandlerAppRead
import bcrypt

class TaskHandlerLogin(QObject):
    loginSuccess = Signal(int)  # Déclaration du signal
    loginPasswdFail = Signal()
    loginEmailFail = Signal()

    def __init__(self, engine):
        super(TaskHandlerLogin, self).__init__()
        self.engine = engine
        self._user_id = None  # Variable pour stocker l'ID de l'utilisateur

    def verify_password(self, stored_password, provided_password):
        # Compare le mot de passe fourni avec le hash stocké
        return bcrypt.checkpw(provided_password.encode(), stored_password)

    @Slot(str, str)
    def checkCredentials(self, email, password):
        if email != "":  # Vérifie si le mail n'est pas vide
            result = get_users(email=email)
        else:
            result = 'no existing links'

        if result != 'no existing links':
            user_data = result[0]
            stored_password = user_data["password"].encode("utf-8")  # transforme le hash de str à Bytes

            if self.verify_password(stored_password, password):
                # Récupère l'ID de l'utilisateur après une connexion réussie
                self._user_id = user_data["id_user"]
                # Émettre le signal pour fermer la fenêtre de login
                self.loginSuccess.emit(self._user_id)

                # Charger la nouvelle interface App.qml
                app_qml_path = Path(__file__).resolve().parents[2] / "KicekifeqoaContent" / "App.qml"
                print(f"Chargement de : {app_qml_path}")
                self.engine.load(os.fspath(app_qml_path))

                # Créer une instance de TaskHandlerAppRead pour récupérer les tâches de l'utilisateur
                task_handler_AppRead = TaskHandlerAppRead(self.engine)
                task_handler_AppRead.fetchTasks(self._user_id)  # Appeler la fonction pour récupérer les tâches de l'utilisateur
            else:
                self.loginPasswdFail.emit()
        else:
            self.loginEmailFail.emit()

    def get_user_id(self):
        return self._user_id
