from datetime import date, timedelta

from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app import app, db
from app.forms.colecao_form import ColecaoForm
from app.forms.emprestimo_form import EmprestimoForm
from app.forms.item_form import ItemForm
from app.models import (
    Colecao,
    Emprestimo,
    Item,
    Solicitante,
    Usuario,
)
from app.services.colecao_service import ColecaoService
from app.services.emprestimo_service import EmprestimoService
from app.services.item_service import ItemService


@app.context_processor
def utilidades():
    """Disponibiliza datas úteis para todos os templates."""
    return {
        "ano_atual": date.today().year,
        "today": date.today(),
    }


# Cores usadas para diferenciar as coleções (SB Admin 2).
# A cor depende do id, então não muda quando novas coleções são criadas.
CORES_COLECAO = ["primary", "success", "info", "warning", "danger", "secondary"]


@app.template_filter("cor_colecao")
def cor_colecao(colecao_id):
    """Devolve o nome da cor da coleção a partir do id dela."""
    return CORES_COLECAO[(colecao_id - 1) % len(CORES_COLECAO)]


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

    return render_template(
        "acervo/lista.html",
        itens=itens,
        colecoes=colecoes,
        termo=termo,
        colecao_id=colecao_id,
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


@app.route("/emprestimos/novo", methods=["GET", "POST"])
def novo_emprestimo():
    """Página para registrar o empréstimo dos itens marcados no acervo.

    O acervo envia os itens por GET (?item_ids=1&item_ids=2). Ao salvar,
    o próprio formulário reenvia os ids em campos ocultos.
    """
    try:
        item_ids = [int(i) for i in request.values.getlist("item_ids")]
    except ValueError:
        item_ids = []

    itens = []
    if item_ids:
        itens = (
            Item.query
            .filter(Item.id.in_(item_ids))
            .order_by(Item.nome)
            .all()
        )

    if not itens:
        flash(
            "Marque pelo menos um item no acervo para registrar "
            "o empréstimo.",
            "warning",
        )
        return redirect(url_for("acervo"))

    solicitantes = Solicitante.query.order_by(Solicitante.nome).all()
    operadores = Usuario.query.order_by(Usuario.nome).all()

    form = EmprestimoForm()
    form.solicitante_id.choices = [(0, "Selecione...")] + [
        (s.id, f"{s.nome} ({s.tipo})") for s in solicitantes
    ]
    form.operador_id.choices = [(0, "Selecione...")] + [
        (u.id, u.nome) for u in operadores
    ]

    # Valores iniciais só na primeira abertura da página.
    if request.method == "GET":
        form.data_emprestimo.data = date.today()
        form.data_devolucao.data = date.today() + timedelta(days=7)
        form.status.data = "ativo"

    if form.validate_on_submit():
        try:
            itens_emprestados, solicitante = EmprestimoService.registrar(
                [i.id for i in itens],
                form.solicitante_id.data,
                form.operador_id.data,
                form.data_emprestimo.data,
                form.data_devolucao.data,
                form.status.data,
            )
        except ValueError as erro:
            db.session.rollback()
            flash(str(erro), "danger")
        except Exception as erro:
            db.session.rollback()
            flash(
                f"Não foi possível registrar o empréstimo: {erro}",
                "danger",
            )
        else:
            flash(
                f"{len(itens_emprestados)} item(ns) emprestado(s) "
                f"para {solicitante.nome}.",
                "success",
            )
            return redirect(url_for("emprestimos"))

    return render_template(
        "emprestimo/novo.html",
        form=form,
        itens=itens,
        sem_cadastros=not solicitantes or not operadores,
    )


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


@app.route("/colecoes/nova", methods=["GET", "POST"])
def nova_colecao():
    """Exibe e processa o formulário de nova coleção."""
    form = ColecaoForm()

    if form.validate_on_submit():
        try:
            colecao = ColecaoService.cadastrar(
                form.nome.data,
                form.descricao.data,
            )
        except Exception as erro:
            db.session.rollback()
            flash(
                f"Não foi possível criar a coleção: {erro}",
                "danger",
            )
        else:
            flash(
                f"Coleção {colecao.nome} criada! "
                "Ela já aparece nos filtros do Acervo.",
                "success",
            )
            return redirect(url_for("colecoes"))

    return render_template(
        "colecao/nova.html",
        form=form,
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
