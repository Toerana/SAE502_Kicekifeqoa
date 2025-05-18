import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Window {
    id: registerWindow
    visible: true
    width: 400
    height: 400
    title: "Kicekifeqoa - Register"    // Titre de la fenêtre principale
    flags: Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint
    minimumWidth: 400      // Largeur minimale fixe
    maximumWidth: 400      // Largeur maximale fixe
    minimumHeight: 400      // Hauteur minimale fixe
    maximumHeight: 400      // Hauteur maximale fixe

    Connections {
        target: taskHandlerRegister
        onRegisterSuccess: {
            registerWindow.close();  // Fermer la fenêtre register
        }
        onAlreadyMail: {
            _text3.text = "Mail déjà existant";  // Affiche un message d'erreur pour le email
        }
        onBadMail: {
            _text3.text = "Adresse mail non valide";  // Affiche un message d'erreur pour le email
        }
        onShortPass: {
            _text3.text = "Mot de passe trop court";  // Affiche un message d'erreur pour le mdp
        }
         onLongPass: {
            _text3.text = "Mot de passe trop long";  // Affiche un message d'erreur pour le mdp
        }
        onUppercasePass: {
            _text3.text = "Majuscule requise";  // Affiche un message d'erreur pour le mdp
        }
        onLowercasePass: {
            _text3.text = "Minuscule requise";  // Affiche un message d'erreur pour le mdp
        }
        onNumberPass: {
            _text3.text = "Nombre requis";  // Affiche un message d'erreur pour le mdp
        }
        onSpecialPass: {
            _text3.text = "Symbole spécial requis";  // Affiche un message d'erreur pour le mdp
        }
        onUnknownError: {
            _text3.text = "Une erreur inconnu s'est produite";  // Affiche un message d'erreur pour le mdp
        }
    }
    Rectangle {
        x: 0
        y: 0
        width: 400
        height: 400
        color: Colors.couleur1
        Rectangle {
        id: rectangle
        x: 9
        y: 9
        width: 380
        height: 382
        color: Colors.couleur2
        radius: 5
        border.width: 0


        Rectangle {
            id: rectangle1
            x: 36
            y: 12
            width: 307
            height: 89
            color: Colors.couleur5
            radius: 5
        }

        Rectangle {
            id: rectangle3
            x: 36
            y: 123
            width: 307
            height: 244
            color: Colors.couleur3
            radius: 5
        }

        Rectangle {
            id: rectangle4
            x: 141
            y: 320
            width: 98
            height: 40
            color: Colors.couleur2
            radius: 5
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            id: _text
            x: 77
            y: 218
            width: 227
            height: 33
            color: Colors.couleur2
            text: "Password :"
            font.pixelSize: 25
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.family: "Verdana"
        }

        Text {
            id: _text2
            x: 77
            y: 130
            width: 227
            height: 33
            color: Colors.couleur2
            text: "E-mail :"
            font.pixelSize: 25
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.family: "Verdana"
        }

        Button {
            id: button
            x: 140
            y: 320
            width: 98
            height: 40
            text: "Register"
            anchors.horizontalCenter: _text2.horizontalCenter
            flat: true
            onClicked: {
                taskHandlerRegister.checkCredentials(textInputmail.text, textInputpasswd.text)
            }
        }

        Text {
            id: _text3
            x: 36
            y: 36
            width: 307
            height: 40
            color: Colors.couleur2
            text: "Créer un compte"
            font.pixelSize: 20
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.family: "Verdana"
        }

        Rectangle {
            id: rectangle5
            x: 47
            y: 163
            width: 256
            height: 36
            color: Colors.couleur2
            radius: 5
            anchors.left: rectangle2.left
            anchors.right: rectangle2.right
            anchors.rightMargin: 0
        }

        Rectangle {
            id: rectangle2
            x: 77
            y: 251
            width: 286
            height: 36
            color: Colors.couleur2
            radius: 5
            anchors.left: _text2.left
            anchors.bottom: _text1.top
            anchors.leftMargin: -30
            anchors.bottomMargin: 6
        }

        Text {
            id: _text4
            x: 48
            y: 293
            width: 285
            height: 27
            text: ""
            anchors.top: rectangle2.bottom
            anchors.topMargin: 6
            anchors.bottomMargin: 6
            color: "#e91717"
            font.pixelSize: 20
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    TextInput {
        id: textInputmail
        x: 65
        y: 172
        width: 264
        height: 36
        text: ""
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        clip: true  // Coupe le texte dépassant la largeur définie
    }

    TextInput {
        id: textInputpasswd
        x: 65
        y: 262
        width: 264
        height: 36
        text: ""
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        echoMode: TextInput.Password  // Cache le texte pour le champ de mot de passe
        clip: true  // Coupe le texte dépassant la largeur définie
    }
    }
}