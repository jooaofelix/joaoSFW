/*
 * Gera as artes do Instagram a partir de arte.html.
 *
 *   npm i playwright          (uma vez)
 *   node instagram/gerar-artes.js
 *
 * Cada bloco com data-nome vira um PNG em instagram/artes/.
 * Posts saem 1080x1350 (4:5) e capas de destaque 1080x1080.
 */
const { chromium } = require("playwright");
const http = require("http");
const fs = require("fs");
const path = require("path");

const AQUI = __dirname;
const RAIZ = path.resolve(AQUI, "..");
const SAIDA = path.join(AQUI, "artes");

const TIPOS = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript",
                ".png": "image/png", ".woff2": "font/woff2" };

function servir(raiz) {
  const servidor = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split("?")[0]).replace(/^[/]+/, "");
    const arq = path.resolve(raiz, rel);
    if (!arq.startsWith(raiz) || !fs.existsSync(arq) || fs.statSync(arq).isDirectory()) {
      return res.writeHead(404).end("nao encontrado");
    }
    res.writeHead(200, { "Content-Type": TIPOS[path.extname(arq)] || "application/octet-stream" });
    fs.createReadStream(arq).pipe(res);
  });
  return new Promise(r => servidor.listen(0, "127.0.0.1", () => r(servidor)));
}

function acharChrome() {
  if (process.env.CHROME_BIN && fs.existsSync(process.env.CHROME_BIN)) return process.env.CHROME_BIN;
  const base = process.env.PLAYWRIGHT_BROWSERS_PATH || "/opt/pw-browsers";
  if (!fs.existsSync(base)) return undefined;
  for (const dir of fs.readdirSync(base).filter(d => d.startsWith("chromium-")).sort().reverse()) {
    for (const sub of ["chrome-linux64", "chrome-linux"]) {
      const p = path.join(base, dir, sub, "chrome");
      if (fs.existsSync(p)) return p;
    }
  }
  return undefined;
}

(async () => {
  fs.mkdirSync(SAIDA, { recursive: true });
  const servidor = await servir(RAIZ);
  const navegador = await chromium.launch({ executablePath: acharChrome() });
  const pagina = await navegador.newPage({ viewport: { width: 1180, height: 1500 }, deviceScaleFactor: 1 });

  const falhas = [];
  pagina.on("requestfailed", r => falhas.push(r.url()));
  await pagina.goto("http://127.0.0.1:" + servidor.address().port + "/instagram/arte.html",
    { waitUntil: "networkidle" });
  await pagina.waitForTimeout(300);

  const blocos = await pagina.$$("[data-nome]");
  for (const bloco of blocos) {
    const nome = await bloco.getAttribute("data-nome");
    const caixa = await bloco.boundingBox();
    await bloco.screenshot({ path: path.join(SAIDA, nome + ".png") });
    console.log("· " + nome + ".png  " + Math.round(caixa.width) + "x" + Math.round(caixa.height));
  }

  if (falhas.length) console.error("! nao carregou: " + falhas.join(", "));
  console.log("\n" + blocos.length + " artes em instagram/artes/");
  await navegador.close();
  servidor.close();
})();
