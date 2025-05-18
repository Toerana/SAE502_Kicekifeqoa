<?php
// API Orginal
// Charger les informations de connexion à partir d'un fichier de configuration (optionnel) ou définir directement ici
$config = [
    'host' => 'mysql-kicekifeqoa.alwaysdata.net',
    'dbname' => 'kicekifeqoa_todolist',
    'username' => '379269_admin',
    'password' => 'Kicekifeqoa123*'
];

try {
    // Connexion à la base de données avec PDO
    $pdo = new PDO("mysql:host={$config['host']};dbname={$config['dbname']}", $config['username'], $config['password']);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(["error" => "Échec de la connexion à la base de données : " . $e->getMessage()]);
    exit();
}

// Vérifier la méthode de la requête
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
    default:
        http_response_code(405);
        echo json_encode(["error" => "Méthode non autorisée. Utilisez GET, POST ou DELETE."]);
}

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

function handlePost($pdo) {
    $data = json_decode(file_get_contents("php://input"), true);
    $table = $data['table'] ?? null;
    $action = $data['action'] ?? null;

    if ($table && $action) {
        if ($action === 'insert') {
            // Gérer l'insertion
            $columns = implode(", ", array_keys($data['data']));
            $placeholders = implode(", ", array_fill(0, count($data['data']), '?'));
            $stmt = $pdo->prepare("INSERT INTO `$table` ($columns) VALUES ($placeholders)");
            $stmt->execute(array_values($data['data']));
            echo json_encode(["message" => "Données ajoutées avec succès."]);
        } elseif ($action === 'update') {
            // Gérer la mise à jour
            $set = [];
            foreach ($data['data'] as $column => $value) {
                $set[] = "$column = ?";
            }
            $set = implode(", ", $set);
            $column = $data['column'];
            $value = $data['value'];
            $stmt = $pdo->prepare("UPDATE `$table` SET $set WHERE $column = ?");
            $stmt->execute(array_merge(array_values($data['data']), [$value]));
            echo json_encode(["message" => "Données mises à jour avec succès."]);
        } else {
            http_response_code(400);
            echo json_encode(["error" => "Action non reconnue."]);
        }
    } else {
        http_response_code(400);
        echo json_encode(["error" => "Nom de table ou action manquante."]);
    }
}

function handleDelete($pdo) {
    $data = json_decode(file_get_contents("php://input"), true);
    $table = $data['table'] ?? null;
    $column = $data['column'] ?? null;
    $value = $data['value'] ?? null;

    if ($table && $column && $value) {
        $stmt = $pdo->prepare("DELETE FROM `$table` WHERE $column = ?");
        $stmt->execute([$value]);
        echo json_encode(["message" => "Données supprimées avec succès."]);
    } else {
        http_response_code(400);
        echo json_encode(["error" => "Table, colonne ou valeur manquante."]);
    }
}
?>