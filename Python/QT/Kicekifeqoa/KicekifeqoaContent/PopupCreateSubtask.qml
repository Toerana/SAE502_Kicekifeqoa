import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Window {
    id: popupcreate
    visible: true
    color: "#00ffffff"
    width: 420
    height: 150
    title: "Ajout d'une sous-tâche"    // Titre de la fenêtre principale
    flags: Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint
    minimumWidth: 420      // Largeur minimale fixe
    maximumWidth: 420      // Largeur maximale fixe
    minimumHeight: 150      // Hauteur minimale fixe
    maximumHeight: 150      // Hauteur maximale fixe

    signal addTaskName(string taskname)
    signal addEndDate(string enddate)
    signal taskCompleted(int status)
    signal validateInfo()

    Rectangle {
        id: background
        x: 0
        y: 0
        width: 420
        height: 150
        color: Colors.couleur1
        radius: 5
        border.width: 0

        Rectangle {
        id: rectangle
        x: 10
        y: 10
        width: 400
        height: 130
        visible: true
        radius: 5
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: 0
        anchors.horizontalCenterOffset: 0
        anchors.horizontalCenter: parent.horizontalCenter
        ListModel {
            id: tagsListModel
        }

        ListModel {
            id: usersListModel
        }

        RoundButton {
            id: validate
            x: 306
            y: 152
            text: "\u2713"
            anchors.verticalCenter: close.verticalCenter
            anchors.right: close.left
            anchors.top: close.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: 6
            anchors.bottomMargin: 8
            checkable: false
            icon.cache: true
            font.pointSize: 15
            onClicked: {
                addTaskName(taskname.text);
                addEndDate(enddate.text);
                taskCompleted(checkBox.checked ? 1 : 0);
                validateInfo();
            }
        }

        TextField {
            id: taskname
            x: 15
            y: 12
            width: 181
            height: 30
            placeholderText: "Nom de la sous-tâche"
        }

        TextField {
            id: enddate
            x: 15
            y: 94
            width: 95
            height: 30
            horizontalAlignment: Text.AlignHCenter
            placeholderText: "--/--/----"
        }

        Text {
            id: _text5
            x: 15
            y: 80
            width: 95
            height: 15
            color: Colors.couleur1
            text: "Date de fin :"
            font.pixelSize: 11

            CheckBox {
                id: checkBox
                x: 263
                y: -72
                width: 150
                height: 30
                text: "Tache Terminée"
                scale: 0.8
                checkState: Qt.Unchecked
            }
        }



        RoundButton {
            id: close
            x: 352
            y: 152
            text: "X"
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.rightMargin: 8
            anchors.topMargin: 6
            anchors.bottomMargin: 8
            font.pointSize: 15
            onClicked: {
                popupcreate.close();
            }
        }
    }
    }
    Connections {
        target: subtaskHandlerCreate
        function onValidationSuccess() {
            popupcreate.close();  // Ferme le popup uniquement en cas de succès
        }
    }
}