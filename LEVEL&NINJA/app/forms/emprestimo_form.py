from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired


class EmprestimoForm(FlaskForm):
    """Formulário da página de registrar empréstimo."""

    solicitante_id = SelectField(
        "Nome de quem pegou",
        coerce=int,
        validators=[DataRequired(message="Selecione quem pegou o item.")],
    )

    operador_id = SelectField(
        "Nome de quem realizou o empréstimo",
        coerce=int,
        validators=[DataRequired(message="Selecione quem realizou o empréstimo.")],
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
