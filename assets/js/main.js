/*
 * Desata — comportamentos do site
 * Tudo aqui é progressivo: sem JavaScript, a página continua legível e navegável.
 */
(function () {
  "use strict";

  var config = window.DESATA_CONFIG || {};
  var semMovimento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- 1. Contato (WhatsApp, e-mail, Instagram) ---------- */
  function soDigitos(valor) {
    return String(valor || "").replace(/\D/g, "");
  }

  function aplicarContatos() {
    var faltando = [];
    var numero = soDigitos(config.whatsapp);
    var email = (config.email || "").trim();
    var instagram = (config.instagram || "").trim().replace(/^@/, "");
    var local = (config.local || "").trim();

    // WhatsApp
    var linksZap = document.querySelectorAll('[data-contato="whatsapp"]');
    if (numero) {
      var url = "https://wa.me/" + numero;
      if (config.whatsappMensagem) {
        url += "?text=" + encodeURIComponent(config.whatsappMensagem);
      }
      Array.prototype.forEach.call(linksZap, function (a) {
        a.href = url;
        a.target = "_blank";
        a.rel = "noopener";
      });
    } else {
      faltando.push("Número do WhatsApp (campo <code>whatsapp</code>)");
    }

    // E-mail
    var linksEmail = document.querySelectorAll('[data-contato="email"]');
    if (email) {
      Array.prototype.forEach.call(linksEmail, function (a) {
        a.href = "mailto:" + email + "?subject=" + encodeURIComponent("Projeto com a Desata");
        a.hidden = false;
      });
      mostrarItem("email");
    } else {
      faltando.push("E-mail de contato (campo <code>email</code>)");
    }

    // Instagram
    var linksInsta = document.querySelectorAll('[data-contato="instagram"]');
    if (instagram) {
      Array.prototype.forEach.call(linksInsta, function (a) {
        a.href = "https://instagram.com/" + instagram;
        a.target = "_blank";
        a.rel = "noopener";
      });
      mostrarItem("instagram");
    }

    // Cidade/região no rodapé
    if (local) {
      var alvo = document.getElementById("local-texto");
      if (alvo) { alvo.textContent = local; }
      mostrarItem("local");
    }

    mostrarAviso(faltando);
  }

  function mostrarItem(nome) {
    var itens = document.querySelectorAll('[data-contato-item="' + nome + '"]');
    Array.prototype.forEach.call(itens, function (el) { el.hidden = false; });
  }

  function mostrarAviso(faltando) {
    var aviso = document.getElementById("aviso-config");
    var lista = document.getElementById("aviso-config-lista");
    if (!aviso || !lista || !faltando.length) { return; }
    lista.innerHTML = faltando.map(function (item) {
      return "<li>" + item + "</li>";
    }).join("");
    aviso.hidden = false;
  }

  /* ---------- 2. Cabeçalho e menu ---------- */
  function iniciarCabecalho() {
    var cabecalho = document.getElementById("cabecalho");
    var botao = document.getElementById("menu-botao");
    var nav = document.getElementById("nav-principal");
    if (!cabecalho || !botao || !nav) { return; }

    var ticking = false;
    function aoRolar() {
      if (ticking) { return; }
      ticking = true;
      window.requestAnimationFrame(function () {
        cabecalho.classList.toggle("esta-rolado", window.scrollY > 8);
        ticking = false;
      });
    }
    window.addEventListener("scroll", aoRolar, { passive: true });
    aoRolar();

    function fechar(devolverFoco) {
      nav.classList.remove("esta-aberto");
      botao.setAttribute("aria-expanded", "false");
      botao.setAttribute("aria-label", "Abrir menu");
      if (devolverFoco) { botao.focus(); }
    }

    botao.addEventListener("click", function () {
      var aberto = nav.classList.toggle("esta-aberto");
      botao.setAttribute("aria-expanded", aberto ? "true" : "false");
      botao.setAttribute("aria-label", aberto ? "Fechar menu" : "Abrir menu");
    });

    nav.addEventListener("click", function (evento) {
      if (evento.target.closest("a")) { fechar(false); }
    });

    document.addEventListener("keydown", function (evento) {
      if (evento.key === "Escape" && nav.classList.contains("esta-aberto")) {
        fechar(true);
      }
    });

    document.addEventListener("click", function (evento) {
      if (!nav.classList.contains("esta-aberto")) { return; }
      if (!cabecalho.contains(evento.target)) { fechar(false); }
    });

    // Ao voltar para a largura de desktop, o menu não fica preso aberto.
    var desktop = window.matchMedia("(min-width: 861px)");
    function aoTrocarLargura(e) { if (e.matches) { fechar(false); } }
    if (desktop.addEventListener) {
      desktop.addEventListener("change", aoTrocarLargura);
    } else if (desktop.addListener) {
      desktop.addListener(aoTrocarLargura);
    }
  }

  /* ---------- 3. Revelar conteúdo e desenhar os laços ---------- */
  function iniciarAnimacoes() {
    var alvos = document.querySelectorAll(".revelar, .laco-animado");

    // Prepara o traço dos laços com o comprimento real do caminho.
    Array.prototype.forEach.call(document.querySelectorAll(".laco-animado .laco-traco"), function (traco) {
      var tamanho = Math.ceil(traco.getTotalLength ? traco.getTotalLength() : 3000);
      traco.parentNode.style.setProperty("--tamanho", tamanho);
    });

    if (semMovimento || !("IntersectionObserver" in window)) {
      Array.prototype.forEach.call(alvos, function (el) { el.classList.add("esta-visivel"); });
      return;
    }

    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (entrada.isIntersecting) {
          entrada.target.classList.add("esta-visivel");
          observador.unobserve(entrada.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });

    Array.prototype.forEach.call(alvos, function (el) { observador.observe(el); });
  }

  /* ---------- 4. Ano no rodapé ---------- */
  function iniciarAno() {
    var ano = document.getElementById("ano");
    if (ano) { ano.textContent = new Date().getFullYear(); }
  }

  /* ---------- Início ---------- */
  function iniciar() {
    aplicarContatos();
    iniciarCabecalho();
    iniciarAnimacoes();
    iniciarAno();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciar);
  } else {
    iniciar();
  }
})();
