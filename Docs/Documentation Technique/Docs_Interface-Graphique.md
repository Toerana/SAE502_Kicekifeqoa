# Documentation de l'Interface Graphique  
  
1. [Documentation du Frontend - Interface Graphique (QML)](#documentation-du-frontend---interface-graphique-qml) 
2. [Documentation du Backend - Logique Backend (Python)](#documentation-du-backend-de-linterface-graphique-python)

# Documentation du Frontend - Interface Graphique (QML)

L’interface graphique de l’application Kicekifeqoa est construite à l’aide de QML et des composants QtQuick. Elle permet de consulter, créer, modifier et supprimer des tâches et des sous-tâches. L’utilisateur peut cliquer sur des éléments pour les sélectionner, ouvrir des popups contextuels pour créer ou modifier des éléments, et afficher des messages d’erreur ou de succès lorsque des opérations sont effectuées.

![arborescence QT](https://i.imgur.com/lWuGuqi.png)

Chaque fichier QML remplit un rôle particulier : affichage de la page de login, enregistrement des utilisateurs, tableau principal de gestion des tâches, et popups spécifiques à la création, modification ou suppression de tâches et sous-tâches. Les éléments de l’interface s’appuient sur les TaskHandlers pour effectuer les opérations CRUD, tandis que la gestion des signaux et slots permet une synchronisation en temps réel entre l’UI et la logique métier.

## Sommaire

1. [Login.qml](#loginqml)  
2. [Register.qml](#registerqml)  
3. [App.qml](#appqml)  
4. [PopupCreateTask.qml](#popupcreatetaskqml)  
5. [PopupUpdateTask.qml](#popupupdatetaskqml)  
6. [PopupDeleteTask.qml](#popupdeletetaskqml)  
7. [PopupCreateSubtask.qml](#popupcreatesubtaskqml)  
8. [PopupUpdateSubtask.qml](#popupupdatesubtaskqml)

## `Login.qml`
### Rôle Général
Ce fichier QML représente la fenêtre de connexion (login) pour l'application. Il offre une interface graphique permettant à l'utilisateur de saisir son adresse email et son mot de passe, de valider ses informations et d'accéder à la fenêtre d'enregistrement s'il n'a pas encore de compte. Il gère également l'affichage de messages d'erreur en cas de mauvaises informations, la personnalisation du thème et des animations d'ouverture / rechargement.

1. Afficher un champ email et un champ mot de passe pour la connexion.
2. Gérer la validation des identifiants via le `taskHandlerLogin` (affichage d'erreurs, fermeture de la fenêtre en cas de succès).
3. Fournir un bouton pour accéder à la fenêtre d'enregistrement (`Register.qml`).
4. Permettre le changement de thème de l'application et le rechargement de la fenêtre.
5. Inclure des animations visuelles pour l'ouverture de la fenêtre et le changement de thème.

### Composants Clés
- **TextInput (textInput1, textInput2)** : Champs de saisie pour l'email et le mot de passe.
- **Button (loginButton)** : Lance la vérification des identifiants auprès du `taskHandlerLogin`.
- **Button (registerButton)** : Charge dynamiquement la page d'enregistrement `Register.qml`.
- **Button (colorButton)** : Permet de changer la palette de couleurs et de recharger la fenêtre (changement de thème).
- **Text (_text3)** : Affiche les messages d'erreur (mot de passe incorrect, email incorrect).
- **Image (image)** : Affiche le logo de l'application.
- **Connections (taskHandlerLogin)** : Écoute les signaux `loginSuccess`, `loginPasswdFail` et `loginEmailFail` pour réagir aux tentatives de connexion.
- **Animations (openingAnimation, animation)** : Gèrent les transitions d'ouverture de la fenêtre et le rechargement après un changement de thème.

## `Register.qml`
### Rôle Général
Ce fichier QML représente la fenêtre d'enregistrement (register) de l'application. Il permet à l'utilisateur de saisir une adresse email et un mot de passe pour créer un compte. Des validations sont effectuées côté serveur (via `taskHandlerRegister`) et des messages d'erreur sont affichés en cas de problème (email existant, format incorrect, mot de passe non conforme, etc.). En cas de succès, la fenêtre se ferme.

1. Afficher des champs de saisie pour l'email et le mot de passe.
2. Envoyer les données au `taskHandlerRegister` pour valider et créer un nouveau compte.
3. Afficher des messages d'erreur en fonction de la réponse du handler (email déjà pris, mot de passe non conforme, etc.).
4. Fermer la fenêtre d'enregistrement en cas de succès.

### Composants Clés
- **TextInput (textInputmail, textInputpasswd)** : Champs de saisie pour l'email et le mot de passe.
- **Button (button)** : Lance la procédure d'enregistrement via `taskHandlerRegister`.
- **Text (_text3)** : Affiche le titre et, en réutilisant la même zone, les éventuels messages d'erreur.
- **Connections (taskHandlerRegister)** : Écoute les signaux indiquant le succès ou les différentes erreurs de l'enregistrement. Selon le signal reçu, met à jour `_text3` avec le message correspondant.

## `App.qml`
### Rôle Général
Ce fichier QML représente la fenêtre principale de l'application après la connexion d'un utilisateur. Il présente un tableau de bord affichant les tâches et leurs sous-tâches, organisées en quatre colonnes selon leur priorité et leur état d'achèvement (Urgent, En cours, À Faire, Fini).

1. Afficher les tâches de l’utilisateur connecté, réparties en quatre colonnes selon leur priorité et leur statut (cochées ou non).
2. Permettre la sélection d’une tâche ou d’une sous-tâche.
3. Ouvrir des popups pour la création, la modification ou la suppression de tâches / sous-tâches selon l’élément sélectionné.
4. Actualiser les données après chaque opération CRUD en interrogeant les TaskHandlers (backend).

### Composants Clés
- **GridLayout + 4 Rectangles (taskArea, taskArea2, taskArea3, taskArea4)** :  
  Affichent les listes de tâches réparties par priorité (urgent, en cours, à faire) et par statut (fini).
  
- **ListView (taskListView, taskListView2, taskListView3, taskListView4) + ListModel** :  
  Chaque colonne utilise un modèle de données lié à des tâches spécifiques, récupérées via `taskHandlerBackend`. Les `ListView` utilisent un delegate affichant le nom, l’ID, la date de fin, un indicateur de priorité, les tags, et un checkbox pour le statut de chaque tâche.

- **Interaction avec les tâches** :  
  - **Sélection d’une tâche** : Un clic sur une tâche la met en surbrillance et stocke son ID et son nom.
  - **Création de nouvelles tâches / sous-tâches** : Le bouton “+” ouvre un popup approprié (`PopupCreateTask.qml` ou `PopupCreateSubtask.qml`) selon qu’une tâche est sélectionnée (pour créer une sous-tâche) ou non (pour créer une nouvelle tâche).
  - **Modification d’une tâche / sous-tâche** : Le bouton 🖌️ ouvre le popup de modification (`PopupUpdateTask.qml` ou `PopupUpdateSubtask.qml`) en fonction du type d’élément sélectionné.
  - **Suppression d’une tâche / sous-tâche** : Le bouton 🗑️ ouvre un popup de suppression (`PopupDeleteTask.qml`).

- **Connections (taskHandlerBackend, taskHandlerCreate, taskHandlerUpdate, subtaskHandlerCreate, subtaskHandlerUpdate, taskHandlerDelete)** :  
  Permettent de récupérer, mettre à jour, ajouter ou supprimer des tâches. Les signaux `TasksFetchedPriorityX` sont utilisés pour charger les tâches dans chaque colonne.

- **Animations et Interface** :  
  Les propriétés de style (couleurs, polices, etc.) sont gérées par la palette de couleurs `Colors.couleurX` et le design reste cohérent avec les autres écrans.

## `PopupCreateTask.qml`
### Rôle Général
Ce composant QML affiche une fenêtre popup qui permet à l’utilisateur de créer une nouvelle tâche. Il offre la possibilité de définir le nom, la date de fin, la priorité, d’ajouter ou retirer des tags, ainsi que de marquer la tâche comme terminée. Une fois les informations validées, il envoie ces données au `taskHandlerCreate`.

1. Saisir et valider le nom de la tâche.
2. Définir la priorité de la tâche (basse, moyenne, urgente).
3. Ajouter ou supprimer des tags.
4. Définir la date de fin.
5. Marquer la tâche comme terminée ou non.
6. Envoyer l’ensemble des informations au `taskHandlerCreate` pour la création de la tâche.

### Composants Clés
- **TextField (taskname, tagname, enddate)** : Champs de saisie pour le nom de la tâche, le nom des tags, et la date de fin.
- **Slider (priorityslider)** : Permet de choisir la priorité de la tâche (0, 1 ou 2).
- **RoundButton (tagadd, tagremove, validate, close)** :  
  - `tagadd`: Ajoute un tag à la liste des tags.  
  - `tagremove`: Supprime le dernier tag ajouté.  
  - `validate`: Valide les informations saisies et déclenche la création de la tâche.  
  - `close`: Ferme la fenêtre sans valider.
- **CheckBox (checkBox)** : Permet d’indiquer si la tâche est déjà terminée.
- **ListModel (tagsListModel)** + **Flickable / Repeater** : Gèrent l’affichage dynamique des tags ajoutés.
- **Connections (taskHandlerCreate)** : Ferme le popup lors de la réception du signal `validationSuccess` indiquant la réussite de la création.

## `PopupUpdateTask.qml`
### Rôle Général
Ce composant QML affiche une fenêtre popup pour la mise à jour d’une tâche existante. Il offre la possibilité de modifier le nom, la priorité, les tags, la date de fin, et le statut (terminée ou non) de la tâche. Les informations initiales de la tâche sont préremplies. Une fois les modifications apportées et validées, elles sont transmises au `taskHandlerUpdate` pour enregistrement.

1. Afficher et modifier le nom de la tâche existante.
2. Ajuster la priorité (basse, moyenne, urgente) via un slider.
3. Ajouter ou retirer des tags.
4. Modifier la date de fin.
5. Mettre à jour le statut de la tâche (terminée ou non).
6. Envoyer les informations mises à jour au `taskHandlerUpdate` pour sauvegarde.

### Composants Clés
- **TextField (taskname, enddate, tagname)** : Champs de saisie pour le nom de la tâche, sa date de fin, et l’ajout de tags.
- **Slider (priorityslider)** : Permet de définir la priorité (0 à 2) et de voir l’état textuel correspondant.
- **RoundButton (tagadd, tagremove, validate, close)** :  
  - `tagadd` : Ajoute un tag à la liste.  
  - `tagremove` : Supprime le dernier tag ajouté.  
  - `validate` : Valide les informations mises à jour et déclenche l’enregistrement.  
  - `close` : Ferme la fenêtre sans enregistrer.
- **CheckBox (checkBox)** : Indique si la tâche est marquée comme terminée.
- **ListModel (tagsListModel)** + **Flickable / Repeater** : Affichent dynamiquement les tags associés.
- **Connections (taskHandlerUpdate)** : Ferme le popup en cas de succès de la mise à jour.


## `PopupDeleteTask.qml`
### Rôle Général
Ce fichier QML représente une fenêtre popup de confirmation pour la suppression d’une sous-tâche (ou d’une tâche, selon le contexte). Il informe l’utilisateur de la tâche qu’il est sur le point de supprimer et offre la possibilité de confirmer ou d’annuler l’opération.

1. Afficher le nom de la tâche (ou sous-tâche) ciblée pour la suppression.
2. Permettre à l’utilisateur de confirmer ou d’annuler la suppression.
3. Émettre les signaux nécessaires (`taskId` et `validateDeleteInfo`) pour déclencher la logique de suppression côté backend.

### Composants Clés
- **Window** : Fenêtre popup dédiée à la confirmation de la suppression.
- **Text (tasknametext)** : Affiche le nom de la tâche à supprimer.
- **RoundButton (validate, cancel)** :  
  - `validate` : Confirme la suppression, émet les signaux nécessaires puis ferme le popup.  
  - `cancel` : Annule l’opération et ferme le popup.
- **Signals (taskId, validateDeleteInfo)** : Transmettent l’ID de la tâche et déclenchent la procédure de suppression du côté du code Python.

## `PopupCreateSubtask.qml`
### Rôle Général
Ce composant QML affiche une fenêtre popup permettant de créer une sous-tâche associée à une tâche parent déjà sélectionnée. L’utilisateur peut spécifier le nom de la sous-tâche, sa date de fin, et indiquer si elle est déjà terminée. Une fois validées, ces informations sont envoyées au `subtaskHandlerCreate` pour la création en base de données.

1. Saisir le nom de la sous-tâche.
2. Définir la date de fin de la sous-tâche.
3. Spécifier si la sous-tâche est déjà terminée.
4. Envoyer les informations au `subtaskHandlerCreate` pour créer la sous-tâche.

### Composants Clés
- **TextField (taskname, enddate)** : Champs de saisie pour le nom de la sous-tâche et sa date de fin.
- **CheckBox (checkBox)** : Permet d’indiquer si la sous-tâche est terminée.
- **RoundButton (validate, close)** :  
  - `validate`: Valide les informations saisies et envoie les données au `subtaskHandlerCreate`.  
  - `close`: Ferme la fenêtre sans valider.
- **Connections (subtaskHandlerCreate)** : Ferme le popup en cas de succès de la création.

## `PopupUpdateSubtask.qml`
### Rôle Général
Ce composant QML affiche une fenêtre popup pour la mise à jour d’une sous-tâche existante. Il offre la possibilité de modifier le nom, la date de fin, et le statut (terminée ou non) de la sous-tâche. Les informations initiales de la sous-tâche sont préremplies. Une fois les modifications apportées et validées, elles sont transmises au `subtaskHandlerUpdate` pour enregistrement.

1. Afficher et modifier le nom de la sous-tâche existante.
2. Mettre à jour la date de fin.
3. Indiquer si la sous-tâche est terminée ou non.
4. Envoyer les informations mises à jour au `subtaskHandlerUpdate` pour sauvegarde.

### Composants Clés
- **TextField (taskname, enddate)** : Champs de saisie pour le nom de la sous-tâche et sa date de fin.
- **CheckBox (checkBox)** : Indique si la sous-tâche est marquée comme terminée.
- **RoundButton (validate, close)** :  
  - `validate` : Valide les informations mises à jour et déclenche l’enregistrement.  
  - `close` : Ferme la fenêtre sans enregistrer.
- **Connections (subtaskHandlerUpdate)** : Ferme le popup en cas de succès de la mise à jour.

# Documentation du backend de l'Interface Graphique (Python)

1. [TaskHandlers](#taskhandlers)
2. [Modules Python Restants](#modules-python-restants)

## TaskHandlers

Les **TaskHandlers** sont des composants assurant la liaison entre les fichiers (CRUD sur la base de données) et l'interface graphique QML, fournissant ainsi une couche intermédiaire qui facilite la récupération, la mise à jour, la création et la suppression des données.

![arborescence taskhandler](https://i.imgur.com/ifgJUZs.png)

Chaque TaskHandler est spécialisé dans une partie , comme la gestion des utilisateurs (login, register), la récupération des données, la création, la mise à jour ou la suppression des tâches et sous-tâches. Ils offrent des interfaces claires sous forme de Slots et de Signaux, permettant au QML de réagir aux changements en temps réel et de transmettre facilement les données de l’utilisateur au code Python, puis au backend.

## Sommaire 

1. [task_handler_Login (TaskHandlerLogin)](#task_handler_login-taskhandlerlogin)  
2. [task_handler_Register (TaskHandler)](#task_handler_register-taskhandler)  
3. [task_handler_AppRead (TaskHandlerAppRead)](#task_handler_appread-taskhandlerappread)  
4. [task_handler_Pcreate (TaskHandler)](#task_handler_pcreate-taskhandler)  
5. [task_handler_Pupdate (TaskHandler)](#task_handler_pupdate-taskhandler)  
6. [task_handler_Pdelete (TaskHandler)](#task_handler_pdelete-taskhandler)  
7. [subtask_handler_Pcreate (TaskHandler)](#subtask_handler_pcreate-taskhandler)  
8. [subtask_handler_Pupdate (TaskHandler)](#subtask_handler_pupdate-taskhandler)



## `task_handler_Login` (TaskHandlerLogin)
### Rôle Général
Ce TaskHandler gère la logique d'authentification des utilisateurs. Il vérifie les identifiants de connexion (email, mot de passe), signale le succès ou l'échec de la tentative de connexion et, en cas de réussite, charge l'interface principale et récupère les tâches associées à l'utilisateur.

1. Vérifier l’authenticité des identifiants (email / mot de passe) des utilisateurs.
2. Gérer les signaux de succès ou d’échec de la connexion (erreur mot de passe, erreur email).
3. Sur connexion réussie, charger l'interface principale et déclencher la récupération des tâches utilisateur.

### Fonctions Clés

- **verify_password(stored_password, provided_password)** :  
  Compare le mot de passe fourni par l'utilisateur avec le mot de passe hashé stocké dans la base de données à l'aide de bcrypt. Retourne True si les mots de passe correspondent, False sinon.

- **checkCredentials(email, password)** :  
  Vérifie si l'email existe et récupère les informations de l'utilisateur. Si l'utilisateur est trouvé, vérifie le mot de passe.  
  - En cas de succès :  
    - Émet le signal `loginSuccess` avec l'ID de l’utilisateur.  
    - Charge l’interface principale (`App.qml`).  
    - Utilise `TaskHandlerAppRead` pour récupérer les tâches associées.  
  - En cas d’échec :  
    - Émet `loginPasswdFail` si le mot de passe est incorrect.  
    - Émet `loginEmailFail` si l'email n'est pas reconnu.

- **get_user_id()** :  
  Retourne l'ID de l'utilisateur actuellement connecté après une authentification réussie.

## `task_handler_Register` (TaskHandler)
### Rôle Général
Ce TaskHandler gère la logique d'enregistrement des nouveaux utilisateurs. Il vérifie la validité de l'email et du mot de passe, signale le succès ou les différentes erreurs (email déjà pris, format d'email incorrect, mot de passe trop court, etc.).

1. Valider les informations d'inscription (email et mot de passe).
2. Gérer et signaler les différentes erreurs d'enregistrement (format d'email, longueur du mot de passe, etc.).
3. Sur validation complète, émettre un signal de succès.

### Fonctions Clés

- **checkCredentials(email, password)** :  
  Tente de créer un nouvel utilisateur avec l'email et le mot de passe fournis en appelant `create_user`.  
  - En cas de réussite : émet `registerSuccess`.  
  - En cas d’échec : émet le signal correspondant au problème détecté (email déjà existant, problème de format d’email, mot de passe non conforme, etc.).

## `task_handler_AppRead` (TaskHandlerAppRead)
### Rôle Général
Ce TaskHandler se charge de récupérer les tâches et leurs sous-tâches associées depuis la base de données en fonction de l'utilisateur connecté. Il les répartit par priorité et par statut (cochées ou non), puis les transmet à l'interface QML via des signaux.

1. Récupérer les tâches pour l'utilisateur connecté, classées par priorité et statut (non terminées / terminées).
2. Récupérer et associer les sous-tâches à leurs tâches parentes.
3. Émettre des signaux vers l'interface QML pour mettre à jour la vue principale de l'application.

### Fonctions Clés

- **fetchTasks(user_id)** :  
  Récupère les tâches selon leur priorité (0, 1, 2) et leur statut (cochées / non cochées) pour un utilisateur donné.  
  - Récupère toutes les tâches et sous-tâches.  
  - Les groupe par parent (tâche principale) avec leurs sous-tâches.  
  - Émet les signaux `tasksFetchedPriority2`, `tasksFetchedPriority1`, `tasksFetchedPriority0`, `tasksFetchedChecked` contenant les tâches regroupées.

- **get_tasks_from_api(user_id, priority_filter=None, checked_filter=None, exclude_checked=False)** :  
  Interroge l'API (via CRUD) pour récupérer les tâches filtrées par priorité et/ou par statut (coché ou non).  
  - Retourne une liste de tâches formatées avec `id_task`, `name`, `end_date`, `checked`, `priority`, `tag`.

- **get_subtasks_from_api(exclude_checked=False)** :  
  Récupère toutes les sous-tâches et détermine leur priorité en fonction de leurs tâches parentes.  
  - Peut filtrer les sous-tâches cochées si demandé.  
  - Retourne une liste de sous-tâches formatées avec `id_task`, `name`, `end_date`, `checked`, `priority`, `tag`, `parent_id`, ainsi que les utilisateurs associés à la tâche parente.

- **group_tasks_with_subtasks(tasks, subtasks)** :  
  Associe chaque tâche principale à ses sous-tâches correspondantes, formant une liste structurée qui sera envoyée à l’interface.  
  - Retourne une liste combinant tâches et sous-tâches, facilitant ainsi leur affichage en cascade dans l’UI.

## `task_handler_Pcreate` (TaskHandler)
### Rôle Général
Ce TaskHandler gère la création de nouvelles tâches dans l'application. Il permet de renseigner un nom, une priorité, des tags, des utilisateurs associés, une date de fin et un statut d'achèvement. Après validation, il crée la tâche, l'associe à l'utilisateur connecté ainsi qu'à l'administrateur.

1. Recueillir et valider les informations nécessaires à la création d’une tâche (nom, date de fin, priorité, tags, utilisateurs).
2. Créer la tâche en base de données.
3. Associer la tâche à l’utilisateur connecté et à l’administrateur.
4. Émettre un signal de succès une fois la tâche créée.

### Fonctions Clés

- **add_task_name(taskname)** :  
  Ajoute le nom de la tâche. Vérifie que le nom n’est pas vide.

- **add_task_priority(priority)** :  
  Définit la priorité de la tâche (0, 1, 2). Vérifie que la priorité est valide.

- **add_tag(tag)** / **remove_last_tag()** :  
  Ajoute ou supprime des tags à la liste des tags de la tâche. Met ensuite à jour la liste de tags dans l’interface QML.

- **add_user(user)** / **remove_last_user()** :  
  Ajoute ou supprime des utilisateurs associés à la tâche (utilisable seulement par l'admin).

- **add_end_date(enddate)** :  
  Définit la date de fin de la tâche après validation du format de la date.

- **task_completed(status)** :  
  Met à jour le statut d’achèvement de la tâche (cochée ou non).

- **validate_info()** :  
  Vérifie que toutes les informations requises (nom, date de fin) sont renseignées et cohérentes.  
  - Crée la tâche en base de données.  
  - Associe la tâche à l’utilisateur connecté et à l’administrateur.  
  - Émet le signal `validationSuccess` en cas de réussite.

## `task_handler_Pupdate` (TaskHandler)
### Rôle Général
Ce TaskHandler gère la mise à jour des tâches existantes. Il récupère d’abord une tâche à partir de son ID, puis permet de modifier son nom, sa priorité, ses tags, sa date de fin et son statut (achevée ou non). Après validation, il enregistre les modifications dans la base de données.

1. Récupérer une tâche existante par son ID.
2. Mettre à jour ses attributs (nom, priorité, tags, date de fin, statut).
3. Valider les informations mises à jour et enregistrer la tâche en base de données.
4. Émettre un signal de succès après une mise à jour réussie.

### Fonctions Clés

- **fetch_task_by_id(task_id)** :  
  Récupère la tâche correspondante à l’ID donné, ainsi que ses attributs. Émet le signal `taskFetched` pour transmettre les données au QML (nom, priorité, tags, date de fin, statut).

- **update_task_name(updatetaskname)** :  
  Met à jour le nom de la tâche, en vérifiant qu’il n’est pas vide.

- **update_task_priority(updatepriority)** :  
  Met à jour la priorité de la tâche, vérifie que la priorité est valide (0, 1, ou 2).

- **add_tag(tagname)** / **remove_last_tag()** :  
  Ajoute ou supprime un tag associé à la tâche. Met à jour la liste des tags dans le QML.

- **update_end_date(updateenddate)** :  
  Met à jour la date de fin de la tâche après en avoir validé le format.

- **task_completed(status)** :  
  Met à jour l’état d’achèvement de la tâche (cochée ou non).

- **validate_update_info()** :  
  Vérifie la cohérence et la validité des informations mises à jour (nom, date de fin). En cas de succès, appelle `update_task` pour sauvegarder les changements en base de données et émet le signal `validationSuccess`.

## `task_handler_Pdelete` (TaskHandler)
### Rôle Général
Ce TaskHandler gère la suppression des tâches et de leurs sous-tâches associées. Il permet de sélectionner une tâche ou une sous-tâche à supprimer, puis effectue la suppression dans la base de données.

1. Sélectionner une tâche ou une sous-tâche à supprimer.
2. Supprimer les sous-tâches associées avant de supprimer la tâche principale, afin de maintenir l’intégrité des données.
3. Gérer la suppression de sous-tâches individuelles en cas d’identifiants au format spécifique (ex: "id_subtask.id_task").

### Fonctions Clés

- **set_task_id(taskid)** :  
  Définit l’ID de la tâche ou de la sous-tâche à supprimer. Vérifie que l’ID n’est pas vide et l’enregistre.

- **validate_delete_info()** :  
  Effectue la logique de suppression.  
  - Si l’ID comporte un point (`"."`), il s’agit d’une sous-tâche. La sous-tâche est alors supprimée.  
  - Sinon, toutes les sous-tâches associées sont supprimées, puis la tâche principale est supprimée.  
  Gère les erreurs de validation si aucune tâche n’a été spécifiée.

## `subtask_handler_Pcreate` (TaskHandler)
### Rôle Général
Ce TaskHandler gère la création de nouvelles sous-tâches. Il permet de définir la tâche parente, le nom et la date de fin de la sous-tâche, ainsi que son statut (terminée ou non). Après validation, il crée la sous-tâche dans la base de données.

1. Définir l’ID de la tâche parente.
2. Renseigner le nom et la date de fin de la sous-tâche.
3. Vérifier la validité du nom, du format de la date et la cohérence des dates.
4. Créer la sous-tâche dans la base de données et émettre un signal de succès.

### Fonctions Clés

- **define_parent_task_id(parenttaskid)** :  
  Définit l’ID de la tâche parente à partir de l’ID fourni (qui peut contenir un format spécial, ex: "1.2"), en ne gardant que la partie principale.

- **add_task_name(taskname)** :  
  Définit le nom de la sous-tâche, en s’assurant qu’il n’est pas vide.

- **add_end_date(enddate)** :  
  Détermine et valide le format de la date de fin de la sous-tâche.  
  Si la date n’est pas valide ou est vide, une erreur est levée.

- **task_completed(status)** :  
  Met à jour le statut d’achèvement de la sous-tâche (0 = non terminée, 1 = terminée).

- **validate_info()** :  
  Vérifie que le nom et la date de fin de la sous-tâche sont valides et cohérents.  
  - En cas de succès, crée la sous-tâche dans la base de données.  
  - Émet le signal `validationSuccess` après une création réussie.

## `subtask_handler_Pupdate` (TaskHandler)
### Rôle Général
Ce TaskHandler gère la mise à jour des sous-tâches existantes. Il permet de récupérer une sous-tâche à partir de son ID, puis de modifier son nom, sa date de fin et son statut (terminée ou non). Après validation, il met à jour la sous-tâche dans la base de données.

1. Récupérer une sous-tâche existante par son ID.
2. Mettre à jour les informations de la sous-tâche (nom, date de fin, statut).
3. Valider ces informations et enregistrer les modifications.
4. Émettre un signal de succès après une mise à jour réussie.

### Fonctions Clés

- **fetch_task_by_id(task_id)** :  
  Récupère et émet les informations de la sous-tâche (ID, ID de la tâche parente, nom, date de fin, statut) au QML via le signal `taskFetched`.

- **update_task_name(updatetaskname)** :  
  Met à jour le nom de la sous-tâche, en vérifiant qu’il n’est pas vide.

- **update_end_date(updateenddate)** :  
  Met à jour la date de fin de la sous-tâche après en avoir validé le format.

- **task_completed(status)** :  
  Met à jour le statut de la sous-tâche (0 = non terminée, 1 = terminée).

- **validate_update_info()** :  
  Vérifie la validité du nom et de la date de fin, ainsi que la cohérence des dates.  
  - En cas de succès, met à jour la sous-tâche dans la base de données.  
  - Émet le signal `validationSuccess` après une mise à jour réussie.

## Modules Python Restants

Ces modules fournissent des fonctions d’aide à la manipulation des données (formatage des dates, gestion des thèmes et des couleurs).
## Sommaire

1. [colors.py](#colorspy)
2. [format_date.py](#format_datepy)  
3. [settings.py](#settingspy)  

## `colors.py`
### Rôle Général
Ce module définit une classe `Colors` qui gère un ensemble de thèmes de couleurs pour l’interface graphique de l’application. Il permet de changer dynamiquement le style couleur principal, et propose différentes déclinaisons (fond, zones claires, foncées, contours, etc.). Chaque style est identifié par un numéro, et l’utilisateur peut faire défiler les différents thèmes.

1. Gérer différents thèmes de couleurs (jusqu’à 12 styles) pour l’interface graphique.
2. Permettre de changer le style courant par le biais du slot `changeStyle()`.
3. Fournir des propriétés réactives (avec `Property` et `Signal`) pour mettre à jour l’interface QML en fonction du thème sélectionné.

### Propriétés Clés

- **style (Property int)** :  
  Numéro courant du style. Passe en revue les styles de 1 à 12.

- **couleur1, couleur2, couleur3, couleur4, couleur5, couleur6, couleur7 (Property str)** :  
  Ces propriétés retournent des codes hexadécimaux de couleurs différentes selon le style courant.  
  - `couleur1` : Couleur du fond.  
  - `couleur2` : Couleur neutre (généralement blanc ou gris pour le thème sombre).  
  - `couleur3` à `couleur5` : Couleurs de plus en plus foncées, utilisées pour les priorités ou certaines zones de l’interface.  
  - `couleur6` : Couleur utilisée pour les contours ou les bordures.  
  - `couleur7` : Couleur très claire, par exemple pour représenter les tâches terminées.


## `format_date.py`
### Rôle Général
Ce module fournit des fonctions utilitaires pour gérer le formatage et la validation des dates dans l’application. Il permet de :

1. Valider une date saisie par l’utilisateur et la convertir dans un format standard.
2. Vérifier la cohérence des dates (même si la fonction `check_dates_consistency` n’est pas complètement implémentée dans le code fourni).
3. Convertir des dates stockées au format "aaaa-mm-jj hh:mm:ss" en un format plus lisible "jj/mm/aaaa" pour l’affichage.

### Fonctions Clés

- **validate_date_format(date_str)** :  
  Valide le format de la date passée en paramètre (attendu : "jj/mm/aaaa") et la convertit en "aaaa-mm-jj 00:00:00".  
  - En cas de format invalide, lève une exception `ValueError` expliquant le format attendu.

- **check_dates_consistency(end_date)** :  
  Prévue pour vérifier la cohérence des dates (par exemple, s’assurer que la date de fin n’est pas antérieure à la date actuelle).  
  - La fonction n’est pas entièrement implémentée dans le code fourni.

- **read_date_format(date_str)** :  
  Convertit une date du format "aaaa-mm-jj hh:mm:ss" en "jj/mm/aaaa".  
  - En cas de problème de format, affiche un message d’erreur et retourne la chaîne originale.

# `settings.py`
Définit l'URL pointant vers le fichier QML `Login.qml`, qui correspond à l'interface de connexion affichée au démarrage de l'application.
