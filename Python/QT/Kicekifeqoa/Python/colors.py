from PySide6.QtCore import QObject, Property, Slot, Signal


class Colors(QObject):
    styleChanged = Signal()  # Signal pour notifier le changement de style

    def __init__(self, parent=None, style=1):
        super().__init__(parent)
        self._style = style

    @Slot()
    def changeStyle(self):
        self._style += 1
        if self._style > 12:  # 12 styles au total, y compris le thème par défaut
            self._style = 1
        self.styleChanged.emit()

    @Property(int, notify=styleChanged)
    def style(self):
        return self._style

    @Property(str, constant=True)
    def couleur1(self):  # Couleur du fond
        if self.style == 1:
            return "#4E598C"  # Thème par défaut
        elif self.style == 2:
            return "#2C3E50"  # Thème 1
        elif self.style == 3:
            return "#563D7C"  # Thème 2
        elif self.style == 4:
            return "#34495E"  # Thème 3
        elif self.style == 5:
            return "#5D4037"  # Thème 4
        elif self.style == 6:
            return "#145A32"  # Thème 5
        elif self.style == 7:
            return "#1C2833"  # Thème 6
        elif self.style == 8:
            return "#7D6608"  # Thème 7
        elif self.style == 9:
            return "#641E16"  # Thème 8
        elif self.style == 10:
            return "#2E86C1"  # Thème 9
        elif self.style == 11:
            return "#784212"  # Thème 10
        elif self.style == 12:
            return "#2C2F33"  # Thème sombre

    @Property(str, constant=True)
    def couleur2(self):  # Endroit blanc
        if self.style in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
            return "#FFFFFF"
        elif self.style == 12:
            return "#404249"

    @Property(str, constant=True)
    def couleur3(self):  # Couleur clair
        if self.style == 1:
            return "#F9C784"
        elif self.style == 2:
            return "#A3CB38"
        elif self.style == 3:
            return "#F39C12"
        elif self.style == 4:
            return "#5DADE2"
        elif self.style == 5:
            return "#D7BDE2"
        elif self.style == 6:
            return "#58D68D"
        elif self.style == 7:
            return "#AED6F1"
        elif self.style == 8:
            return "#F7DC6F"
        elif self.style == 9:
            return "#F5B7B1"
        elif self.style == 10:
            return "#AED6F1"
        elif self.style == 11:
            return "#FAD7A0"
        elif self.style == 12:
            return "#7289DA"

    @Property(str, constant=True)
    def couleur4(self):  # Couleur moyen
        if self.style == 1:
            return "#FCAF58"
        elif self.style == 2:
            return "#78E08F"
        elif self.style == 3:
            return "#E67E22"
        elif self.style == 4:
            return "#3498DB"
        elif self.style == 5:
            return "#AF7AC5"
        elif self.style == 6:
            return "#28B463"
        elif self.style == 7:
            return "#5DADE2"
        elif self.style == 8:
            return "#F4D03F"
        elif self.style == 9:
            return "#EC7063"
        elif self.style == 10:
            return "#5DADE2"
        elif self.style == 11:
            return "#E59866"
        elif self.style == 12:
            return "#5865F2"

    @Property(str, constant=True)
    def couleur5(self):  # Couleur foncé (élevé)
        if self.style == 1:
            return "#FF8C42"
        elif self.style == 2:
            return "#38ADA9"
        elif self.style == 3:
            return "#D35400"
        elif self.style == 4:
            return "#2E86C1"
        elif self.style == 5:
            return "#76448A"
        elif self.style == 6:
            return "#1E8449"
        elif self.style == 7:
            return "#2E86C1"
        elif self.style == 8:
            return "#D4AC0D"
        elif self.style == 9:
            return "#C0392B"
        elif self.style == 10:
            return "#21618C"
        elif self.style == 11:
            return "#CA6F1E"
        elif self.style == 12:
            return "#23272A"

    @Property(str, constant=True)
    def couleur6(self):  # Couleur de contour
        if self.style == 1:
            return "#BC6C25"
        elif self.style == 2:
            return "#1B4F72"
        elif self.style == 3:
            return "#6C3483"
        elif self.style == 4:
            return "#1F618D"
        elif self.style == 5:
            return "#4A235A"
        elif self.style == 6:
            return "#186A3B"
        elif self.style == 7:
            return "#1B4F72"
        elif self.style == 8:
            return "#7E5109"
        elif self.style == 9:
            return "#7B241C"
        elif self.style == 10:
            return "#1B4F72"
        elif self.style == 11:
            return "#6E2C00"
        elif self.style == 12:
            return "#202225"

    @Property(str, constant=True)
    def couleur7(self):  # Couleur très clair (fini)
        if self.style == 1:
            return "#BCBCBC"
        elif self.style == 2:
            return "#D5D8DC"
        elif self.style == 3:
            return "#EBDEF0"
        elif self.style == 4:
            return "#D6EAF8"
        elif self.style == 5:
            return "#F4ECF7"
        elif self.style == 6:
            return "#D4EFDF"
        elif self.style == 7:
            return "#EAF2F8"
        elif self.style == 8:
            return "#FDEBD0"
        elif self.style == 9:
            return "#FADBD8"
        elif self.style == 10:
            return "#D6EAF8"
        elif self.style == 11:
            return "#F6DDCC"
        elif self.style == 12:
            return "#4F545C"
