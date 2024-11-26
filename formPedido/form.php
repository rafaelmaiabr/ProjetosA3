<?php
$dbFile = __DIR__ . '/database.sqlite';

// Criar ou abrir o banco de dados
try {
  $pdo = new PDO("sqlite:$dbFile");
  $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

  // Criar a tabela pedidos se não existir
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

  // echo "Banco de dados criado ou conectado com sucesso e tabela criada!";

} catch (PDOException $e) {
  http_response_code(400);
  echo "Erro ao conectar ao banco de dados: " . $e->getMessage();
}

$name = $_POST['name'] ?? false;
$phone = $_POST['phone'] ?? false;
$email = $_POST['email'] ?? false;
$qnt = $_POST['qnt'] ?? false;
$comment = $_POST['comment'] ?? false;
$type = $_POST['type'] ?? 'indefinido';

if ($name && $phone && $email && $qnt && $comment && $type) {

  // Prepara a consulta SQL para inserir os dados
  $stmt = $pdo->prepare("INSERT INTO pedidos (nome, telefone, email, qnt, comment, type) VALUES (:nome, :telefone, :email, :qnt, :comment, :type)");
  $stmt->bindParam(':nome', $name);
  $stmt->bindParam(':telefone', $phone);
  $stmt->bindParam(':email', $email);
  $stmt->bindParam(':qnt', $qnt);
  $stmt->bindParam(':comment', $comment);
  $stmt->bindParam(':type', $type);

  // Executa a consulta
  if ($stmt->execute()) {
      echo "Pedido enviado com sucesso!";
  } else {
      http_response_code(500); // Define o código de status HTTP para 500 (Internal Server Error)
      echo "Erro ao enviar o pedido.";
  }

} else {
  http_response_code(400);
  echo "Erro: Todos os campos são obrigatórios.";
}

