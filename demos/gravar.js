/*
 * Grava os vídeos de demonstração.
 *
 *   npm i playwright                                    (uma vez)
 *   node demos/gravar.js loja-roupas 148-demonstracao
 *   node demos/gravar.js landing-roupas 148-landing
 *
 * Abre o palco da pasta indicada, filma e salva um MP4 1080x1920 ali dentro.
 * Precisa do ffmpeg no PATH.
 */
const { chromium } = require("playwright");
const { execFileSync, spawnSync } = require("child_process");
const http = require("http");
const fs = require("fs");
const path = require("path");

const DEMO = process.argv[2];
if (!DEMO) {
  console.error("uso: node demos/gravar.js <pasta-do-demo> [nome-do-mp4]");
  process.exit(1);
}
const AQUI = path.join(__dirname, DEMO);
const RAIZ = path.resolve(__dirname, "..");
const SAIDA = path.join(AQUI, (process.argv[3] || DEMO) + ".mp4");
const TEMP = path.join(AQUI, ".gravacao");

function contatos() {
  const fonte = fs.readFileSync(path.join(RAIZ, "assets", "js", "config.js"), "utf8");
  const pega = c => (fonte.match(new RegExp(`\\b${c}\\s*:\\s*"([^"]*)"`)) || [])[1] || "";
  const n = pega("whatsapp").replace(/\D/g, "");
  const m = n.match(/^55(\d{2})(\d{4,5})(\d{4})$/);
  return { zap: m ? `(${m[1]}) ${m[2]}-${m[3]}` : n, site: "desata.jvctrfelix.workers.dev" };
}

/* O palco carrega a loja num iframe, e em file:// o navegador trata cada
   arquivo como origem diferente — o roteiro não alcançaria a página de dentro.
   Servir por HTTP resolve sem afrouxar a segurança do navegador. */
const TIPOS = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css",
                ".png": "image/png", ".webp": "image/webp", ".woff2": "font/woff2",
                ".svg": "image/svg+xml", ".mp4": "video/mp4", ".webm": "video/webm" };

function servir(raiz) {
  const servidor = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split("?")[0]).replace(/^\/+/, "");
    const arquivo = path.resolve(raiz, rel);
    if (!arquivo.startsWith(raiz) || !fs.existsSync(arquivo) || fs.statSync(arquivo).isDirectory()) {
      res.writeHead(404).end("não encontrado");
      return;
    }
    const tipo = TIPOS[path.extname(arquivo)] || "application/octet-stream";
    const tamanho = fs.statSync(arquivo).size;
    /* O navegador pede vídeo por pedaços. Sem resposta 206 ele desiste de
       tocar o arquivo, e a janela do reel sairia preta na gravação. */
    const faixa = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range || "");
    if (faixa) {
      const ini = faixa[1] ? Number(faixa[1]) : 0;
      const fim = faixa[2] ? Math.min(Number(faixa[2]), tamanho - 1) : tamanho - 1;
      res.writeHead(206, {
        "Content-Type": tipo, "Accept-Ranges": "bytes",
        "Content-Range": `bytes ${ini}-${fim}/${tamanho}`, "Content-Length": fim - ini + 1,
      });
      fs.createReadStream(arquivo, { start: ini, end: fim }).pipe(res);
      return;
    }
    res.writeHead(200, { "Content-Type": tipo, "Accept-Ranges": "bytes", "Content-Length": tamanho });
    fs.createReadStream(arquivo).pipe(res);
  });
  return new Promise(r => servidor.listen(0, "127.0.0.1", () => r(servidor)));
}

function acharChrome() {
  if (process.env.CHROME_BIN && fs.existsSync(process.env.CHROME_BIN)) return process.env.CHROME_BIN;
  const base = process.env.PLAYWRIGHT_BROWSERS_PATH || "/opt/pw-browsers";
  if (!fs.existsSync(base)) return undefined;   // deixa o Playwright procurar sozinho
  for (const dir of fs.readdirSync(base).filter(d => d.startsWith("chromium-")).sort().reverse()) {
    for (const sub of ["chrome-linux64", "chrome-linux"]) {
      const p = path.join(base, dir, sub, "chrome");
      if (fs.existsSync(p)) return p;
    }
  }
  return undefined;
}

