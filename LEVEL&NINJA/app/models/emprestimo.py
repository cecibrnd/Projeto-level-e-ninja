from datetime import date

from app import db


class Emprestimo(db.Model):
    """Representa um empréstimo de um item do acervo."""

    __tablename__ = "emprestimos"

    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("itens.id"),
        nullable=False,
    )

    solicitante_id = db.Column(
        db.Integer,
        db.ForeignKey("solicitantes.id"),
        nullable=False,
    )

    operador_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False,
    )

    data_retirada = db.Column(
        db.Date,
        default=date.today,
        nullable=False,
    )

    data_prevista_devolucao = db.Column(
        db.Date,
        nullable=False,
    )

    data_devolucao = db.Column(db.Date)

    status = db.Column(
        db.String(20),
        default="ativo",
        nullable=False,
    )

    operador = db.relationship(
        "Usuario",
        backref="emprestimos_operados",
    )
