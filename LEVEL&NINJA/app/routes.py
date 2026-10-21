from datetime import date, timedelta

from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app import app, db
from app.forms.item_form import ItemForm
from app.models import (
    Colecao,
    Emprestimo,
    Item,
    Solicitante,
    Usuario,
)
from app.services.emprestimo_service import EmprestimoService
from app.services.item_service import ItemService


@app.context_processor
def utilidades():
    """Disponibiliza datas úteis para todos os templates."""
    return {
        "ano_atual": date.today().year,
        "today": date.today(),
    }


@app.route("/")
def dashboard():
    """Exibe os principais indicadores do sistema."""
    emprestimos_ativos = Emprestimo.query.filter_by(
        status="ativo"
    ).count()

    emprestimos_atrasados = Emprestimo.query.filter(
        Emprestimo.status == "ativo",
        Emprestimo.data_prevista_devolucao < date.today(),
    ).count()

    dados = {
        "itens": Item.query.count(),
        "disponiveis": Item.query.filter_by(
            disponivel=True
        ).count(),
        "emprestimos_ativos": emprestimos_ativos,
        "emprestimos_atrasados": emprestimos_atrasados,
    }

    recentes = (
        Emprestimo.query
        .order_by(Emprestimo.id.desc())
        .limit(6)
        .all()
    )

    return render_template(
        "dashboard.html",
        dados=dados,
        recentes=recentes,
    )


@app.route("/acervo")
def acervo():
    """Exibe o acervo e permite pesquisar itens."""
    termo = request.args.get("q", "")
    colecao_id = request.args.get(
        "colecao",
        type=int,
    )

    itens = ItemService.buscar(
        termo,
        colecao_id,
    )

    colecoes = (
        Colecao.query
        .filter_by(ativa=True)
        .order_by(Colecao.nome)
        .all()
    )

    solicitantes = Solicitante.query.order_by(Solicitante.nome).all()
    operadores = Usuario.query.order_by(Usuario.nome).all()

    return render_template(
        "acervo/lista.html",
        itens=itens,
        colecoes=colecoes,
        termo=termo,
        colecao_id=colecao_id,
        solicitantes=solicitantes,
        operadores=operadores,
        data_padrao=(date.today() + timedelta(days=7)).isoformat(),
    )


@app.route("/itens/cadastrar", methods=["GET", "POST"])
def cadastrar_item():
    """Exibe e processa o formulário de cadastro de item."""
    form = ItemForm()

    colecoes = (
        Colecao.query
        .filter_by(ativa=True)
        .order_by(Colecao.nome)
        .all()
    )

    form.colecao_id.choices = [
        (colecao.id, colecao.nome)
        for colecao in colecoes
    ]

    if form.validate_on_submit():
        dados = {
            "nome": form.nome.data.strip(),
            "descricao": form.descricao.data,
            "categoria": form.categoria.data,
            "origem_doador": form.origem_doador.data,
            "tipo": form.tipo.data,
            "codigo": form.codigo.data or None,
            "observacoes": form.observacoes.data,
            "colecao_id": form.colecao_id.data,
            "imagem": form.imagem.data,
            "disponivel": form.disponivel.data,
        }

        try:
            ItemService.cadastrar(dados)
            flash(
                "Item cadastrado com sucesso!",
                "success",
            )
            return redirect(url_for("acervo"))

        except Exception as erro:
            db.session.rollback()
            flash(
                f"Não foi possível cadastrar o item: {erro}",
                "danger",
            )

    return render_template(
        "item/cadastrar.html",
        form=form,
    )


@app.route("/itens/<int:item_id>")
def detalhe_item(item_id):
    """Exibe os detalhes e o histórico de um item."""
    item = db.get_or_404(Item, item_id)

    historico = (
        Emprestimo.query
        .filter_by(item_id=item.id)
        .order_by(Emprestimo.data_retirada.desc())
        .all()
    )

    return render_template(
        "item/detalhe.html",
        item=item,
        historico=historico,
    )


@app.route("/emprestimos")
def emprestimos():
    """Lista todos os empréstimos."""
    registros = (
        Emprestimo.query
        .order_by(Emprestimo.id.desc())
        .all()
    )

    return render_template(
        "emprestimo/lista.html",
        emprestimos=registros,
    )


@app.route("/emprestimos/registrar", methods=["POST"])
def registrar_emprestimos():
    """Registra o empréstimo dos itens selecionados no acervo."""
    # Guardamos a pesquisa atual para voltar ao mesmo resultado se der erro.
    voltar = url_for(
        "acervo",
        q=request.form.get("q") or None,
        colecao=request.form.get("colecao", type=int),
    )

    try:
        item_ids = [int(i) for i in request.form.getlist("item_ids")]
        solicitante_id = int(request.form.get("solicitante_id", ""))
        operador_id = int(request.form.get("operador_id", ""))
        data_prevista = date.fromisoformat(
            request.form.get("data_prevista_devolucao", "")
        )
    except ValueError:
        flash("Preencha todos os campos corretamente.", "danger")
        return redirect(voltar)

    try:
        itens, solicitante = EmprestimoService.registrar(
            item_ids,
            solicitante_id,
            operador_id,
            data_prevista,
        )
    except ValueError as erro:
        db.session.rollback()
        flash(str(erro), "danger")
        return redirect(voltar)
    except Exception as erro:
        db.session.rollback()
        flash(f"Não foi possível registrar o empréstimo: {erro}", "danger")
        return redirect(voltar)

    flash(
        f"{len(itens)} item(ns) emprestado(s) para {solicitante.nome}.",
        "success",
    )
    return redirect(url_for("emprestimos"))


@app.route(
    "/emprestimos/<int:emprestimo_id>/devolver",
    methods=["POST"],
)
def devolver_emprestimo(emprestimo_id):
    """Registra a devolução de um empréstimo."""
    emprestimo = db.get_or_404(
        Emprestimo,
        emprestimo_id,
    )

    EmprestimoService.devolver(emprestimo)

    flash(
        "Devolução registrada com sucesso!",
        "success",
    )

    return redirect(url_for("emprestimos"))


@app.route("/colecoes")
def colecoes():
    """Lista as coleções cadastradas."""
    lista = (
        Colecao.query
        .order_by(Colecao.nome)
        .all()
    )

    return render_template(
        "colecoes.html",
        colecoes=lista,
    )


@app.route("/usuarios")
def usuarios():
    """Lista os usuários do sistema."""
    lista = (
        Usuario.query
        .order_by(Usuario.nome)
        .all()
    )

    return render_template(
        "usuarios.html",
        usuarios=lista,
    )


@app.route("/solicitantes")
def solicitantes():
    """Lista os solicitantes."""
    lista = (
        Solicitante.query
        .order_by(Solicitante.nome)
        .all()
    )

    return render_template(
        "solicitantes.html",
        solicitantes=lista,
    )
