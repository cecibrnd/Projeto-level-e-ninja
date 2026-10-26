from datetime import date

from app import db
from app.models import Emprestimo, Item, Solicitante, Usuario

STATUS_VALIDOS = ("ativo", "devolvido")


class EmprestimoService:
    """Regras relacionadas aos empréstimos."""

    @staticmethod
    def registrar(
        item_ids,
        solicitante_id,
        operador_id,
        data_retirada,
        data_prevista,
        status="ativo",
    ):
        """Registra o empréstimo de um ou vários itens de uma vez.

        Tudo ou nada: se qualquer validação falhar, nenhum empréstimo
        é gravado. Lança ValueError com uma mensagem amigável.

        - status "ativo": o item fica indisponível até ser devolvido.
        - status "devolvido": registro de um empréstimo que já terminou;
          o item continua disponível.
        """
        item_ids = set(item_ids)
        hoje = date.today()

        if not item_ids:
            raise ValueError("Selecione pelo menos um item.")

        if status not in STATUS_VALIDOS:
            raise ValueError("Status inválido.")

        if data_retirada > hoje:
            raise ValueError(
                "A data do empréstimo não pode estar no futuro."
            )

        if data_prevista < data_retirada:
            raise ValueError(
                "A data de devolução não pode ser anterior "
                "à data do empréstimo."
            )

        if status == "ativo" and data_prevista < hoje:
            raise ValueError(
                "A data de devolução de um empréstimo ativo "
                "não pode estar no passado."
            )

        if status == "devolvido" and data_prevista > hoje:
            raise ValueError(
                "Um empréstimo devolvido não pode ter "
                "data de devolução no futuro."
            )

        solicitante = db.session.get(Solicitante, solicitante_id)
        if solicitante is None:
            raise ValueError("Solicitante não encontrado.")

        operador = db.session.get(Usuario, operador_id)
        if operador is None:
            raise ValueError("Operador não encontrado.")

        # with_for_update trava as linhas até o commit, evitando que duas
        # pessoas emprestem o mesmo item ao mesmo tempo.
        itens = (
            Item.query
            .filter(Item.id.in_(item_ids))
            .with_for_update()
            .all()
        )

        if len(itens) != len(item_ids):
            raise ValueError("Algum item selecionado não existe mais.")

        if status == "ativo":
            indisponiveis = [i.nome for i in itens if not i.disponivel]
            if indisponiveis:
                raise ValueError(
                    "Itens indisponíveis para empréstimo: "
                    + ", ".join(indisponiveis)
                    + "."
                )

        for item in itens:
            db.session.add(
                Emprestimo(
                    item_id=item.id,
                    solicitante_id=solicitante.id,
                    operador_id=operador.id,
                    data_retirada=data_retirada,
                    data_prevista_devolucao=data_prevista,
                    data_devolucao=(
                        data_prevista if status == "devolvido" else None
                    ),
                    status=status,
                )
            )

            if status == "ativo":
                item.disponivel = False

        db.session.commit()

        return itens, solicitante

    @staticmethod
    def devolver(emprestimo):
        """Registra a devolução de um empréstimo."""
        emprestimo.status = "devolvido"
        emprestimo.data_devolucao = date.today()
        emprestimo.item.disponivel = True

        db.session.commit()
