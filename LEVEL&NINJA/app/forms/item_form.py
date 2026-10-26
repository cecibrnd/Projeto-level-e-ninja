from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional


class ItemForm(FlaskForm):
    """Formulário para cadastro de itens."""

    nome = StringField(
        "Nome do item",
        validators=[
            DataRequired(),
            Length(max=120),
        ],
    )

    descricao = TextAreaField(
        "Descrição",
        validators=[Optional()],
    )

    categoria = StringField(
        "Categoria",
        validators=[
            Optional(),
            Length(max=80),
        ],
    )

    origem_doador = StringField(
        "Origem / Doador",
        validators=[
            Optional(),
            Length(max=120),
        ],
    )

    tipo = StringField(
        "Tipo",
        validators=[
            Optional(),
            Length(max=80),
        ],
    )

    codigo = StringField(
        "SKU / QR Code",
        validators=[
            Optional(),
            Length(max=80),
        ],
    )

    observacoes = TextAreaField(
        "Observações",
        validators=[Optional()],
    )

    colecao_id = SelectField(
        "Coleção",
        coerce=int,
        validators=[DataRequired()],
    )

    imagem = StringField(
        "Imagem (URL ou caminho)",
        validators=[
            Optional(),
            Length(max=255),
        ],
    )

    disponivel = BooleanField(
        "Disponível para empréstimo",
        default=True,
    )

    submit = SubmitField("Salvar item")
