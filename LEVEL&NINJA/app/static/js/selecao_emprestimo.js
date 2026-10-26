// Seleção de itens no acervo para registrar empréstimos em lote.
(function () {
    var barra = document.getElementById("barra-selecao");
    if (!barra) return;

    var contador = document.getElementById("contador-selecao");
    var checks = Array.prototype.slice.call(
        document.querySelectorAll(".item-check")
    );

    function atualizar() {
        var marcados = checks.filter(function (c) { return c.checked; });

        contador.textContent = marcados.length;
        barra.classList.toggle("d-none", marcados.length === 0);

        // Destaca o card selecionado.
        checks.forEach(function (c) {
            c.closest(".item-card").classList.toggle("item-card-selecionado", c.checked);
        });
    }

    checks.forEach(function (c) { c.addEventListener("change", atualizar); });

    var todos = document.getElementById("btn-selecionar-todos");
    if (todos) {
        todos.addEventListener("click", function () {
            var todosMarcados = checks.length > 0 && checks.every(function (c) { return c.checked; });
            checks.forEach(function (c) { c.checked = !todosMarcados; });
            atualizar();
        });
    }

    document.getElementById("btn-limpar-selecao").addEventListener("click", function () {
        checks.forEach(function (c) { c.checked = false; });
        atualizar();
    });

    // Ao voltar para a página (botão "voltar" do navegador) mantém o estado coerente.
    atualizar();
})();
