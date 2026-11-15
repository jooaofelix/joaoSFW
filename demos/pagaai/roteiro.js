/*
 * Roteiro do reel do pagaAí — sem narração, texto na tela.
 *
 * O ritmo é o da referência: corte a cada 1 a 2 segundos no gancho, um pouco
 * mais de ar nas cenas que têm o que ler. Os tempos abaixo são o vídeo todo;
 * mexer aqui é mexer no ritmo.
 */
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const $ = (s) => document.querySelector(s);

// [id da cena, quanto tempo fica na tela]
const CENAS = [
  ['c1', 1500],   // Você pagou a conta.
  ['c2', 1700],   // Ela pagou o mercado.
  ['c3', 2600],   // Quem anotou? (três compras)
  ['c4', 1900],   // E a fatura vence dia 21.
  ['c5', 2400],   // Agora elas se anotam sozinhas.
  ['c6', 2800],   // celular: anotado na hora
  ['c7', 2400],   // sem digitar nada / categoria
  ['c8', 2600],   // de dia, de noite, no domingo
  ['c9', 2600],   // quem gastou, em quê, de onde saiu
  ['c10', 2800],  // o que vence
  ['c11', 2800],  // total do mês + barras
  ['c12', 2600],  // enquanto vocês vivem
  ['c13', 3200],  // logo + selo
];

// O contador sobe junto com as barras, na cena do total.
function contar(ate, ms) {
  const el = $('#contador');
  if (!el) return;
  const t0 = performance.now();
  const passo = (t) => {
    const k = Math.min(1, (t - t0) / ms);
    const suave = 1 - Math.pow(1 - k, 3);
    el.textContent = 'R$ ' + Math.round(ate * suave).toLocaleString('pt-BR');
    if (k < 1) requestAnimationFrame(passo);
  };
  requestAnimationFrame(passo);
}

async function roteiro() {
  for (const [id, tempo] of CENAS) {
    const cena = document.getElementById(id);
    cena.classList.add('ativa');
    if (id === 'c11') contar(2980, 1600);
    await espera(tempo);
    cena.classList.remove('ativa');
    await espera(90);   // respiro curto entre cortes
  }
  await espera(300);
  document.title = 'FIM';   // o gravar.js espera por isto
}

addEventListener('load', () => setTimeout(roteiro, 500));
