from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class EmprestimoForm(FlaskForm):
    """Formulário da página de registrar empréstimo."""

    solicitante_nome = StringField(
        "Nome de quem pegou",
        validators=[
            DataRequired(message="Digite o nome de quem pegou o item."),
            Length(max=120),
        ],
    )

    operador_nome = StringField(
        "Nome de quem realizou o empréstimo",
        validators=[
            DataRequired(message="Digite o nome de quem realizou o empréstimo."),
            Length(max=120),
        ],
    )

    data_emprestimo = DateField(
        "Data do empréstimo",
        format="%Y-%m-%d",
        validators=[DataRequired(message="Informe a data do empréstimo.")],
    )

    data_devolucao = DateField(
        "Data de devolução",
        format="%Y-%m-%d",
        validators=[DataRequired(message="Informe a data de devolução.")],
    )

    status = SelectField(
        "Status",
        choices=[
            ("ativo", "Ativo (em andamento)"),
            ("devolvido", "Devolvido"),
        ],
        validators=[DataRequired(message="Selecione o status.")],
    )

    submit = SubmitField("Confirmar empréstimo")
