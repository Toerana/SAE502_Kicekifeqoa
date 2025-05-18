from PySide6.QtCore import QObject, Slot, Signal
from Python.CRUD.Users.Create_User import create_user

class TaskHandler(QObject):
    registerSuccess = Signal()
    alreadyMail = Signal()
    badMail = Signal()
    shortPass = Signal()
    longPass = Signal()
    uppercasePass = Signal()
    lowercasePass = Signal()
    numberPass = Signal()
    specialPass = Signal()
    unknownError= Signal()

    def __init__(self, engine):
        super(TaskHandler, self).__init__()
        self.engine = engine

    @Slot(str, str)  # Accepter deux paramètres : email et password
    def checkCredentials(self, email, password):
        result = create_user(email,password)
        print(result)
        checkResults = {
            "Mail Exist":self.alreadyMail,
            "Mail NOK":self.badMail,
            "Pass <8": self.shortPass,
            "Pass >72":self.longPass,
            "Pass Uppercase":self.uppercasePass,
            "Pass Lowercase":self.lowercasePass,
            "Pass Number":self.numberPass,
            "Pass Special":self.specialPass,
            "Unkown Error":self.unknownError
        }

        if result[0] == True:
            self.registerSuccess.emit()
        else:
            signal = checkResults.get(result[1])
            signal.emit()