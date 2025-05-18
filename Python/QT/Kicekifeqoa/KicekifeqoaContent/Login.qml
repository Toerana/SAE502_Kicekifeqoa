import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

// Fenêtre principale de login
Window {
    id: loginWindow  // Identifiant unique pour la fenêtre
    visible: true    // Rend la fenêtre visible au lancement
    color: Colors.couleur1  // Couleur de fond définie par la palette de couleurs personnalisée
    width: 600
    height: 580
    title: "Kicekifeqoa - Login"  // Titre de la fenêtre
    minimumWidth: 600       // Largeur minimale fixe pour éviter le redimensionnement
    maximumWidth: 600       // Largeur maximale fixe
    minimumHeight: 580      // Hauteur minimale fixe
    maximumHeight: 580      // Hauteur maximale fixe

    // Lance l'animation d'ouverture au chargement de la fenêtre
    Component.onCompleted: {
        openingAnimation.start();
    }

    // Connexions pour gérer les différents états de login
    Connections {
        target: taskHandlerLogin

        // Ferme la fenêtre en cas de succès du login
        function onLoginSuccess() {
            loginWindow.close();
        }

        // Affiche un message d'erreur si le mot de passe est incorrect
        function onLoginPasswdFail() {
            _text3.text = "Mot de passe incorrect";
        }

        // Affiche un message d'erreur si l'email est incorrect
        function onLoginEmailFail() {
            _text3.text = "Email incorrect";
        }
    }

    // Fonction pour recharger la fenêtre de login
    function reloadWindow() {
        loginWindow.close();  // Ferme la fenêtre actuelle
        Qt.createComponent("Login.qml").createObject(null);  // Crée une nouvelle instance de la fenêtre
    }

    // Conteneur principal pour les éléments de l'interface utilisateur
    Rectangle {
        id: rectangle
        x: 20
        y: 20
        width: 560
        height: 546
        color: Colors.couleur2
        radius: 5
        border.width: 0
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: 0
        anchors.horizontalCenterOffset: 0
        anchors.horizontalCenter: parent.horizontalCenter

        // Conteneur pour les boutons de login et d'enregistrement
        Rectangle {
            id: rectangle4
            x: 153
            y: 405
            width: 361
            height: 125
            color: Colors.couleur3
            radius: 5
            border.width: 0
            anchors.horizontalCenter: parent.horizontalCenter

            Rectangle {
                id: rectangle5
                x: 70
                y: 70
                width: 100
                height: 40
                color: Colors.couleur2
                radius: 5
            }

            Rectangle {
                id: rectangle6
                x: 195
                y: 69
                width: 100
                height: 40
                color: Colors.couleur2
                radius: 5
                anchors.bottom: rectangle5.bottom
            }
        }

        Rectangle {
            id: rectangle3
            x: 153
            y: 138
            width: 361
            height: 245
            color: Colors.couleur5
            radius: 5
            anchors.bottom: rectangle2.bottom
            anchors.bottomMargin: -139
            anchors.horizontalCenterOffset: 0
            anchors.horizontalCenter: parent.horizontalCenter
        }

        // Étiquette pour le champ d'email
        Text {
            id: _text1
            x: 229
            y: 155
            width: 103
            height: 42
            color: Colors.couleur2
            text: "E-mail :"
            font.pixelSize: 30
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.family: "Verdana"
        }

        // Rectangle de fond pour le champ de saisie de l'email
        Rectangle {
            id: rectangle2
            x: 123
            y: 208
            width: 317
            height: 36
            opacity: 1
            color: Colors.couleur2
            radius: 5
            clip: false
        }

        // Champ de saisie pour l'email
        TextInput {
            id: textInput1
            x: 128
            y: 208
            width: 304
            height: 36
            text: ""
            anchors.top: rectangle2.top
            anchors.bottom: rectangle2.bottom
            font.pixelSize: 16
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.horizontalCenter: parent.horizontalCenter
            selectedTextColor: Colors.couleur2
            clip: true

            Keys.onReturnPressed: {
                loginButton.clicked()
            }
            Keys.onTabPressed: {
                textInput2.forceActiveFocus()
            }
        }

        // Étiquette pour le champ de mot de passe
        Text {
            id: _text2
            x: 208
            y: 264
            width: 144
            height: 43
            color: Colors.couleur2
            text: "Password :"
            font.pixelSize: 30
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.family: "Verdana"

            // Rectangle de fond pour le champ de mot de passe
            Rectangle {
                id: rectangle1
                x: -84
                y: 47
                width: 315
                height: 36
                opacity: 1
                color: Colors.couleur2
                radius: 5
                clip: false
            }
        }

        // Champ de saisie pour le mot de passe
        TextInput {
            id: textInput2
            x: 202
            y: 313
            width: 300
            height: 36
            text: ""
            anchors.top: _text2.bottom
            anchors.topMargin: 6
            font.pixelSize: 16
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.horizontalCenter: rectangle2.horizontalCenter
            selectedTextColor: Colors.couleur2
            echoMode: TextInput.Password  // Cache le texte pour le mot de passe
            clip: true

            // Déclenche le clic sur le bouton de login en appuyant sur Entrée
            Keys.onReturnPressed: {
                loginButton.clicked();
            }
        }

        // Bouton pour soumettre le login
        Button {
            id: loginButton
            x: 168
            y: 474
            width: 100
            height: 40
            visible: true
            text: "Login"
            highlighted: false
            flat: true
            icon.color: "#b6d4f2"

            // Appel à la fonction de vérification des identifiants
            onClicked: {
                taskHandlerLogin.checkCredentials(textInput1.text, textInput2.text);
            }
        }

        // Connexion pour gérer le succès du login
        Connections {
            target: taskHandlerLogin
            onLoginSuccess: function(userId) {
                Qt.application.userId = userId;  // Stocke l'ID utilisateur globalement
            }
        }

        // Bouton pour ouvrir la page d'enregistrement
        Button {
            id: registerButton
            x: 295
            y: 474
            width: 100
            height: 40
            text: "Register"
            flat: true

            // Chargement dynamique du fichier Register.qml
            onClicked: {
                var component = Qt.createComponent("Register.qml");

                // Vérifie si le composant est prêt avant de le créer
                if (component.status === Component.Ready) {
                    component.createObject(parent);
                }
            }
        }

        // Logo de l'application
        Image {
            id: image
            x: 230
            y: 18
            width: 102
            height: 101
            source: "images/logo.png"  // Chemin vers le logo de l'application
        }

        // Texte pour afficher les messages d'erreur de login
        Text {
            id: _text3
            x: 112
            y: 417
            width: 338
            height: 30
            color: Colors.couleur2
            font.pixelSize: 20
            horizontalAlignment: Text.AlignHCenter
            font.styleName: "Gras"
            font.family: "Verdana"
            anchors.horizontalCenter: rectangle2.horizontalCenter
        }

        // Bouton pour changer le thème de l'application
        Button {
            id: colorButton
            x: 520
            y: 505
            width: 40
            height: 40

            // Fond transparent pour le bouton
            background: Rectangle {
                color: "transparent"
            }

            // Image du sélecteur de couleur
            contentItem: Image {
                source: "images/Cwheel.png"  // Chemin vers l'image du sélecteur
                width: 40
                height: 40
                anchors.centerIn: parent
            }

            // Change le thème et lance l'animation
            onClicked: {
                Colors.changeStyle();
                animation.start();
            }
        }

        // Animation pour le changement de thème
        SequentialAnimation {
            id: animation

            // Animation pour réduire l'opacité de la fenêtre
            PropertyAnimation {
                target: loginWindow
                property: "opacity"
                from: 1
                to: 0
                duration: 500  // Durée de l'animation
            }

            // Action pour recharger la fenêtre après l'animation
            ScriptAction {
                script: {
                    loginWindow.reloadWindow();
                }
            }
        }

        // Animation pour l'ouverture de la fenêtre
        PropertyAnimation {
            id: openingAnimation
            target: loginWindow
            property: "opacity"
            from: 0
            to: 1
            duration: 500  // Durée de l'animation d'ouverture
        }

        // État de la fenêtre
        states: [
            State {
                name: "clicked"  // État nommé "clicked" (placeholder pour des extensions futures)
            }
        ]

    }

}
