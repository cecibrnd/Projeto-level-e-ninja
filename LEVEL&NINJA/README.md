# LEVEL Board — Base organizada

Sistema web para gerenciamento do acervo LEVEL e NINJA.

## Estrutura

```text
LEVEL_Board/
├── app/
│   ├── forms/
│   ├── models/
│   ├── services/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   ├── __init__.py
│   └── routes.py
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## Para executar

1. Abra o PowerShell na pasta do projeto.
2. Ative o ambiente virtual:

```powershell
.\venv\Scripts\activate.bat
```

3. Instale as dependências, se necessário:

```powershell
pip install -r requirements.txt
```

4. Confira o usuário, a senha e o nome do banco no `config.py`.

5. Inicie o sistema:

```powershell
flask run
```

Depois, abra `http://127.0.0.1:5000` no navegador.

## Banco de dados

O projeto usa MySQL. O `config.py` possui as configurações:

- `DB_USERNAME`: usuário do MySQL.
- `DB_PASSWORD`: senha do MySQL.
- `DB_NAME`: nome do banco.
- `SECRET_KEY`: chave usada pelo Flask.

Também é possível definir essas configurações por variáveis de ambiente.

## Organização do código

- `models/`: representa as tabelas do banco.
- `forms/`: formulários HTML com Flask-WTF.
- `services/`: regras de negócio.
- `routes.py`: recebe as requisições e chama os serviços.
- `templates/`: páginas HTML.
- `static/css/`: estilos.
- `static/js/`: JavaScript.

## Observação sobre o banco

O Flask chama `db.create_all()` ao iniciar. Portanto, o banco configurado precisa existir no MySQL e o usuário informado no `config.py` precisa ter permissão para acessá-lo.
