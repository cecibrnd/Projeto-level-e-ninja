from app import db
from app.models import Colecao


class ColecaoService:
    """Regras relacionadas às coleções."""

    @staticmethod
    def cadastrar(nome, descricao=None):
        """Cria uma nova coleção ativa."""
        colecao = Colecao(
            nome=nome.strip(),
            descricao=(descricao or "").strip() or None,
        )

        db.session.add(colecao)
        db.session.commit()

        return colecao
