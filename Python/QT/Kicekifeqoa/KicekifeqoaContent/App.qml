import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15

// Déclaration de la fenêtre principale
Window {

    property int userId: Qt.application.userId

    id: root
    visible: true
    color: Colors.couleur1  // Utilise une couleur définie par la palette personnalisée
    width: 1000
    height: 800
    title: "Kicekifeqoa - " + userId    // Titre de la fenêtre principale
    minimumWidth: 1000      // Largeur minimale fixe
    maximumWidth: 1000      // Largeur maximale fixe
    minimumHeight: 800      // Hauteur minimale fixe
    maximumHeight: 800      // Hauteur maximale fixe

    // Propriétés pour stocker les informations de la tâche sélectionnée
    property string selectedTaskName: ""
    property string selectedTaskId: ""
    property var selectedDelegate: null

    // Rectangle principal de fond pour l'application
    Rectangle {
        id: rectangle
        x: 26
        y: 22
        width: 955
        height: 754
        color: Colors.couleur2
        radius: 5
        border.color: Colors.couleur6
        border.width: 0
        layer.enabled: false

        // Logo de l'application
        Image {
            id: image
            x: 12
            y: 11
            width: 100
            height: 96
            source: "images/logo.png"
            fillMode: Image.PreserveAspectFit
        }
    }

    // Disposition en grille pour afficher les colonnes de tâches
    GridLayout {
        anchors.fill: parent
        anchors.leftMargin: 39
        anchors.rightMargin: 32
        anchors.topMargin: 142
        anchors.bottomMargin: 34
        columns: 4                // Quatre colonnes pour les priorités
        columnSpacing: 10         // Espacement entre les colonnes

        // Première colonne - tâches avec priorité élevée
        Rectangle {
            id: taskArea
            color: Colors.couleur5
            radius: 5
            border.width: 0
            border.color: Colors.couleur6
            width: 225
            Layout.fillHeight: true

            // Modèle pour les tâches de cette colonne
            ListModel {
                id: taskModel
            }

            // Action exécutée au chargement du composant pour récupérer les tâches
            Component.onCompleted: {
                taskHandlerBackend.fetchTasks(root.userId);
            }

            // Liste pour afficher les tâches
            ListView {
                id: taskListView
                model: taskModel
                anchors.fill: parent
                anchors.topMargin: 51
                anchors.bottomMargin: 12.5
                spacing: 0

                // Délégué pour chaque élément de la liste (tâche)
                delegate: Column {
                    spacing: 0
                    anchors.horizontalCenter: parent.horizontalCenter

                    Rectangle {
                        id: root
                        width: 200
                        height: model.name.startsWith("↳") ? 60 : 90  // Hauteur différente si c'est une sous-tâche
                        radius: 5
                        color: selected ? "#dcdcdc" : "#eeeeee" // Change de couleur si sélectionné
                        border.width: 2
                        border.color: Colors.couleur2

                        // Propriété pour indiquer si l'élément est sélectionné
                        property bool selected: false

                        // Zone interactive pour sélectionner/désélectionner la tâche
                        MouseArea {
                            id: mouseArea
                            anchors.fill: parent
                            onClicked: {
                                if (root.selected) {
                                    root.selected = false
                                    selectedDelegate = null
                                    selectedTaskId = ""
                                    selectedTaskName = ""

                                    console.log("Aucune tâche sélectionnée")
                                } else {
                                    if (selectedDelegate !== null) {
                                        selectedDelegate.selected = false
                                    }

                                    root.selected = true
                                    selectedDelegate = root

                                    selectedTaskId = taskid.text
                                    selectedTaskName = taskname.text

                                    console.log("Tâche sélectionnée ID:", selectedTaskId)
                                    console.log("Tâche sélectionnée Nom:", selectedTaskName)
                                }
                            }
                        }

                        // Texte affichant le nom de la tâche
                        Text {
                            id: taskname
                            x: 4
                            y: 6
                            text: model.name
                            font.pixelSize: model.name.startsWith("↳") ? 15 : 17
                            font.styleName: "Gras"
                        }

                        // Texte affichant l'ID de la tâche
                        Text {
                            id: taskid
                            x: 150
                            y: 25
                            color: Colors.couleur7
                            text: model.id_task
                            font.pixelSize: 17
                            font.styleName: "Gras"
                        }

                        // Texte affichant la date d'échéance de la tâche
                        Text {
                            id: enddate
                            x: 4
                            y: model.name.startsWith("↳") ? 30 : 57
                            text: model.end_date
                            font.pixelSize: 12
                        }

                        // Checkbox pour marquer la tâche comme terminée
                        CheckBox {
                            id: checked
                            x: 152
                            y: 2
                            width: 60
                            height: 30
                            text: "Fini ?"
                            enabled: false
                            checked: model.checked === 1
                        }

                        // Texte pour afficher l'indicateur de priorité
                        Text {
                            id: priority
                            x: 65
                            y: 56
                            font.pixelSize: model.name.startsWith("↳") ? 1 : 12
                            text: {
                                if (model.priority === 1) {
                                    return "🕐";
                                } else if (model.priority === 2) {
                                    return "⚠️";
                                } else {
                                    return "";
                                }
                            }
                        }

                        // Texte pour afficher les tags associés à la tâche
                        Text {
                            id: tag
                            x: 4
                            y: 35
                            text: model.tag
                            font.pixelSize: 12
                        }
                    }

                    // Ajoute un espacement supplémentaire après les sous-tâches si l'élément suivant est une tâche principale
                    Item {
                        width: 1
                        height: (index < taskModel.count - 1 && !taskModel.get(index + 1).name.startsWith("↳")) ? 5 : 1
                    }
                }
            }
            // Bouton pour ajouter une tâche ou une sous-tâche
            RoundButton {
                id: addButton
                x: 866
                y: -101
                text: "+"
                anchors.margins: 10
                onClicked: {
                    // Vérifie si une tâche est sélectionnée pour ajouter une sous-tâche
                    if (selectedTaskId !== "") {
                        subtaskHandlerCreate.define_parent_task_id(selectedTaskId);
                        var component = Qt.createComponent("PopupCreateSubtask.qml");

                        // Crée le composant PopupCreateSubtask si le chargement est réussi
                        if (component.status === Component.Ready) {
                            var PopupCreateSubtask = component.createObject(parent);

                            if (PopupCreateSubtask === null) {
                                console.error("Erreur lors de la création de PopupCreateSubTask");
                            } else {
                                if (taskHandlerCreate) {
                                    // Connexions pour transmettre les données à subtaskHandlerCreate
                                    PopupCreateSubtask.addTaskName.connect(subtaskHandlerCreate.add_task_name);
                                    PopupCreateSubtask.addEndDate.connect(subtaskHandlerCreate.add_end_date);
                                    PopupCreateSubtask.taskCompleted.connect(subtaskHandlerCreate.task_completed);
                                    PopupCreateSubtask.validateInfo.connect(function () {
                                        subtaskHandlerCreate.validate_info();
                                        taskHandlerBackend.fetchTasks(root.userId);
                                    });
                                } else {
                                    console.error("Erreur : TaskHandler est introuvable.");
                                }
                            }
                        } else {
                            console.error("Erreur lors du chargement de PopupCreateSubtask.qml");
                        }
                    } else {
                        // Si aucune tâche n'est sélectionnée, crée une nouvelle tâche
                        var component = Qt.createComponent("PopupCreateTask.qml");

                        if (component.status === Component.Ready) {
                            var PopupCreateTask = component.createObject(parent);

                            if (PopupCreateTask === null) {
                                console.error("Erreur lors de la création de PopupCreateTask");
                            } else {
                                if (taskHandlerCreate) {
                                    // Connexions pour transmettre les données à taskHandlerCreate
                                    PopupCreateTask.addTaskName.connect(taskHandlerCreate.add_task_name);
                                    PopupCreateTask.addTaskPriority.connect(taskHandlerCreate.add_task_priority);
                                    PopupCreateTask.addTag.connect(taskHandlerCreate.add_tag);
                                    PopupCreateTask.removeLastTag.connect(taskHandlerCreate.remove_last_tag);
                                    PopupCreateTask.addEndDate.connect(taskHandlerCreate.add_end_date);
                                    PopupCreateTask.taskCompleted.connect(taskHandlerCreate.task_completed);
                                    PopupCreateTask.validateInfo.connect(function () {
                                        taskHandlerCreate.validate_info();
                                        taskHandlerBackend.fetchTasks(root.userId);
                                    });
                                } else {
                                    console.error("Erreur : TaskHandler est introuvable.");
                                }
                            }
                        } else {
                            console.error("Erreur lors du chargement de PopupCreateTask.qml");
                        }
                    }
                }
            }

            // Connexion pour mettre à jour le modèle avec les tâches récupérées du backend
            Connections {
                target: taskHandlerBackend
                onTasksFetchedPriority2: function (tasks) {
                    taskModel.clear();
                    for (var i = 0; i < tasks.length; i++) {
                        taskModel.append({
                            "id_task": tasks[i].id_task,
                            "name": tasks[i].name,
                            "end_date": tasks[i].end_date,
                            "checked": tasks[i].checked,
                            "priority": tasks[i].priority,
                            "tag": tasks[i].tag
                        });
                    }
                }
            }

            // Bouton pour modifier une tâche sélectionnée
            RoundButton {
                id: modify
                x: 836
                y: -71
                text: "🖌️"
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 10
                anchors.rightMargin: -651
                anchors.bottomMargin: 655
                onClicked: {
                    if (selectedTaskId !== "") {
                        var ids = selectedTaskId.split("."); // Divise l'ID par le séparateur "."
                        if (ids.length === 1) {
                            // Cas où l'ID est sous la forme "XX"
                            taskHandlerUpdate.fetch_task_by_id(selectedTaskId);
                        } else if (ids.length === 2) {
                            // Cas où l'ID est sous la forme "YY.XX"
                            subtaskHandlerUpdate.fetch_task_by_id(ids[0]); // Utilise "YY"
                        } else {
                            console.error("Erreur : Format de l'ID non valide.");
                        }
                    } else {
                        console.error("Erreur : Aucune tâche sélectionnée.");
                    }
                }

                // Connexion pour afficher le popup de modification avec les données récupérées
                Connections {
                    target: taskHandlerUpdate
                    onTaskFetched: function (taskData) {
                        var component = Qt.createComponent("PopupUpdateTask.qml");

                        if (component.status === Component.Ready) {
                            var PopupUpdateTask = component.createObject(root, {
                                "taskName": taskData.task_name,
                                "taskPriority": taskData.task_priority,
                                "taskTags": taskData.tag ? taskData.tag.join(", ") : "",
                                "taskEndDate": taskData.end_date,
                                "taskChecked": taskData.checked
                            });

                            if (PopupUpdateTask === null) {
                                console.error("Erreur lors de la création de PopupUpdateTask");
                            } else {
                                if (taskHandlerUpdate) {
                                    // Connexions pour transmettre les données à taskHandlerUpdate
                                    PopupUpdateTask.updateTaskName.connect(taskHandlerUpdate.update_task_name);
                                    PopupUpdateTask.updateTaskPriority.connect(taskHandlerUpdate.update_task_priority);
                                    PopupUpdateTask.updateTag.connect(taskHandlerUpdate.add_tag);
                                    PopupUpdateTask.removeLastTag.connect(taskHandlerUpdate.remove_last_tag);
                                    PopupUpdateTask.updateEndDate.connect(taskHandlerUpdate.update_end_date);
                                    PopupUpdateTask.taskCompleted.connect(taskHandlerUpdate.task_completed);
                                    PopupUpdateTask.validateUpdateInfo.connect(function () {
                                        taskHandlerUpdate.validate_update_info();
                                        taskHandlerBackend.fetchTasks(root.userId);
                                    });
                                } else {
                                    console.error("Erreur : TaskHandler est introuvable.");
                                }
                            }
                        } else {
                            console.error("Erreur lors du chargement de PopupUpdateTask.qml");
                        }
                    }
                }

                // Connexion pour afficher le popup de modification de sous-tache avec les données récupérées
                Connections {
                    target: subtaskHandlerUpdate
                    onTaskFetched: function (taskData) {
                        var component = Qt.createComponent("PopupUpdateSubtask.qml");

                        if (component.status === Component.Ready) {
                            var PopupUpdateSubtask = component.createObject(root, {
                                "taskName": taskData.task_name,
                                "taskEndDate": taskData.end_date,
                                "taskChecked": taskData.checked
                            });

                            if (PopupUpdateSubtask === null) {
                                console.error("Erreur lors de la création de PopupUpdateTask");
                            } else {
                                if (subtaskHandlerUpdate) {
                                    // Connexions pour transmettre les données à taskHandlerUpdate
                                    PopupUpdateSubtask.updateTaskName.connect(subtaskHandlerUpdate.update_task_name);
                                    PopupUpdateSubtask.updateEndDate.connect(subtaskHandlerUpdate.update_end_date);
                                    PopupUpdateSubtask.taskCompleted.connect(subtaskHandlerUpdate.task_completed);
                                    PopupUpdateSubtask.validateUpdateInfo.connect(function () {
                                        subtaskHandlerUpdate.validate_update_info();
                                        taskHandlerBackend.fetchTasks(root.userId);
                                    });

                                    if (PopupUpdateTask === null) {
                                        console.error("Erreur lors de la création de PopupUpdateTask");
                                    } else {
                                        // Assigner les signaux pour gérer les mises à jour
                                        if (taskHandlerUpdate) {
                                            PopupUpdateTask.updateTaskName.connect(taskHandlerUpdate.update_task_name);
                                            PopupUpdateTask.updateTaskPriority.connect(taskHandlerUpdate.update_task_priority);
                                            PopupUpdateTask.updateTag.connect(taskHandlerUpdate.add_tag);
                                            PopupUpdateTask.removeLastTag.connect(taskHandlerUpdate.remove_last_tag);
                                            PopupUpdateTask.updateEndDate.connect(taskHandlerUpdate.update_end_date);
                                            PopupUpdateTask.taskCompleted.connect(taskHandlerUpdate.task_completed);
                                            PopupUpdateTask.validateUpdateInfo.connect(function () {
                                                taskHandlerUpdate.validate_update_info();
                                                taskHandlerBackend.fetchTasks(root.userId);
                                            });
                                        } else {
                                            console.error("Erreur : TaskHandler est introuvable.");
                                        }
                                    }
                                } else {
                                    console.error("Erreur : TaskHandler est introuvable.");
                                }
                            }
                        } else {
                            console.error("Erreur lors du chargement de PopupUpdateTask.qml");
                        }
                    }
                }
            }

            RoundButton {
                id: remove
                x: 884
                y: -71
                text: "🗑️"
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 10
                anchors.rightMargin: -699
                anchors.bottomMargin: 655
                onClicked: {
                    if (selectedTaskName !== "" && selectedTaskId !== "") {
                        var component = Qt.createComponent("PopupDeleteTask.qml");

                        if (component.status === Component.Ready) {
                            var PopupDeleteTask = component.createObject(parent, {
                                "taskName": selectedTaskName,
                                "taskID": selectedTaskId
                            });

                            if (PopupDeleteTask === null) {
                                console.error("Erreur lors de la création de PopupDeleteTask");
                            } else {
                                if (taskHandlerDelete) {
                                    // Connexions pour transmettre les données à taskHandlerUpdate
                                    PopupDeleteTask.taskId.connect(taskHandlerDelete.set_task_id);
                                    PopupDeleteTask.validateDeleteInfo.connect(function() {
                                        taskHandlerDelete.validate_delete_info();
                                        taskHandlerBackend.fetchTasks(root.userId);
                                    });
                                    selectedTaskId = ""
                                    selectedTaskName = ""
                                } else {
                                    console.error("Erreur : taskHandlerDelete n'est pas initialisé");
                                }
                            }
                        } else {
                            console.error("Erreur lors du chargement de PopupDeleteTask.qml");
                        }
                    } else {
                        console.error("Erreur : Aucune tâche sélectionnée.");
                    }
                }
            }
        }

        // Deuxième colonne - tâches avec priorité moyenne
        Rectangle {
            id: taskArea2
            color: Colors.couleur4  // Couleur de fond pour la deuxième colonne
            radius: 5
            border.width: 0
            border.color: Colors.couleur6
            width: 225
            Layout.fillHeight: true  // La hauteur de l'élément s'adapte à la hauteur du parent

            // Modèle pour stocker les tâches de priorité moyenne
            ListModel {
                id: taskModel2
            }

            // Chargement des tâches de priorité moyenne lorsque le composant est créé
            Component.onCompleted: {
                taskHandlerBackend.fetchTasks(root.userId)
            }

            // Liste pour afficher les tâches du modèle
            ListView {
                id: taskListView2
                model: taskModel2
                anchors.fill: parent
                anchors.topMargin: 51
                anchors.bottomMargin: 12.5
                spacing: 0

                // Délégué pour afficher chaque tâche dans la liste
                delegate: Column {
                    spacing: 0
                    anchors.horizontalCenter: parent.horizontalCenter

                    // Rectangle pour chaque tâche
                    Rectangle {
                        id: root2
                        width: 200
                        height: model.name.startsWith("↳") ? 60 : 90  // Hauteur ajustée si c'est une sous-tâche
                        radius: 5
                        color: selected ? "#dcdcdc" : "#eeeeee"  // Couleur différente si l'élément est sélectionné
                        border.width: 2
                        border.color: Colors.couleur2

                        // Propriété pour savoir si l'élément est sélectionné
                        property bool selected: false

                        // Zone cliquable pour sélectionner/désélectionner une tâche
                        MouseArea {
                            id: mouseArea2
                            anchors.fill: parent
                            onClicked: {
                                if (root2.selected) {
                                    root2.selected = false
                                    selectedDelegate = null
                                    selectedTaskId = ""
                                    selectedTaskName = ""
                                    console.log("Aucune tâche sélectionnée")
                                } else {
                                    if (selectedDelegate !== null) {
                                        selectedDelegate.selected = false
                                    }
                                    root2.selected = true
                                    selectedDelegate = root2
                                    selectedTaskId = taskid2.text
                                    selectedTaskName = taskname2.text
                                    console.log("Tâche sélectionnée ID:", selectedTaskId)
                                    console.log("Tâche sélectionnée Nom:", selectedTaskName)
                                }
                            }
                        }

                        // Nom de la tâche
                        Text {
                            id: taskname2
                            x: 4
                            y: 6
                            text: model.name
                            font.pixelSize: model.name.startsWith("↳") ? 15 : 17
                            font.styleName: "Gras"
                        }

                        // ID de la tâche
                        Text {
                            id: taskid2
                            x: 150
                            y: 25
                            color: Colors.couleur7
                            text: model.id_task
                            font.pixelSize: 17
                            font.styleName: "Gras"
                        }

                        // Date d'échéance de la tâche
                        Text {
                            id: enddate2
                            x: 4
                            y: model.name.startsWith("↳") ? 30 : 57
                            text: model.end_date
                            font.pixelSize: 12
                        }

                        // Checkbox pour indiquer si la tâche est terminée
                        CheckBox {
                            id: checked2
                            x: 152
                            y: 2
                            width: 60
                            height: 30
                            text: "Fini ?"
                            enabled: false
                            checked: model.checked === 1
                        }

                        // Indicateur de priorité avec des icônes
                        Text {
                            id: priority2
                            x: 65
                            y: 56
                            font.pixelSize: model.name.startsWith("↳") ? 1 : 12
                            text: {
                                if (model.priority === 1) {
                                    return "🕐";
                                } else if (model.priority === 2) {
                                    return "⚠️";
                                } else {
                                    return "";
                                }
                            }
                        }

                        // Tags associés à la tâche
                        Text {
                            id: tag2
                            x: 4
                            y: 35
                            text: model.tag
                            font.pixelSize: 12
                        }
                    }

                    // Espacement supplémentaire après les sous-tâches si l'élément suivant est une tâche principale
                    Item {
                        width: 1
                        height: (index < taskModel2.count - 1 && !taskModel2.get(index + 1).name.startsWith("↳")) ? 5 : 1
                    }
                }
            }

            // Connexion pour récupérer les tâches de priorité moyenne depuis le backend
            Connections {
                target: taskHandlerBackend
                onTasksFetchedPriority1: function (tasks) {
                    taskModel2.clear();  // Efface les anciennes tâches avant de charger les nouvelles
                    for (var i = 0; i < tasks.length; i++) {
                        taskModel2.append({  // Ajoute chaque tâche au modèle
                            "id_task": tasks[i].id_task,
                            "name": tasks[i].name,
                            "end_date": tasks[i].end_date,
                            "checked": tasks[i].checked,
                            "priority": tasks[i].priority,
                            "tag": tasks[i].tag
                        });
                    }
                }
            }
        }

        // Troisième colonne - tâches avec priorité basse
        Rectangle {
            id: taskArea3
            color: Colors.couleur3  // Couleur de fond pour la troisième colonne (priorité basse)
            radius: 5
            border.width: 0
            border.color: Colors.couleur6
            width: 225
            Layout.fillHeight: true  // La hauteur s'adapte à celle du parent

            // Modèle pour stocker les tâches de priorité basse
            ListModel {
                id: taskModel3
            }

            // Chargement des tâches de priorité basse lorsque le composant est créé
            Component.onCompleted: {
                taskHandlerBackend.fetchTasks(root.userId)
            }

            // Liste pour afficher les tâches du modèle
            ListView {
                id: taskListView3
                model: taskModel3
                anchors.fill: parent
                anchors.topMargin: 51
                anchors.bottomMargin: 12.5
                spacing: 0

                // Délégué pour afficher chaque tâche
                delegate: Column {
                    spacing: 0
                    anchors.horizontalCenter: parent.horizontalCenter

                    // Rectangle pour chaque tâche affichée
                    Rectangle {
                        id: root3
                        width: 200
                        height: model.name.startsWith("↳") ? 60 : 90  // Hauteur ajustée pour les sous-tâches
                        radius: 5
                        color: selected ? "#d0d0d0" : "#eeeeee"  // Change de couleur si l'élément est sélectionné
                        border.width: 2
                        border.color: Colors.couleur2

                        // Propriété pour savoir si l'élément est sélectionné
                        property bool selected: false

                        // Zone cliquable pour sélectionner/désélectionner une tâche
                        MouseArea {
                            id: mouseArea3
                            anchors.fill: parent
                            onClicked: {
                                if (root3.selected) {
                                    root3.selected = false
                                    selectedDelegate = null
                                    selectedTaskId = ""
                                    selectedTaskName = ""
                                    console.log("Aucune tâche sélectionnée")
                                } else {
                                    if (selectedDelegate !== null) {
                                        selectedDelegate.selected = false
                                    }
                                    root3.selected = true
                                    selectedDelegate = root3
                                    selectedTaskId = taskid3.text
                                    selectedTaskName = taskname3.text
                                    console.log("Tâche sélectionnée ID:", selectedTaskId)
                                    console.log("Tâche sélectionnée Nom:", selectedTaskName)
                                }
                            }
                        }

                        // Texte affichant le nom de la tâche
                        Text {
                            id: taskname3
                            x: 4
                            y: 6
                            text: model.name
                            font.pixelSize: model.name.startsWith("↳") ? 15 : 17
                            font.styleName: "Gras"
                        }

                        // Texte affichant l'ID de la tâche
                        Text {
                            id: taskid3
                            x: 150
                            y: 25
                            color: Colors.couleur7
                            text: model.id_task
                            font.pixelSize: 17
                            font.styleName: "Gras"
                        }

                        // Texte affichant la date d'échéance
                        Text {
                            id: enddate3
                            x: 4
                            y: model.name.startsWith("↳") ? 30 : 57
                            text: model.end_date
                            font.pixelSize: 12
                        }

                        // Checkbox pour indiquer si la tâche est terminée
                        CheckBox {
                            id: checked3
                            x: 152
                            y: 2
                            width: 60
                            height: 30
                            text: "Fini ?"
                            enabled: false
                            checked: model.checked === 1
                        }

                        // Texte affichant l'indicateur de priorité
                        Text {
                            id: priority3
                            x: 65
                            y: 56
                            font.pixelSize: model.name.startsWith("↳") ? 1 : 12
                            text: {
                                if (model.priority === 1) {
                                    return "🕐";
                                } else if (model.priority === 2) {
                                    return "⚠️";
                                } else {
                                    return "";
                                }
                            }
                        }

                        // Texte affichant les tags associés à la tâche
                        Text {
                            id: tag3
                            x: 4
                            y: 35
                            text: model.tag
                            font.pixelSize: 12
                        }
                    }

                    // Espacement après chaque tâche pour les séparer visuellement
                    Item {
                        width: 1
                        height: (index < taskModel3.count - 1 && !taskModel3.get(index + 1).name.startsWith("↳")) ? 5 : 1
                    }
                }
            }

            // Connexion au backend pour récupérer les tâches de priorité basse
            Connections {
                target: taskHandlerBackend
                onTasksFetchedPriority0: function (tasks) {
                    taskModel3.clear();  // Efface les anciennes tâches avant d'ajouter les nouvelles
                    for (var i = 0; i < tasks.length; i++) {
                        taskModel3.append({
                            "id_task": tasks[i].id_task,
                            "name": tasks[i].name,
                            "end_date": tasks[i].end_date,
                            "checked": tasks[i].checked,
                            "priority": tasks[i].priority,
                            "tag": tasks[i].tag
                        });
                    }
                }
            }
        }

        // Quatrième colonne - tâches fini
        Rectangle {
            id: taskArea4
            color: "#eeeeee"
            radius: 5
            border.width: 2
            border.color: "#afafaf"
            width: 225
            Layout.fillHeight: true

            ListModel {
                id: taskModel4
            }

            Component.onCompleted: {
                taskHandlerBackend.fetchTasks(root.userId)
            }

            ListView {
                id: taskListView4
                model: taskModel4
                anchors.fill: parent
                anchors.topMargin: 51
                anchors.bottomMargin: 12.5
                spacing: 0

                delegate: Column {
                    spacing: 0
                    anchors.horizontalCenter: parent.horizontalCenter

                    Rectangle {
                        id: root4
                        width: 200
                        height: model.name.startsWith("↳") ? 60 : 90
                        radius: 5
                        color: selected ? "#dcdcdc" : "#eeeeee"
                        border.width: 2
                        border.color: Colors.couleur2

                        property bool selected: false

                        MouseArea {
                            id: mouseArea4
                            anchors.fill: parent
                            onClicked: {
                                if (root4.selected) {
                                    root4.selected = false
                                    selectedDelegate = null
                                    selectedTaskId = ""
                                    selectedTaskName = ""

                                    console.log("Aucune tâche sélectionnée")
                                } else {
                                    if (selectedDelegate !== null) {
                                        selectedDelegate.selected = false
                                    }

                                    root4.selected = true
                                    selectedDelegate = root4

                                    selectedTaskId = taskid4.text
                                    selectedTaskName = taskname4.text

                                    console.log("Tâche sélectionnée ID:", selectedTaskId)
                                    console.log("Tâche sélectionnée Nom:", selectedTaskName)
                                }
                            }
                        }

                        Text {
                            id: taskname4
                            x: 4
                            y: 6
                            text: model.name
                            font.pixelSize: model.name.startsWith("↳") ? 15 : 17
                            font.styleName: "Gras"
                        }

                        Text {
                            id: taskid4
                            x: 150
                            y: 25
                            color: Colors.couleur7
                            text: model.id_task
                            font.pixelSize: 17
                            font.styleName: "Gras"
                        }

                        Text {
                            id: enddate4
                            x: 4
                            y: model.name.startsWith("↳") ? 30 : 57
                            text: model.end_date
                            font.pixelSize: 12
                        }

                        CheckBox {
                            id: checked4
                            x: 152
                            y: 2
                            width: 60
                            height: 30
                            text: "Fini ?"
                            enabled: false
                            checked: model.checked === 1
                        }

                        Text {
                            id: priority4
                            x: 65
                            y: 56
                            font.pixelSize: model.name.startsWith("↳") ? 1 : 12
                            text: {
                                if (model.priority === 1) {
                                    return "🕐";
                                } else if (model.priority === 2) {
                                    return "⚠️";
                                } else {
                                    return "";
                                }
                            }
                        }

                        Text {
                            id: tag4
                            x: 4
                            y: 35
                            text: model.tag
                            font.pixelSize: 12
                        }
                    }

                    // Ajoute un espacement supplémentaire après les sous-tâches si l'élément suivant est une tâche principale
                    Item {
                        width: 1
                        height: (index < taskModel4.count - 1 && !taskModel4.get(index + 1).name.startsWith("↳")) ? 5 : 1
                    }
                }
            }

            Connections {
                target: taskHandlerBackend
                onTasksFetchedChecked: function (tasks) {
                    taskModel4.clear();
                    for (var i = 0; i < tasks.length; i++) {
                        taskModel4.append({
                            "id_task": tasks[i].id_task,
                            "name": tasks[i].name,
                            "end_date": tasks[i].end_date,
                            "checked": tasks[i].checked,
                            "priority": tasks[i].priority,
                            "tag": tasks[i].tag
                        });
                    }
                }
            }
        }
    }

    Rectangle {
        id: rectangle1
        x: 146
        y: 33
        width: 719
        height: 96
        color: "#eeeeee"
        radius: 5
        border.color: Colors.couleur6
        border.width: 0
        layer.enabled: false
    }

    Rectangle {
        id: rectangle4
        x: 515
        y: 147
        width: 213
        height: 42
        color: Colors.couleur2
        radius: 5
        border.color: Colors.couleur6
        border.width: 0
        layer.enabled: false
    }

    Rectangle {
        id: rectangle3
        x: 280
        y: 147
        width: 213
        height: 42
        color: Colors.couleur2
        radius: 5
        border.color: Colors.couleur6
        border.width: 0
        layer.enabled: false
    }

    Rectangle {
        id: rectangle5
        x: 750
        y: 147
        width: 213
        height: 42
        color: Colors.couleur2
        radius: 5
        border.color: Colors.couleur6
        border.width: 0
        layer.enabled: false
    }

    Rectangle {
        id: rectangle2
        x: 45
        y: 147
        width: 213
        height: 42
        color: Colors.couleur2
        radius: 5
        border.color: Colors.couleur6
        border.width: 0
        layer.enabled: false

        Text {
            id: _text
            x: 0
            y: 2
            width: 213
            height: 38
            color: Colors.couleur5
            text: "Urgent"
            font.pixelSize: 28
            horizontalAlignment: Text.AlignHCenter
            font.family: "Verdana"
        }

        Text {
            id: _text1
            x: 234
            y: 2
            width: 213
            height: 38
            color: Colors.couleur4
            text: "En cours"
            font.pixelSize: 28
            horizontalAlignment: Text.AlignHCenter
            font.family: "Verdana"
        }

        Text {
            id: _text2
            x: 470
            y: 2
            width: 213
            height: 38
            color: Colors.couleur3
            text: "A Faire"
            font.pixelSize: 28
            horizontalAlignment: Text.AlignHCenter
            font.family: "Verdana"
        }

        Text {
            id: _text3
            x: 705
            y: 2
            width: 213
            height: 38
            color: "#afafafaf"
            text: "Fini"
            font.pixelSize: 28
            horizontalAlignment: Text.AlignHCenter
            styleColor: "#afafafaf"
            style: Text.Outline
            font.family: "Verdana"
        }

    }
}
