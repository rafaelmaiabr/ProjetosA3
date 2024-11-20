# 1 Inicializar ambiente virtual para rodar o projeto (powershell)
Caso não tenha o ambiente venv, instale usando o comando `py -m venv venv`
`.\crud\venv\Scripts\Activate.ps1`
`py crud\main.py`

Caso o comando não funcione, execute abrir powershell como admin e executar.
`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
Após isto, volte no terminal do projeto e rode o `activate.ps1`

# Estrutura CRUD

```paintext
project_root/
│
├── main.py                # Arquivo principal para rodar a aplicação
├── app/
│   ├── __init__.py        # Inicializador da aplicação Flask
│   ├── routes.py          # Rotas para as funcionalidades da API
│   ├── services/
│   │   ├── __init__.py
│   │   ├── audio_extraction.py   # Função para extrair áudio do vídeo
│   │   ├── audio_processing.py   # Funções para dividir áudio e transcrever
│   │   └── cleanup.py            # Função para excluir chunks de áudio
├── static/
│   └── css/
│       └── styles.css     # Arquivo de estilos adicionais, se necessário
└── templates/
    └── index.html         # Frontend da aplicação com Bootstrap
```




