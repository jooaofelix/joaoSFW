/*
 * Roteiro do vídeo de demonstração — 1080x1920, sem narração.
 * Tudo é cronometrado aqui; o gravar.js só abre esta página e filma.
 *
 * Contatos entram por ?zap=...&site=... (o gravar.js lê de assets/js/config.js).
 */
const $ = s => document.querySelector(s);
const espera = ms => new Promise(r => setTimeout(r, ms));
const params = new URLSearchParams(location.search);

$("#contato").innerHTML =
  (params.get("zap")  || "(12) 99133-8866") + "<br>" +
  (params.get("site") || "desata.jvctrfelix.workers.dev");

// comprimento real do traço, para o laço se desenhar certinho
document.querySelectorAll(".laco").forEach(svg => {
  const p = svg.querySelector("path");
  svg.style.setProperty("--len", Math.ceil(p.getTotalLength()));
});

const tela = $("#tela");
const toque = $("#toque");
const onda = $("#onda");
const ESC = 1.3846;   // o iframe é 390px mostrado a 540px

const api = () => tela.contentWindow.api;
const doc = () => tela.contentDocument;

/** Leva o dedo até o elemento (coordenadas do site -> coordenadas do palco). */
async function mirar(seletor, ms = 650) {
  const alvo = doc().querySelector(seletor);
  if (!alvo) return null;
  const r = alvo.getBoundingClientRect();
  const x = (r.left + r.width / 2) * ESC;
  const y = (r.top + r.height / 2) * ESC;
  toque.style.left = onda.style.left = x + "px";
  toque.style.top = onda.style.top = y + "px";
  toque.classList.add("on");
  await espera(ms);
  return alvo;
}

/** Toca: anima o dedo, dispara a onda e executa a ação. */
async function tocar(seletor, acao, ms = 520) {
  await mirar(seletor);
  toque.classList.add("bate");
  onda.classList.add("toca");
  await espera(180);
  if (acao) acao();
  await espera(ms);
  toque.classList.remove("bate");
  onda.classList.remove("toca");
}

function legenda(texto) {
  const el = $("#legenda");
  el.classList.remove("on");
  setTimeout(() => { el.innerHTML = texto; el.classList.add("on"); }, 260);
}

async function roteiro() {
  // ---------- abertura (0 → 4,2s) ----------
  $("#laco-intro").classList.add("desenha");
  await espera(4200);
  $("#intro").classList.add("sai");
  await espera(500);

  // ---------- a loja entra (4,7 → 6,2s) ----------
  $("#demo").classList.add("on");
  await espera(250);
  $("#fone").classList.add("on");
  legenda("A vitrine abre <b>no celular</b>");
  await espera(750);
  api().revelar();
  await espera(1050);

  // ---------- vitrine (6,2 → 10,5s) ----------
  await api().rolar(300, 1000);
  await espera(350);
  legenda("Filtra pelo <b>tamanho</b> que ela usa");
  await espera(750);
  await tocar('.chip[data-tam="M"]', () => api().filtrar("M"), 1000);
  await espera(450);

  // ---------- peça 1 (10,5 → 18s) ----------
  legenda("Toca na peça e <b>vê o produto</b>");
  await espera(700);
  await tocar('.card[data-id="2"]', () => api().abrir(2), 1100);
  await espera(500);
  legenda("Escolhe o <b>tamanho</b>");
  await espera(600);
  await tocar('.tam[data-tam="M"]', () => api().tamanho("M"), 700);
  await espera(400);
  legenda("E joga <b>na sacola</b>");
  await espera(500);
  await tocar("#btn-add", () => api().add(2, "M"), 850);
  await espera(500);

  // ---------- peça 2 (18 → 24,5s) ----------
  api().fechar();
  await espera(550);
  legenda("Outra peça, mesmo caminho");
  await tocar('.card[data-id="5"]', () => api().abrir(5), 1000);
  await espera(300);
  await tocar('.tam[data-tam="G"]', () => api().tamanho("G"), 600);
  await espera(250);
  await tocar("#btn-add", () => api().add(5, "G"), 850);
  await espera(500);
  api().fechar();
  await espera(600);

  // ---------- sacola (24,5 → 29s) ----------
  legenda("A sacola já soma <b>tudo</b>");
  await espera(500);
  await tocar("#btn-sacola", () => api().verSacola(), 1000);
  await espera(1300);

  // ---------- pedido no whatsapp (29 → 35,5s) ----------
  legenda("O pedido chega <b>pronto no WhatsApp</b>");
  await espera(700);
  await tocar("#btn-zap", () => api().whatsapp(), 900);
  toque.classList.remove("on");
  await espera(1200);
  legenda("Peça, tamanho e total — <b>sem digitar nada</b>");
  await espera(2600);

  // ---------- fecho (35,5 → 42s) ----------
  $("#outro").classList.add("on");
  $("#laco-outro").classList.add("desenha");
  await espera(4600);

  document.title = "FIM";   // o gravar.js espera por isto
}

addEventListener("load", () => setTimeout(roteiro, 400));