/** Quanto tempo o vídeo fica preto logo no começo (0 se já abre na imagem). */
function pretoNoComeco(arquivo) {
  // o relatório do blackdetect sai no stderr, com o ffmpeg terminando bem
  const r = spawnSync("ffmpeg", ["-hide_banner", "-i", arquivo,
    "-vf", "blackdetect=d=0.03:pic_th=0.95:pix_th=0.10", "-an", "-f", "null", "-"],
    { encoding: "utf8" });
  const m = /black_start:0(?:\.0+)?\s+black_end:([\d.]+)/.exec(r.stderr || "");
  return m ? Math.min(Number(m[1]), 2) : 0;
}

(async () => {
  fs.rmSync(TEMP, { recursive: true, force: true });
  const { zap, site } = contatos();

  const servidor = await servir(RAIZ);
  const porta = servidor.address().port;

  const navegador = await chromium.launch({
    executablePath: acharChrome(),
    args: ["--autoplay-policy=no-user-gesture-required", "--force-device-scale-factor=1"],
  });
  const ctx = await navegador.newContext({
    viewport: { width: 1080, height: 1920 },
    deviceScaleFactor: 1,
    recordVideo: { dir: TEMP, size: { width: 1080, height: 1920 } },
  });
  const pagina = await ctx.newPage();

  const falhas = [];
  pagina.on("pageerror", e => falhas.push(e.message));
  pagina.on("console", m => { if (m.type() === "error") falhas.push(m.text()); });

  const rel = path.relative(RAIZ, path.join(AQUI, "palco.html")).split(path.sep).join("/");
  await pagina.goto(`http://127.0.0.1:${porta}/${rel}`
    + `?zap=${encodeURIComponent(zap)}&site=${encodeURIComponent(site)}`,
    { waitUntil: "networkidle" });

  console.log("· gravando...");
  try {
    await pagina.waitForFunction(() => document.title === "FIM", null, { timeout: 90000 });
  } catch (e) {
    console.error("! o roteiro não chegou ao fim." + (falhas.length ? "\n  " + falhas.join("\n  ") : ""));
    throw e;
  }
  await pagina.waitForTimeout(400);

  await ctx.close();
  await navegador.close();
  servidor.close();

  const webm = fs.readdirSync(TEMP).find(f => f.endsWith(".webm"));
  if (!webm) throw new Error("gravação não encontrada");

  /* A gravação começa antes de o navegador pintar o primeiro quadro, então o
     arquivo abre com alguns décimos de preto. Num reel isso é o tempo em que
     a pessoa decide se continua — melhor começar já na imagem. */
  const inicio = pretoNoComeco(path.join(TEMP, webm));
  if (inicio > 0) console.log(`· cortando ${inicio.toFixed(2)}s de preto do começo...`);

  console.log("· convertendo para MP4...");
  execFileSync("ffmpeg", [
    "-y", ...(inicio > 0 ? ["-ss", inicio.toFixed(3)] : []), "-i", path.join(TEMP, webm),
    "-vf", "fps=30,scale=1080:1920:flags=lanczos,format=yuv420p",
    "-c:v", "libx264", "-preset", "slow", "-crf", "21",
    "-movflags", "+faststart", "-an", SAIDA,
  ], { stdio: ["ignore", "ignore", "pipe"] });

  fs.rmSync(TEMP, { recursive: true, force: true });
  const seg = execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration",
    "-of", "default=nw=1:nk=1", SAIDA]).toString().trim();
  console.log(`· ${path.basename(SAIDA)} — ${(+seg).toFixed(1)}s, ${(fs.statSync(SAIDA).size / 1048576).toFixed(1)} MB`);
})();
