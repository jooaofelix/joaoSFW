/*
 * Roteiro do vídeo da landing page — 1080x1920, sem narração.
 * O caminho que se quer mostrar: link do perfil → página → WhatsApp.
 */
const $ = s => document.querySelector(s);
const espera = ms => new Promise(r => setTimeout(r, ms));
const params = new URLSearchParams(location.search);

$("#contato").innerHTML =
  (params.get("zap")  || "(12) 99133-8866") + "<br>" +
  (params.get("site") || "desata.jvctrfelix.workers.dev");

document.querySelectorAll(".laco").forEach(svg => {
  const p = svg.querySelector("path");
  svg.style.setProperty("--len", Math.ceil(p.getTotalLength()));
});

const tela = $("#tela"), toque = $("#toque"), onda = $("#onda");
const ESC = 1.3846;
const api = () => tela.contentWindow.api;
const doc = () => tela.contentDocument;

async function mirar(seletor, ms = 620) {
  const alvo = doc().querySelector(seletor);
  if (!alvo) return null;
  const r = alvo.getBoundingClientRect();
  toque.style.left = onda.style.left = (r.left + r.width / 2) * ESC + "px";
  toque.style.top  = onda.style.top  = (r.top + r.height / 2) * ESC + "px";
  toque.classList.add("on");
  await espera(ms);
  return alvo;
}

async function tocar(seletor, acao, ms = 520) {
  await mirar(seletor);
  toque.classList.add("bate");
  onda.classList.add("toca");
  await espera(170);
  if (acao) acao();
  await espera(ms);
  toque.classList.remove("bate");
  onda.classList.remove("toca");
}

function legenda(texto) {
  const el = $("#legenda");
  el.classList.remove("on");
  setTimeout(() => { el.innerHTML = texto; el.classList.add("on"); }, 250);
}

async function roteiro() {
  // abertura
  $("#laco-intro").classList.add("desenha");
  await espera(4000);
  $("#intro").classList.add("sai");
  await espera(450);

  // o funil começa no perfil
  $("#demo").classList.add("on");
  await espera(200);
  $("#fone").classList.add("on");
  legenda("Começa no <b>link do perfil</b>");
  await espera(1500);
  await tocar("#link-bio", () => api().entrar(), 900);
  toque.classList.remove("on");
  await espera(1500);

  // primeira tela
  legenda("A promessa cabe na <b>primeira tela</b>");
  await espera(2300);

  // as peças
  await api().rolar(560, 1100);
  legenda("As peças, com preço, <b>sem cadastro</b>");
  await espera(1900);
  await api().rolar(760, 700);
  await espera(300);

  // cada peça manda a própria mensagem
  legenda("Cada peça manda a <b>própria mensagem</b>");
  await espera(700);
  await tocar(".lote__btn", () => api().pedir(1), 900);
  toque.classList.remove("on");
  await espera(2300);
  legenda("Chega escrito: <b>qual peça e qual número</b>");
  await espera(2600);

  // o botão que acompanha
  api().fecharZap();
  await espera(700);
  legenda("O botão de conversa <b>segue na tela</b>");
  api().chamar();
  await espera(1600);
  await api().rolar(1850, 1200);
  await espera(400);

  // objeções
  legenda("As dúvidas, resolvidas <b>antes de perguntar</b>");
  await api().rolar(2750, 1400);
  await espera(1500);

  // fecho do funil
  await api().rolar(3100, 900);
  legenda("E o caminho termina <b>sempre no mesmo lugar</b>");
  await espera(700);
  await tocar("#btn-fixo", () => api().geral(), 900);
  toque.classList.remove("on");
  await espera(2600);

  // fecho Desata
  $("#outro").classList.add("on");
  $("#laco-outro").classList.add("desenha");
  await espera(4400);

  document.title = "FIM";
}

addEventListener("load", () => setTimeout(roteiro, 400));
