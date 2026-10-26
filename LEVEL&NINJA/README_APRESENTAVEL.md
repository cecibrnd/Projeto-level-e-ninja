# LEVEL Board — Base Apresentável

Esta versão mantém o `venv` original do projeto e melhora a apresentação visual.

## Executar no Windows PowerShell

1. Entre na pasta do projeto.
2. Ative o ambiente:
   `.env\Scripts\Activate.ps1`
3. Instale dependências, se necessário:
   `pip install -r requirements.txt`
4. Confirme que o MySQL possui o banco:
   `CREATE DATABASE level_board;`
5. Rode:
   `flask run`
6. Abra:
   `http://127.0.0.1:5000`

O CSS fica em `app/static/css/custom.css`.
