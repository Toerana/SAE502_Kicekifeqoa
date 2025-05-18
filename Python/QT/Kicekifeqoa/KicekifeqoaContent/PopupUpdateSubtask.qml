import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

// Fenêtre principale pour le popup de mise à jour d'une tâche
ApplicationWindow {

    // Déclaration des propriétés pour gérer les informations des tâches
    property string taskName: ""            // Nom de la tâche
    property string taskEndDate: ""        // Date de fin de la tâche
    property bool taskChecked: false       // Statut de la tâche (terminée ou non)

    id: popupupdate
    visible: true // La fenêtre est visible dès l'ouverture
    color: "#00ffffff" // Fond transparent
    title: "Modification de "+ taskName    // Titre de la fenêtre principale
    width: 420
    height: 150
    flags: Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint
    minimumWidth: 420      // Largeur minimale fixe
    maximumWidth: 420      // Largeur maximale fixe
    minimumHeight: 150      // Hauteur minimale fixe
    maximumHeight: 150      // Hauteur maximale fixe


    // Signaux utilisés pour transmettre les modifications à d'autres parties du code
    signal updateTaskName(string taskname)
    signal updateEndDate(string enddate)
    signal taskCompleted(int status)
    signal validateUpdateInfo()

    // Rectangle principal du popup, style et disposition
    Rectangle {
        id: background
        x: 0
        y: 0
        width: 420
        height: 150
        color: Colors.couleur1  // Couleur personnalisée pour le fond
        radius: 10             // Coins arrondis
        border.width: 0        // Pas de bordure visible

        // Rectangle intérieur qui contient tous les éléments de la fenêtre
        Rectangle {
            id: rectangle
            x: 10
            y: 10
            width: 400
            height: 130
            visible: true
            radius: 10
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter


            // Bouton pour valider la mise à jour de la tâche
            RoundButton {
                id: validate
                x: 306
                y: 152
                text: "\u2713"  // Symbole de coche
                anchors.right: close.left
                anchors.top: close.top
                anchors.bottom: parent.bottom
                anchors.rightMargin: 6
                anchors.bottomMargin: 8
                checkable: false
                icon.cache: true
                font.pointSize: 15
                onClicked: {
                    // Envoie des modifications
                    updateTaskName(taskname.text);
                    updateEndDate(enddate.text);
                    taskCompleted(checkBox.checked ? 1 : 0);  // Envoie le statut de la tâche (terminée ou non)
                    validateUpdateInfo();  // Confirme la validation des modifications
                }
            }

            // Champ de texte pour entrer le nom de la tâche
            TextField {
                id: taskname
                x: 15
                y: 12
                width: 181
                height: 30
                placeholderText: qsTr("Nom de la tâche")
                text: taskName  // Pré-rempli avec le nom de la tâche
            }

            // Champ de texte pour entrer la date de fin de la tâche
            TextField {
                id: enddate
                x: 15
                y: 94
                width: 95
                height: 30
                horizontalAlignment: Text.AlignHCenter
                placeholderText: qsTr("--/--/----")
                text: taskEndDate  // Pré-rempli avec la date de fin
            }

            // Texte indiquant le champ de date de fin
            Text {
                id: _text5
                x: 15
                y: 80
                width: 95
                height: 15
                color: Colors.couleur1
                text: qsTr("Date de fin :")
                font.pixelSize: 11

                // Case à cocher pour marquer la tâche comme terminée
                CheckBox {
                    id: checkBox
                    x: 263
                    y: -72
                    width: 150
                    height: 30
                    text: qsTr("Tâche Terminée")
                    scale: 0.8
                    checked: taskChecked  // Pré-rempli avec le statut de la tâche
                }
            }

            // Bouton pour fermer le popup sans valider
            RoundButton {
                id: close
                x: 352
                y: 152
                text: "X"  // Symbole de fermeture
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.rightMargin: 8
                anchors.topMargin: 6
                anchors.bottomMargin: 8
                font.pointSize: 15
                onClicked: {
                    popupupdate.close();  // Ferme le popup
                }
            }
        }
    }
    Connections {
        target: subtaskHandlerUpdate
        function onValidationSuccess() {
            popupupdate.close();  // Ferme le popup uniquement en cas de succès
        }
    }
}