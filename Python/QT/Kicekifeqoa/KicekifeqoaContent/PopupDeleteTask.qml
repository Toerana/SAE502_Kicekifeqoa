import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
Window {
    property string taskName: ""
    property string taskID: ""

    id: popupdelete
    visible: true
    color: "#00ffffff"
    width: 200
    height: 100
    opacity: 1
    title: "Suppression d'une tâche"   // Titre de la fenêtre principale
    flags: Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint
    minimumWidth: 200      // Largeur minimale fixe
    maximumWidth: 200      // Largeur maximale fixe
    minimumHeight: 100      // Hauteur minimale fixe
    maximumHeight: 100      // Hauteur maximale fixe

    signal taskId(string taskID);
    signal validateDeleteInfo();

    Rectangle {
        id: root
        width: 200
        height: 100
        color: Colors.couleur1
        radius: 5
        Rectangle {
            id: rectangle
            x: 5
            y: 5
            width: 190
            height: 90
            radius: 5
            border.width: 0
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            Text {
                id: _text
            x: 19
            y: 3
            color: Colors.couleur1
            text: "Vous allez supprimer la tâche :"
            font.pixelSize: 12
            anchors.horizontalCenter: parent.horizontalCenter
        }

        RoundButton {
            id: validate
            x: 71
            y: 63
            width: 25
            height: 24
            text: "\u2705"
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 8
            onClicked: {
                taskId(taskID);
                validateDeleteInfo();
                popupdelete.close();
            }
        }

        RoundButton {
            id: cancel
            x: 102
            y: 63
            width: 25
            height: 24
            text: "\u274c"
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 8
            onClicked: {
                popupdelete.close();
            }
        }

        Text {
            id: tasknametext
            x: 19
            y: 25
            width: 158
            height: 25
            color: Colors.couleur1
            text: taskName
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
}