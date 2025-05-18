import os
import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
# from PySide6.QtCore import qInstallMessageHandler, QtMsgType
from Python.QT.Kicekifeqoa.Python.settings import url, import_paths

# Importation des gestionnaires de tâches depuis différents modules
from Python.QT.Kicekifeqoa.Python.taskhandlers.task_handler_Pcreate import TaskHandler as TaskHandlerCreate
from Python.QT.Kicekifeqoa.Python.taskhandlers.subtask_handler_Pcreate import TaskHandler as SubtaskHandlerCreate
from Python.QT.Kicekifeqoa.Python.taskhandlers.task_handler_Pupdate import TaskHandler as TaskHandlerUpdate
from Python.QT.Kicekifeqoa.Python.taskhandlers.subtask_handler_Pupdate import TaskHandler as SubtaskHandlerUpdate
from Python.QT.Kicekifeqoa.Python.taskhandlers.task_handler_Pdelete import TaskHandler as TaskHandlerDelete
from Python.QT.Kicekifeqoa.Python.taskhandlers.task_handler_AppRead import TaskHandlerAppRead as TaskHandlerBackend
from Python.QT.Kicekifeqoa.Python.taskhandlers.task_handler_Login import TaskHandlerLogin as TaskHandlerLogin
from Python.QT.Kicekifeqoa.Python.taskhandlers.task_handler_Register import TaskHandler as TaskHandlerRegister
from Python.QT.Kicekifeqoa.Python.colors import Colors

# Fonction de gestion des messages Qt (commentée)
'''
def message_handler(mode, context, message):
    if mode == QtMsgType.QtDebugMsg:
        print(f"Debug: {message}")
    elif mode == QtMsgType.QtInfoMsg:
        print(f"Info: {message}")
    elif mode == QtMsgType.QtWarningMsg:
        print(f"Warning: {message}")
    elif mode == QtMsgType.QtCriticalMsg:
        print(f"Critical: {message}")
    elif mode == QtMsgType.QtFatalMsg:
        print(f"Fatal: {message}")
'''


if __name__ == '__main__':
    choix = 1  # Définition du choix de style

    # Initialisation de l'application Qt
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Configuration du chemin de l'application
    app_dir = Path(__file__).parent
    engine.addImportPath(os.fspath(app_dir))

    # Définition de l'icône de l'application
    app.setWindowIcon(QIcon(str(app_dir / "Python/QT/Kicekifeqoa/KicekifeqoaContent/images/logo.png")))

    # Configuration des couleurs avec le style spécifié
    colors = Colors(style=choix)
    engine.rootContext().setContextProperty("Colors", colors)

    # Ajout des chemins d'import supplémentaires
    for path in import_paths:
        engine.addImportPath(os.fspath(app_dir / path))

    # Création des instances des gestionnaires de tâches
    task_handler_login = TaskHandlerLogin(engine)
    task_handler_create = TaskHandlerCreate(engine, task_handler_login)
    subtask_handler_create = SubtaskHandlerCreate(engine)
    task_handler_update = TaskHandlerUpdate(engine)
    subtask_handler_update = SubtaskHandlerUpdate(engine)
    task_handler_delete = TaskHandlerDelete(engine)
    task_handler_backend = TaskHandlerBackend(engine)
    task_handler_register = TaskHandlerRegister(engine)

    # Enregistrement des gestionnaires dans le contexte QML
    engine.rootContext().setContextProperty("taskHandlerRegister", task_handler_register)
    engine.rootContext().setContextProperty("taskHandlerLogin", task_handler_login)
    engine.rootContext().setContextProperty("taskHandlerCreate", task_handler_create)
    engine.rootContext().setContextProperty("subtaskHandlerCreate", subtask_handler_create)
    engine.rootContext().setContextProperty("taskHandlerUpdate", task_handler_update)
    engine.rootContext().setContextProperty("subtaskHandlerUpdate", subtask_handler_update)
    engine.rootContext().setContextProperty("taskHandlerDelete", task_handler_delete)
    engine.rootContext().setContextProperty("taskHandlerBackend", task_handler_backend)


    # Chargement du fichier QML principal
    engine.load(os.fspath(app_dir / url))
    if not engine.rootObjects():
        sys.exit(-1)  # Quitter si le chargement échoue

    # Lancer l'application
    sys.exit(app.exec())