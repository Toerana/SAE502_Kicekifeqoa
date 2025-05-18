<?php
/**
 * API Documentation
 * ==================
 *
 * Ce fichier contient l'implémentation d'une API pour effectuer des opérations
 * CRUD sur une base de données. Il inclut également des mécanismes de chiffrement
 * pour la sécurité des données sensibles.
 *
 * **Détails techniques :**
 * - **Chiffrement :** AES-256-CBC
 * - **Clé de chiffrement :** Hash dérivé en SHA-256
 * - **Vecteur d'initialisation (IV) :** Premiers 16 octets des données chiffrées
 */
// Clé de chiffrement utilisée pour chiffrer le fichier
$key = hash('sha256', 'fd7fbf262118bc9631193efdab5e33adf88530610f7bc8bc7c19f7a3ca76f34d', true); // Clé de 32 octets

/**
 * Configuration des erreurs PHP
 *
 * Configure le fichier de log des erreurs pour faciliter le débogage.
 */
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Définir le chemin du fichier de log des erreurs
$logFile = __DIR__ . '/error_log.log';

// Configurer PHP pour écrire les erreurs dans le fichier spécifié
ini_set('log_errors', 1);
ini_set('error_log', $logFile);
/**
 * Fonction utilitaire pour écrire dans le fichier de log
 *
 * :param string $message: Message à écrire
 */
// Fonction pour afficher les erreurs dans le fichier de log
function logDebugInfo($message) {
    error_log($message);
}
/**
 * Initialisation du chiffrement
 *
 * Génère la clé de chiffrement à partir d'un hash SHA-256.
 */
// Chemin vers le fichier chiffré
$encryptedFile = __DIR__ . '/../db_config.enc';
/**
 * Chargement de la configuration de la base de données
 *
 * Déchiffre et lit le fichier de configuration de la base de données.
 */
if (file_exists($encryptedFile)) {
    // Lire et décoder le contenu du fichier chiffré
    $encryptedData = file_get_contents($encryptedFile);

    // Séparer l'IV et les données chiffrées
    $iv = substr($encryptedData, 0, 16); // Les 16 premiers octets sont l'IV
    $ciphertext = substr($encryptedData, 16); // Le reste est le texte chiffré

    // Déchiffrer les données
    $decryptedData = openssl_decrypt($ciphertext, 'aes-256-cbc', $key, OPENSSL_RAW_DATA, $iv);

    if ($decryptedData === false) {
        http_response_code(500);
        echo json_encode(["error" => "Échec du déchiffrement : " . openssl_error_string()]);
        exit();
    }

    // Vérifiez si $decryptedData est bien une chaîne et contient des données
    if (empty($decryptedData)) {
        http_response_code(500);
        echo json_encode(["error" => "Les données déchiffrées sont vides."]);
        exit();
    }

    // Convertir les données déchiffrées en tableau PHP
    $config = json_decode($decryptedData, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        http_response_code(500);
        echo json_encode(["error" => "Erreur JSON : " . json_last_error_msg()]);
        exit();
    }

    try {
        // Connexion à la base de données avec PDO
        $pdo = new PDO("mysql:host={$config['host']};dbname={$config['dbname']}", $config['username'], $config['password']);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(["error" => "Échec de la connexion à la base de données : " . $e->getMessage()]);
        exit();
    }
} else {
    http_response_code(500);
    echo json_encode(["error" => "Erreur interne, fichier de configuration manquant."]);
    exit();
}
/**
 * Routeur principal
 *
 * Gère les différentes méthodes HTTPS : GET, POST, DELETE, COUNT.
 */
$requestMethod = $_SERVER['REQUEST_METHOD'];
switch ($requestMethod) {
    case 'GET':
        handleGet($pdo);
        break;
    case 'POST':
        handlePost($pdo);
        break;
    case 'DELETE':
        handleDelete($pdo);
        break;
    case 'COUNT':
        handleCount($pdo);
        break;
    default:
        http_response_code(405);
        echo json_encode(["error" => "Méthode non autorisée. Utilisez GET, POST, DELETE ou COUNT."]);
}
/**
 * Gère les requêtes GET
 *
 * Permet de récupérer des données d'une table avec des options de jointure et de filtre.
 *
 * :param PDO $pdo: Connexion à la base de données
 */
function handleGet($pdo) {
    $table = $_GET['table'] ?? null;
    $columns = $_GET['columns'] ?? '*'; // Par défaut, toutes les colonnes
    $filterColumn = $_GET['filter_column'] ?? null;
    $filterValue = $_GET['filter_value'] ?? null;
    $joinTables = $_GET['join_table'] ?? null; // Pour les tables à joindre
    $joinConditions = $_GET['join_condition'] ?? null; // Pour les conditions de jointure

    if ($table) {
        // Début de la requête SQL
        $query = "SELECT $columns FROM `$table`";

        // Ajouter des jointures si spécifié
        if ($joinTables && $joinConditions) {
            $joinTablesArray = explode(",", $joinTables);
            $joinConditionsArray = explode(",", $joinConditions);
            foreach ($joinTablesArray as $index => $joinTable) {
                $query .= " JOIN `$joinTable` ON $joinConditionsArray[$index]";
            }
        }

        // Ajouter un filtre si une colonne et une valeur de filtre sont spécifiées
        if ($filterColumn && $filterValue !== null) {
            $query .= " WHERE $filterColumn = :filterValue";
            $stmt = $pdo->prepare($query);

            // Déterminer le type de la colonne pour binder la valeur
            if (is_numeric($filterValue)) {
                $stmt->bindValue(':filterValue', (int)$filterValue, PDO::PARAM_INT);
            } else {
                $stmt->bindValue(':filterValue', $filterValue, PDO::PARAM_STR);
            }
        } else {
            $stmt = $pdo->prepare($query);
        }

        try {
            $stmt->execute();
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
            header('Content-Type: application/json');
            echo json_encode($result);
        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(["error" => "Erreur lors de la récupération des données : " . $e->getMessage()]);
        }
    } else {
        http_response_code(400);
        echo json_encode(["error" => "Nom de table manquant."]);
    }
}
/**
 * Gère les requêtes POST
 *
 * Permet l'ajout de nouvelles données dans la base.
 *
 * :param PDO $pdo: Connexion à la base de données
 * :raises PDOException: En cas d'échec de l'insertion
 */
