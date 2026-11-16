/*
 * Roteiro do reel do pagaAí — plano-sequência.
 *
 * Não existe corte. Existe uma câmera que desce por um cenário só.
 * CAMERA = os pontos por onde ela passa: em que instante (t) está mirando
 * o ponto (x,y) do mundo, com que aproximação (z). O quadro é 1080x1920,
 * então em cada marca ela enxerga 1080/z por 1920/z do cenário — é essa
 * conta que diz se alguma coisa vai entrar cortada.
 *
 * Os clipes filmados são janelas dentro do mesmo cenário. A câmera passa
 * por dentro delas; por isso a troca entre o vídeo real e a parte gráfica
 * é movimento, não corte.
 */
/* Qual mascote fecha o vídeo: 'corrida' é o ciclo filmado, 'moeda' é o desenho
   com a moeda dando pulinhos. O que não for escolhido sai da cena antes de
   qualquer outra coisa ler o palco. */
const FECHO = 'moeda';
for (const el of document.querySelectorAll('[data-fecho]')) {
  if (el.dataset.fecho !== FECHO) el.remove();
}

const mundo = document.getElementById('mundo');

const CAMERA = [
  { t: 0,     x: 1000, y: -1500, z: 0.72 },  // janela 1: o casal pagando no mercado
  { t: 3000,  x: 1000, y: -1300, z: 0.76 },  // aproxima devagar enquanto o clipe roda
  { t: 6000,  x: 1000, y:  1150, z: 0.80 },  // desce: as compras caem sobre a mesa de recibos
  { t: 8800,  x: 1000, y:  2200, z: 0.62 },  // plano aberto: tudo é sugado para o celular
  { t: 11200, x: 1000, y:  3560, z: 1.38 },  // entra no celular, inteiro no quadro
  { t: 15000, x: 1000, y:  3630, z: 1.52 },  // aproxima: categorias e gráfico
  { t: 18200, x: 1000, y:  3740, z: 1.64 },  // o aviso de vencimento sobe
  { t: 21000, x: 1000, y:  3560, z: 0.58 },  // afasta: a vida em volta do celular
  { t: 23200, x: 1000, y:  3700, z: 0.56 },  // segura o plano aberto
  { t: 25800, x: 1000, y:  6250, z: 0.70 },  // janela 2: o casal no sofá
  { t: 27600, x: 1000, y:  6420, z: 0.74 },
  { t: 30000, x: 1000, y:  8451, z: 1.25 },  // assinatura
  { t: 31200, x: 1000, y:  8451, z: 1.28 },  // respiro final
];

const FIM = 32400;

// Elementos que entram (data-em) e saem (data-ate) sozinhos
const PROGRAMADOS = [...document.querySelectorAll('[data-em]')]
  .map((el) => ({ el, em: Number(el.dataset.em), ate: Number(el.dataset.ate) || Infinity,
                  ligado: false, saiu: false }));

// Clipes: cada um começa a tocar na hora marcada, do primeiro quadro
const CLIPES = [...document.querySelectorAll('video[data-toca]')]
  .map((el) => ({ el, em: Number(el.dataset.toca), tocou: false }));

// Momentos com animação própria (não é só aparecer)
const GATILHOS = [
  { em: 8400,  faz: sugarCompras },             // as compras voam para dentro do celular
  { em: 11000, faz: () => contar(53810, 2400) },
  { em: 13000, faz: () => ligar(['tag1', 'tag2']) },
  { em: 13400, faz: () => ligar(['tag3', 'tag4']) },
  { em: 15400, faz: () => ligar(['col1', 'col2', 'col3', 'col4']) },
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
    for (const c of CLIPES) {
      if (!c.tocou && ms >= c.em) { c.el.currentTime = 0; c.el.play(); c.tocou = true; }
    }
    for (const g of GATILHOS) {
      if (!g.feito && ms >= g.em) { g.faz(); g.feito = true; }
    }
    if (ms < FIM) requestAnimationFrame(quadro);
    else document.title = 'FIM';   // o gravar.js espera por isto
  };
  requestAnimationFrame(quadro);
}

/* Só começa quando os três clipes já têm quadro suficiente para tocar sem
   engasgar — senão a gravação pega a janela preta. */
function prontos() {
  const videos = [...document.querySelectorAll('video')];
  return Promise.all(videos.map((v) => v.readyState >= 3
    ? Promise.resolve()
    : new Promise((ok) => v.addEventListener('canplaythrough', ok, { once: true }))));
}

addEventListener('load', async () => {
  camera(0);
  await prontos();
  setTimeout(rodar, 400);
});
