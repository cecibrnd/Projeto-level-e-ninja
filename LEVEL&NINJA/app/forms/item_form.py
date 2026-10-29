from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional


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
        "SKU",
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

    quantidade = IntegerField(
        "Quantidade",
        default=1,
        validators=[
            DataRequired(message="Informe a quantidade."),
            NumberRange(min=1, message="A quantidade deve ser pelo menos 1."),
        ],
    )

    imagem = FileField(
        "Imagem do item",
        validators=[
            Optional(),
            FileAllowed(
                ["jpg", "jpeg", "png", "gif", "webp"],
                "Envie uma imagem (jpg, png, gif ou webp).",
            ),
        ],
    )

    disponivel = BooleanField(
        "Disponível para empréstimo",
        default=True,
    )

    submit = SubmitField("Salvar item")
