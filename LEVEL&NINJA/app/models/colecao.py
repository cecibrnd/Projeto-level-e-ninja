from app import db


class Colecao(db.Model):
    """Representa uma coleção do acervo."""

    __tablename__ = "colecoes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
    )
    descricao = db.Column(db.String(255))
    ativa = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )

    itens = db.relationship(
        "Item",
        backref="colecao",
        lazy=True,
    )
