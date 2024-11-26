@echo off
REM Verifica se o ambiente virtual já está criado
if not exist "crud\venv\Scripts\Activate.ps1" (
  echo Criando ambiente virtual...
  py -m venv crud\venv
)

REM Ativa o ambiente virtual
echo Ativando ambiente virtual...
call .\crud\venv\Scripts\Activate.ps1

REM Acessa o diretório crud
cd crud

REM Inicia a aplicação
echo Iniciando a aplicação...
py main.py