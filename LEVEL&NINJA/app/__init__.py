from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import Config


# Criação da aplicação.
app = Flask(__name__)
app.config.from_object(Config)

# Extensões utilizadas pelo projeto.
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


# Importamos os modelos e as rotas depois da criação do db
# para evitar problemas de importação circular.
from app import models, routes  # noqa: E402, F401


# Cria as tabelas que ainda não existem no banco.
with app.app_context():
    db.create_all()

    # Se a tabela de coleções estiver vazia, cria as duas coleções padrão.
    # Sem isso, o campo "Coleção" do cadastro de item fica sem opções.
    if models.Colecao.query.count() == 0:
        db.session.add_all([
            models.Colecao(
                nome="LEVEL",
                descricao="Coleção principal do acervo LEVEL.",
            ),
            models.Colecao(
                nome="NINJA",
                descricao="Coleção NINJA integrada ao sistema.",
            ),
        ])
        db.session.commit()
