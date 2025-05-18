import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: popupcreate
    visible: true
    color: "#00ffffff"
    width: 420
    height: 220
    title: "Ajout d'une tâche"    // Titre de la fenêtre principale
    flags: Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint
    minimumWidth: 420      // Largeur minimale fixe
    maximumWidth: 420      // Largeur maximale fixe
    minimumHeight: 220      // Hauteur minimale fixe
    maximumHeight: 220      // Hauteur maximale fixe

    signal addTaskName(string taskname)
    signal addTaskPriority(int priority)
    signal addTag(string tagname)
    signal removeLastTag()
    signal addEndDate(string enddate)
    signal taskCompleted(int status)
    signal validateInfo()

    Rectangle {
        id: background
        x: 0
        y: 0
        width: 420
        height: 220
        color: Colors.couleur1
        radius: 5
        border.width: 0

        Rectangle {
        id: rectangle
        x: 10
        y: 10
        width: 400
        height: 200
        visible: true
        radius: 5
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: 0
        anchors.horizontalCenterOffset: 0
        anchors.horizontalCenter: parent.horizontalCenter
        ListModel {
        id: tagsListModel
    }


    Slider {
        id: priorityslider
        x: 273
        y: 4
        width: 115
        height: 30
        value: 0
        scale: 0.7
        stepSize: 1
        live: true
        to: 2
        hoverEnabled: true
        enabled: true
        topPadding: 6
    }

    RoundButton {
        id: tagadd
        x: 173
        y: 65
        width: 20
        height: 20
        text: "+"
        highlighted: false
        flat: false
        icon.color: Colors.couleur1
        onClicked: {
            addTag(tagname.text)
            tagsListModel.append({"tag": tagname.text});
            tagname.text = "";
        }
    }

    RoundButton {
        id: tagremove
        x: 199
        y: 65
        width: 20
        height: 20
        text: "-"
        onClicked: {
            if (tagsListModel.count > 0) {
                tagsListModel.remove(tagsListModel.count - 1)
                removeLastTag();
            }
        }
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
            addTaskPriority(priorityslider.value);
            addEndDate(enddate.text);
            taskCompleted(checkBox.checked ? 1 : 0);
            validateInfo();
        }
    }

    Text {
        id: prioritytext
        x: 277
        y: 26
        width: 115
        height: 16
        color: Colors.couleur1
        font.pixelSize: 12
        horizontalAlignment: Text.AlignHCenter
        text: priorityslider.value === 0 ? "Priorité basse"
             : priorityslider.value === 1 ? "Priorité moyenne"
                                          : "URGENT"
        anchors.right: parent.right
             anchors.rightMargin: 8
    }

    TextField {
        id: tagname
        x: 15
        y: 63
        width: 155
        height: 30
        placeholderText: "Etiquettes"
    }

    TextField {
        id: taskname
        x: 15
        y: 12
        width: 181
        height: 30
        placeholderText: "Nom de la tâche"
    }

    TextField {
        id: enddate
        x: 15
        y: 157
        width: 95
        height: 30
        horizontalAlignment: Text.AlignHCenter
        placeholderText: "--/--/----"
    }

    Text {
        id: _text5
        x: 15
        y: 143
        width: 95
        height: 15
        color: Colors.couleur1
        text: "Date de fin :"
        font.pixelSize: 11

        CheckBox {
            id: checkBox
            x: 263
            y: -106
            width: 150
            height: 30
            text: "Tache Terminée"
            scale: 0.8
            checkState: Qt.Unchecked
        }
    }


    Flickable {
        id: tagsFlickable
        x: 227
        y: 65
        width: 150
        height: 30
        contentWidth: tagsRow.width
        contentHeight: tagsRow.height
        clip: true

        Row {
            id: tagsRow
            spacing: 10
            Repeater {
                model: tagsListModel
                delegate: Text {
                    text: model.tag
                }
            }
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
// Connexion pour fermer le popup après une validation réussie
Connections {
    target: taskHandlerCreate
    function onValidationSuccess() {
        popupcreate.close();  // Ferme le popup uniquement en cas de succès
    }
}
}