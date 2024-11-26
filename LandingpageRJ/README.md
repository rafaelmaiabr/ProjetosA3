# Inicializar o projeto

1. Na raiz do projeto `PROJETOSA3`
2. Inicialize o PHP `php -S localhost:8080`
3. Acesse a página de turismo `http://localhost:8080/LandingpageRJ/index.html`

# Banco de dados

Com o intuito de facilitar a execução do projeto, optei por utilizar o SQLLITE.
Ao acessar o arquivo `formPedido\form.php` ou `formPedido\pedidos.php`. O sistema valida se atabela de pedidos existe.

Em caso de erro no acesso o usuário receberá uma notificação.

## Armazenamento dos registros no SQLITE
Os dados são armazenados em arquivo `formPedido\database.sqlite`.

## Lista dos pedidos
É possível visualizar os registros acessando a rota `http://localhost:8080/formPedido/pedidos.php`

## Excluindo registros
Para remover, os registros basta apagar todos os dados do arquivo `formPedido\database.sqlite`

