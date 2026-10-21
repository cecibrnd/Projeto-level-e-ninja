from app import db


class Usuario(db.Model):
    """Usuário que opera o sistema."""

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(
        db.String(255),
        nullable=False,
        default="",
    )
    nivel = db.Column(
        db.String(30),
        nullable=False,
        default="voluntario",
    )