function handlePost($pdo) {
    $data = json_decode(file_get_contents("php://input"), true);
    $table = $data['table'] ?? null;
    $action = $data['action'] ?? null;

    if ($table && $action) {
        if ($action === 'insert') {
            // Gérer l'insertion simple
            $columns = implode(", ", array_keys($data['data']));
            $placeholders = implode(", ", array_fill(0, count($data['data']), '?'));
            $stmt = $pdo->prepare("INSERT INTO `$table` ($columns) VALUES ($placeholders)");
            $stmt->execute(array_values($data['data']));
            echo json_encode(["message" => "Données ajoutées avec succès."]);
        } elseif ($action === 'add_recup') {
            // Ajouter et récupérer l'ID généré
            try {
                $columns = implode(", ", array_keys($data['data']));
                $placeholders = implode(", ", array_fill(0, count($data['data']), '?'));
                $stmt = $pdo->prepare("INSERT INTO `$table` ($columns) VALUES ($placeholders)");
                $stmt->execute(array_values($data['data']));

                // Récupérer l'ID généré
                $lastId = $pdo->lastInsertId();

                echo json_encode([
                    "message" => "Données ajoutées avec succès.",
                    "id" => $lastId
                ]);
            } catch (PDOException $e) {
                http_response_code(500);
                echo json_encode(["error" => "Erreur lors de l'insertion : " . $e->getMessage()]);
            }
        } elseif ($action === 'update') {
            // Gérer la mise à jour
            try {
                if (empty($data['data']) || empty($data['column']) || !isset($data['value'])) {
                    http_response_code(400);
                    echo json_encode(["error" => "Données, colonne ou valeur manquantes."]);
                    return;
                }

                $set = [];
                foreach ($data['data'] as $column => $value) {
                    $set[] = "`$column` = ?";
                }
                $set = implode(", ", $set);
                $column = $data['column'];
                $value = $data['value'];
                $query = "UPDATE `$table` SET $set WHERE `$column` = ?";

                $stmt = $pdo->prepare($query);
                $stmt->execute(array_merge(array_values($data['data']), [$value]));

                if ($stmt->rowCount() > 0) {
                    echo json_encode(["message" => "Données mises à jour avec succès."]);
                } else {
                    http_response_code(404);
                    echo json_encode(["error" => "Aucune donnée n'a été mise à jour."]);
                }
            } catch (PDOException $e) {
                http_response_code(500);
                echo json_encode(["error" => "Erreur lors de la mise à jour : " . $e->getMessage()]);
            }
        } else {
            http_response_code(400);
            echo json_encode(["error" => "Action non reconnue."]);
        }
    } else {
        http_response_code(400);
        echo json_encode(["error" => "Nom de table ou action manquante."]);
    }
}
/**
 * Gère les requêtes DELETE
 *
 * Permet la suppression de données dans une table spécifique.
 *
 * :param PDO $pdo: Connexion à la base de données
 * :raises PDOException: En cas d'échec de la suppression
 */
function handleDelete($pdo) {
    $data = json_decode(file_get_contents("php://input"), true);
    $table = $data['table'] ?? null;
    $column = $data['column'] ?? null;
    $value = $data['value'] ?? null;

    if ($table && $column && $value) {
        $stmt = $pdo->prepare("DELETE FROM `$table` WHERE $column = ?");
        $stmt->execute([$value]);
        echo json_encode(["message"     => "Données supprimées avec succès."]);
    } else {
        http_response_code(400);
        echo json_encode(["error" => "Table, colonne ou valeur manquante."]);
    }
}
/**
 * Gère les requêtes COUNT
 *
 * Retourne le nombre d'enregistrements dans une table spécifique.
 *
 * :param PDO $pdo: Connexion à la base de données
 * :raises PDOException: En cas d'échec de la requête
 */
function handleCount($pdo) {
    $table = $_GET['table'] ?? null;
    $filterColumn = $_GET['filter_column'] ?? null;
    $filterValue = $_GET['filter_value'] ?? null;

    if ($table && $filterColumn) {
        // Requête pour compter les occurrences
        $query = "SELECT COUNT(*) AS count FROM `$table` WHERE $filterColumn = :filterValue";
        $stmt = $pdo->prepare($query);
        $stmt->bindValue(':filterValue', $filterValue);

        try {
            $stmt->execute();
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            header('Content-Type: application/json');
            echo json_encode($result);
        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(["error" => "Erreur lors du comptage des données : " . $e->getMessage()]);
        }
    } else {
        http_response_code(400);
        echo json_encode(["error" => "Nom de table ou colonne de filtre manquante."]);
    }
}
?>
