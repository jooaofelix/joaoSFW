/*
 * Roteiro do reel do pagaAí — plano-sequência.
 *
 * Não existe corte. Existe uma câmera que desce por um cenário só.
 * CAMERA = os pontos por onde ela passa: em que instante (t) está mirando
 * o ponto (x,y) do mundo, com que aproximação (z). O quadro é 1080x1920,
 * então em cada ponto ela enxerga 1080/z por 1920/z do cenário.
 *
 * Mexer no ritmo é mexer nos tempos. Mexer no enquadramento é mexer no z.
 */
const mundo = document.getElementById('mundo');

const CAMERA = [
  { t: 0,     x: 1000, y:  560, z: 1.12 },  // o título, perto
  { t: 3200,  x: 1000, y:  900, z: 0.82 },  // afasta: as compras vão caindo em volta
  { t: 5800,  x: 1000, y: 1240, z: 0.78 },  // desce um pouco: "Quem anotou?"
  { t: 8000,  x: 1000, y: 1760, z: 0.60 },  // plano aberto: as compras voam para o celular
  { t: 11200, x: 1000, y: 3020, z: 1.38 },  // entra no celular, inteiro no quadro
  { t: 15500, x: 1000, y: 3090, z: 1.52 },  // aproxima devagar: categorias e gráfico
  { t: 18500, x: 1000, y: 3200, z: 1.64 },  // o aviso de vencimento sobe
  { t: 22000, x: 1000, y: 3020, z: 0.58 },  // afasta: a vida em volta do celular
  { t: 24800, x: 1000, y: 3120, z: 0.56 },  // segura o plano aberto
  { t: 27500, x: 1000, y: 4720, z: 0.92 },  // desce para a frase e o mascote
  { t: 30500, x: 1000, y: 5821, z: 1.35 },  // assinatura
  { t: 31800, x: 1000, y: 5821, z: 1.38 },  // respiro final
];

const FIM = 32800;

// Elementos que entram sozinhos, pelo atributo data-em
const PROGRAMADOS = [...document.querySelectorAll('[data-em]')]
  .map((el) => ({ el, em: Number(el.dataset.em), ate: Number(el.dataset.ate) || Infinity,
                  ligado: false, saiu: false }));

// Momentos com animação própria (não é só aparecer)
const GATILHOS = [
  { em: 7500,  faz: sugarCompras },             // as compras voam para dentro do celular
  { em: 10000, faz: () => contar(53810, 2600) },
  { em: 12200, faz: () => ligar(['tag1', 'tag2']) },
  { em: 12700, faz: () => ligar(['tag3', 'tag4']) },
  { em: 15000, faz: () => ligar(['col1', 'col2', 'col3', 'col4']) },
  { em: 18000, faz: () => ligar(['aviso']) },
];

const suave = (k) => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);

function camera(ms) {
  const ultimo = CAMERA[CAMERA.length - 1];
  let a = ultimo, b = ultimo;
  for (let i = 0; i < CAMERA.length - 1; i++) {
    if (ms >= CAMERA[i].t && ms <= CAMERA[i + 1].t) { a = CAMERA[i]; b = CAMERA[i + 1]; break; }
  }
  const k = a === b ? 1 : suave((ms - a.t) / (b.t - a.t));
  const x = a.x + (b.x - a.x) * k;
  const y = a.y + (b.y - a.y) * k;
  const z = a.z + (b.z - a.z) * k;
  // uma respiração lenta, para o quadro nunca ficar morto
  const dy = Math.sin(ms / 2800) * 5;
  mundo.style.transform =
    `translate(540px, 960px) scale(${z.toFixed(4)}) translate(${-x}px, ${-(y + dy).toFixed(2)}px)`;
}

/** As compras saem de onde estão e entram na tela do celular. */
function sugarCompras() {
  const fone = document.getElementById('fone');
  const destino = { x: fone.offsetLeft + fone.offsetWidth / 2, y: fone.offsetTop + 520 };
  ['cp1', 'cp2', 'cp3', 'cp4'].forEach((id, i) => {
    const el = document.getElementById(id);
    const dx = destino.x - (el.offsetLeft + el.offsetWidth / 2);
    const dy = destino.y - (el.offsetTop + el.offsetHeight / 2);
    setTimeout(() => {
      el.style.transform = `translate(${dx}px, ${dy}px) scale(.16) rotate(${i % 2 ? 9 : -9}deg)`;
      el.classList.add('sugada');
    }, i * 180);
  });
}

function ligar(ids) {
  ids.forEach((id) => document.getElementById(id)?.classList.add('on'));
}

function contar(centavos, ms) {
  const el = document.getElementById('total');
  const t0 = performance.now();
  const passo = (t) => {
    const k = Math.min(1, (t - t0) / ms);
    const v = (centavos / 100) * (1 - Math.pow(1 - k, 3));
    el.textContent = 'R$ ' + v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    if (k < 1) requestAnimationFrame(passo);
  };
  requestAnimationFrame(passo);
}

function rodar() {
  const t0 = performance.now();
  const quadro = (t) => {
    const ms = t - t0;
    camera(ms);
    for (const p of PROGRAMADOS) {
      if (!p.ligado && ms >= p.em) { p.el.classList.add('on'); p.ligado = true; }
      if (!p.saiu && ms >= p.ate) { p.el.classList.add('saiu'); p.saiu = true; }
    }
    for (const g of GATILHOS) {
      if (!g.feito && ms >= g.em) { g.faz(); g.feito = true; }
    }
    if (ms < FIM) requestAnimationFrame(quadro);
    else document.title = 'FIM';   // o gravar.js espera por isto
  };
  requestAnimationFrame(quadro);
}

addEventListener('load', () => { camera(0); setTimeout(rodar, 400); });
