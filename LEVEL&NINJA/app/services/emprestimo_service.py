from datetime import date

from app import db
from app.models import Emprestimo, Item, Solicitante, Usuario


class EmprestimoService:
    """Regras relacionadas aos empréstimos."""

    @staticmethod
    def registrar(item_ids, solicitante_id, operador_id, data_prevista):
        """Registra o empréstimo de um ou vários itens de uma vez.

        Tudo ou nada: se qualquer validação falhar, nenhum empréstimo
        é gravado. Lança ValueError com uma mensagem amigável.
        """
        item_ids = set(item_ids)

        if not item_ids:
            raise ValueError("Selecione pelo menos um item.")

        if data_prevista < date.today():
            raise ValueError(
                "A data prevista de devolução não pode estar no passado."
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
                    data_prevista_devolucao=data_prevista,
                )
            )
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
