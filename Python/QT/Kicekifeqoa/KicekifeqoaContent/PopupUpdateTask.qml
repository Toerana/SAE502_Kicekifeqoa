import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

// Fenêtre principale pour le popup de mise à jour d'une tâche
ApplicationWindow {
    // Déclaration des propriétés pour gérer les informations des tâches
    property string taskName: ""            // Nom de la tâche
    property int taskPriority: 0            // Priorité de la tâche (0 = basse, 1 = moyenne, 2 = urgente)
    property string taskTags: ""           // Etiquettes associées à la tâche
    property string taskEndDate: ""        // Date de fin de la tâche
    property bool taskChecked: false       // Statut de la tâche (terminée ou non)

    id: popupupdate
    visible: true // La fenêtre est visible dès l'ouverture
    color: "#00ffffff" // Fond transparent
    width: 420
    height: 220
    title: "Modification de " + taskName   // Titre de la fenêtre principale
    flags: Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint
    minimumWidth: 420      // Largeur minimale fixe
    maximumWidth: 420      // Largeur maximale fixe
    minimumHeight: 220      // Hauteur minimale fixe
    maximumHeight: 220      // Hauteur maximale fixe

    // Signaux utilisés pour transmettre les modifications à d'autres parties du code
    signal updateTaskName(string taskname)
    signal updateTaskPriority(int priority)
    signal updateTag(string tagname)
    signal removeLastTag()
    signal updateEndDate(string enddate)
    signal taskCompleted(int status)
    signal validateUpdateInfo()

    // Rectangle principal du popup, style et disposition
    Rectangle {
        id: background
        x: 0
        y: 0
        width: 420
        height: 220
        color: Colors.couleur1  // Couleur personnalisée pour le fond
        radius: 10             // Coins arrondis
        border.width: 0        // Pas de bordure visible

        // Rectangle intérieur qui contient tous les éléments de la fenêtre
        Rectangle {
            id: rectangle
            x: 10
            y: 10
            width: 400
            height: 200
            visible: true
            radius: 10
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter

            // Liste qui contient les étiquettes associées à la tâche
            ListModel {
                id: tagsListModel
            }

            // Initialisation des tags si la propriété taskTags contient des valeurs
            Component.onCompleted: {
                if (taskTags && taskTags.length > 0) {
                    const tags = taskTags.split(",");
                    tags.forEach(tag => tagsListModel.append({"tag": tag.trim()})); // On ajoute les tags dans la liste
                }
            }

            // Slider pour sélectionner la priorité de la tâche (0, 1, ou 2)
            Slider {
                id: priorityslider
                x: 273
                y: 4
                width: 115
                height: 30
                value: taskPriority
                scale: 0.7
                stepSize: 1
                live: true
                to: 2
                hoverEnabled: true
                enabled: true
                topPadding: 6
            }

            // Bouton pour ajouter un tag
            RoundButton {
                id: tagadd
                x: 173
                y: 65
                width: 20
                height: 20
                text: "+"
                onClicked: {
                    updateTag(tagname.text)  // Envoie le tag ajouté
                    tagsListModel.append({"tag": tagname.text}); // Ajoute le tag à la liste
                    tagname.text = "";  // Réinitialise le champ texte
                }
            }

            // Bouton pour supprimer un tag
            RoundButton {
                id: tagremove
                x: 199
                y: 65
                width: 20
                height: 20
                text: "-"
                onClicked: {
                    if (tagsListModel.count > 0) {
                        tagsListModel.remove(tagsListModel.count - 1)  // Supprime le dernier tag ajouté
                        removeLastTag();  // Signale la suppression du tag
                    }
                }
            }

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
                    updateTaskPriority(priorityslider.value);
                    updateEndDate(enddate.text);
                    taskCompleted(checkBox.checked ? 1 : 0);  // Envoie le statut de la tâche (terminée ou non)
                    validateUpdateInfo();  // Confirme la validation des modifications
                }
            }

            // Texte indiquant le niveau de priorité
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
                                                  : "URGENT" // Affiche "URGENT" si la priorité est 2
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

            // Champ de texte pour entrer le nom de la tâche
            TextField {
                id: taskname
                x: 15
                y: 12
                width: 181
                height: 30
                placeholderText: "Nom de la tâche"
                text: taskName  // Pré-rempli avec le nom de la tâche
            }

            // Champ de texte pour entrer la date de fin de la tâche
            TextField {
                id: enddate
                x: 15
                y: 157
                width: 95
                height: 30
                horizontalAlignment: Text.AlignHCenter
                placeholderText: "--/--/----"
                text: taskEndDate  // Pré-rempli avec la date de fin
            }

            // Texte indiquant le champ de date de fin
            Text {
                id: _text5
                x: 15
                y: 143
                width: 95
                height: 15
                color: Colors.couleur1
                text: "Date de fin :"
                font.pixelSize: 11

                // Case à cocher pour marquer la tâche comme terminée
                CheckBox {
                    id: checkBox
                    x: 263
                    y: -106
                    width: 150
                    height: 30
                    text: "Tâche Terminée"
                    scale: 0.8
                    checked: taskChecked  // Pré-rempli avec le statut de la tâche
                }
            }

            // Zone défilante pour afficher les tags ajoutés à la tâche
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
                            text: model.tag  // Affiche chaque tag dans la liste
                        }
                    }
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
    target: taskHandlerUpdate
    function onValidationSuccess() {
        popupupdate.close();  // Ferme le popup uniquement en cas de succès
    }
}
}
