from app import db


class Solicitante(db.Model):
    """Pessoa que pode realizar empréstimos."""

    __tablename__ = "solicitantes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(30), nullable=False)
    identificacao = db.Column(db.String(80))
    contato = db.Column(db.String(120))

    emprestimos = db.relationship(
        "Emprestimo",
        backref="solicitante",
        lazy=True,
    )
