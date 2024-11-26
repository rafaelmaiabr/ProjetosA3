<?php
$dbFile = __DIR__ . '/database.sqlite';

try {
  $pdo = new PDO("sqlite:$dbFile");
  $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

  $createTableQuery = "
    CREATE TABLE IF NOT EXISTS pedidos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT NOT NULL,
      telefone TEXT NOT NULL,
      email TEXT NOT NULL,
      qnt INTEGER NOT NULL,
      comment TEXT NOT NULL,
      type TEXT NOT NULL
    );
  ";
  $pdo->exec($createTableQuery);

} catch (PDOException $e) {
  http_response_code(400);
  echo "Erro ao conectar ao banco de dados: " . $e->getMessage();
}

// Lista pedidos em JSON
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
  $stmt = $pdo->query("SELECT * FROM pedidos");
  $pedidos = $stmt->fetchAll(PDO::FETCH_ASSOC);
  header('Content-Type: application/json');
  echo json_encode($pedidos);
}
?>