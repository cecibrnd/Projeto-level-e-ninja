from app import db


class Item(db.Model):
    """Representa um item disponível no acervo."""

    __tablename__ = "itens"

    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(255))
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(80))
    origem_doador = db.Column(db.String(120))
    tipo = db.Column(db.String(80))
    codigo = db.Column(db.String(80), unique=True)
    quantidade = db.Column(db.Integer, default=1, nullable=False)
    observacoes = db.Column(db.Text)
    disponivel = db.Column(db.Boolean, default=True, nullable=False)

    colecao_id = db.Column(
        db.Integer,
        db.ForeignKey("colecoes.id"),
        nullable=False,
    )

    emprestimos = db.relationship(
        "Emprestimo",
        backref="item",
        lazy=True,
    )
