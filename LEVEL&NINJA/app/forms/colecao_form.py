from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from app import db
from app.models import Colecao


class ColecaoForm(FlaskForm):
    """Formulário para criar uma nova coleção."""

    nome = StringField(
        "Nome da coleção",
        validators=[
            DataRequired(message="Informe o nome da coleção."),
            Length(max=80),
        ],
    )

    descricao = StringField(
        "Descrição",
        validators=[
            Optional(),
            Length(max=255),
        ],
    )

    submit = SubmitField("Criar coleção")

    def validate_nome(self, campo):
        """Impede duas coleções com o mesmo nome (sem diferenciar maiúsculas)."""
        nome = (campo.data or "").strip()
        existe = Colecao.query.filter(
            db.func.lower(Colecao.nome) == nome.lower()
        ).first()

        if existe:
            raise ValidationError("Já existe uma coleção com esse nome.")
