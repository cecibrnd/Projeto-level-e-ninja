from app import db
from app.models import Item


class ItemService:
    """Regras relacionadas aos itens do acervo."""

    @staticmethod
    def buscar(termo="", colecao_id=None):
        """Busca itens por texto e/ou coleção."""
        query = Item.query

        if termo:
            termo = f"%{termo.strip()}%"

            query = query.filter(
                db.or_(
                    Item.nome.ilike(termo),
                    Item.categoria.ilike(termo),
                    Item.tipo.ilike(termo),
                    Item.codigo.ilike(termo),
                )
            )

        if colecao_id:
            query = query.filter_by(
                colecao_id=colecao_id,
            )

        return query.order_by(Item.nome).all()

    @staticmethod
    def cadastrar(dados):
        """Cadastra um novo item."""
        item = Item(**dados)

        db.session.add(item)
        db.session.commit()

        return item
