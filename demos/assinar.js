/*
 * Cola a assinatura da Desata no fim de um vídeo.
 *
 *   npm i playwright                                   (uma vez)
 *   node demos/assinar.js <video.mp4> [saida.mp4] [--seg 6] [--arroba]
 *
 * O fecho é gravado na mesma resolução e na mesma taxa de quadros do vídeo de
 * entrada, e entra com uma passagem cruzada de meio segundo. Se o vídeo tiver
 * áudio, o fecho recebe silêncio do mesmo formato, senão a junção falha.
 *
 * Os contatos saem de assets/js/config.js.
 */
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const http = require("http");
const fs = require("fs");
const path = require("path");
const os = require("os");

const RAIZ = path.resolve(__dirname, "..");
const PASSAGEM = 0.5;   // segundos de passagem cruzada

const args = process.argv.slice(2);
const sinalizadores = args.filter(a => a.startsWith("--"));
const soltos = args.filter(a => !a.startsWith("--") && !/^\d+(\.\d+)?$/.test(a));
const entrada = soltos[0];
if (!entrada || !fs.existsSync(entrada)) {
  console.error("uso: node demos/assinar.js <video.mp4> [saida.mp4] [--seg 6] [--arroba]");
  process.exit(1);
}
const saida = soltos[1] || entrada.replace(/\.mp4$/i, "") + "-assinado.mp4";
const iSeg = args.indexOf("--seg");
const SEGUNDOS = iSeg >= 0 ? Number(args[iSeg + 1]) : 6;
const COM_ARROBA = sinalizadores.includes("--arroba");

/* ---------- dados ---------- */
function config() {
  const fonte = fs.readFileSync(path.join(RAIZ, "assets", "js", "config.js"), "utf8");
  const pega = c => (fonte.match(new RegExp("\\b" + c + "\\s*:\\s*\"([^\"]*)\"")) || [])[1] || "";
  const n = pega("whatsapp").replace(/\D/g, "");
  const m = n.match(/^55(\d{2})(\d{4,5})(\d{4})$/);
  return {
    zap: m ? "(" + m[1] + ") " + m[2] + "-" + m[3] : n,
    instagram: pega("instagram"),
    site: "desata.jvctrfelix.workers.dev",
  };
}

function sonda(arquivo) {
  const linhas = execFileSync("ffprobe", ["-v", "error",
    "-show_entries", "stream=codec_type,width,height,r_frame_rate",
    "-show_entries", "format=duration", "-of", "default=nw=1", arquivo]).toString();
  const pega = c => (linhas.match(new RegExp("^" + c + "=(.+)$", "m")) || [])[1];
  const fps = (pega("r_frame_rate") || "30/1").split("/");
  return {
    largura: Number(pega("width")), altura: Number(pega("height")),
    fps: Math.round(Number(fps[0]) / Number(fps[1] || 1)),
    duracao: Number(pega("duration")),
    temAudio: /codec_type=audio/.test(linhas),
  };
}

/* ---------- servidor local (o file:// não carrega a fonte) ---------- */
const TIPOS = { ".html": "text/html", ".css": "text/css", ".png": "image/png", ".woff2": "font/woff2" };
function servir(raiz) {
  const s = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split("?")[0]).replace(/^[/]+/, "");
    const arq = path.resolve(raiz, rel);
    if (!arq.startsWith(raiz) || !fs.existsSync(arq) || fs.statSync(arq).isDirectory()) {
      return res.writeHead(404).end("nao encontrado");
    }
    res.writeHead(200, { "Content-Type": TIPOS[path.extname(arq)] || "application/octet-stream" });
    fs.createReadStream(arq).pipe(res);
  });
  return new Promise(r => s.listen(0, "127.0.0.1", () => r(s)));
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
  const v = sonda(entrada);
  const c = config();
  const contato = COM_ARROBA && c.instagram
    ? "@" + c.instagram + "|" + c.zap
    : c.zap + "|" + c.site;

  console.log("· entrada: " + v.largura + "x" + v.altura + ", " + v.fps + "fps, "
    + v.duracao.toFixed(1) + "s" + (v.temAudio ? ", com áudio" : ", sem áudio"));

  const temp = fs.mkdtempSync(path.join(os.tmpdir(), "fecho-"));
  const servidor = await servir(RAIZ);
  const navegador = await chromium.launch({ executablePath: acharChrome() });
  const ctx = await navegador.newContext({
    viewport: { width: v.largura, height: v.altura },
    deviceScaleFactor: 1,
    recordVideo: { dir: temp, size: { width: v.largura, height: v.altura } },
  });
  const pagina = await ctx.newPage();
  const url = "http://127.0.0.1:" + servidor.address().port + "/demos/fecho/fecho.html"
    + "?ms=" + SEGUNDOS * 1000
    + "&contato=" + encodeURIComponent(contato)
    + "&aviso=" + encodeURIComponent("feito pela desata");
  await pagina.goto(url, { waitUntil: "networkidle" });

  console.log("· gravando o fecho (" + SEGUNDOS + "s)...");
  await pagina.waitForFunction(() => document.title === "FIM", null, { timeout: 60000 });
  await pagina.waitForTimeout(200);
  await ctx.close();
  await navegador.close();
  servidor.close();

  const webm = path.join(temp, fs.readdirSync(temp).find(f => f.endsWith(".webm")));
  const fecho = path.join(temp, "fecho.mp4");
  execFileSync("ffmpeg", ["-y", "-i", webm,
    "-vf", "fps=" + v.fps + ",scale=" + v.largura + ":" + v.altura + ",format=yuv420p",
    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-an", fecho],
    { stdio: ["ignore", "ignore", "pipe"] });

  console.log("· juntando com passagem cruzada...");
  const corte = Math.max(0, v.duracao - PASSAGEM);
  const filtros = [
    "[0:v]fps=" + v.fps + ",format=yuv420p[a]",
    "[1:v]fps=" + v.fps + ",format=yuv420p[b]",
    "[a][b]xfade=transition=fade:duration=" + PASSAGEM + ":offset=" + corte.toFixed(3) + "[v]",
  ];
  const cmd = ["-y", "-i", entrada, "-i", fecho];
  if (v.temAudio) {
    // o fecho é mudo: sem uma trilha de silêncio, a junção perde o áudio do vídeo
    cmd.push("-f", "lavfi", "-t", String(SEGUNDOS), "-i", "anullsrc=channel_layout=stereo:sample_rate=44100");
    filtros.push("[0:a]afade=t=out:st=" + corte.toFixed(3) + ":d=" + PASSAGEM + "[a0]");
    filtros.push("[a0][2:a]concat=n=2:v=0:a=1[aout]");
  }
  cmd.push("-filter_complex", filtros.join(";"), "-map", "[v]");
  if (v.temAudio) cmd.push("-map", "[aout]", "-c:a", "aac", "-b:a", "160k");
  cmd.push("-c:v", "libx264", "-preset", "slow", "-crf", "21", "-movflags", "+faststart", saida);
  execFileSync("ffmpeg", cmd, { stdio: ["ignore", "ignore", "pipe"] });

  fs.rmSync(temp, { recursive: true, force: true });
  const f = sonda(saida);
  console.log("· " + path.basename(saida) + " — " + f.duracao.toFixed(1) + "s, "
    + (fs.statSync(saida).size / 1048576).toFixed(1) + " MB");
})();
