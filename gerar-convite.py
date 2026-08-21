#!/usr/bin/env python3
"""
Gera o convite em PDF (convite.pdf) a partir dos dados do index.html.

    python3 gerar-convite.py

Não edite o convite.html gerado — ele é sobrescrito a cada execução.
Para mudar nome, telefone, e-mail ou endereço do site, edite o bloco
`const SITE` no topo do index.html e rode este script de novo.

Requisitos: python3, segno (pip install segno) e o Chromium/Chrome.
"""

import base64
import html
import os
import re
import shutil
import subprocess
import sys
import urllib.request

RAIZ = os.path.dirname(os.path.abspath(__file__))
CACHE_FONTES = os.path.join(RAIZ, "assets", "fontes.css")

FONTES_URL = (
    "https://fonts.googleapis.com/css2"
    "?family=Archivo:wght@600;700"
    "&family=IBM+Plex+Sans:wght@400;500;600"
    "&family=IBM+Plex+Mono:wght@400;600&display=swap"
)
UA_CHROME = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

PADRAO = {
    "nome": "João Félix",
    "whatsapp": "5512991338866",
    "email": "jvctrfelix@gmail.com",
    "instagram": "",
    "cidade": "São José dos Campos · SP",
    "site": "https://futuro.jvctrfelix.workers.dev",
}


# --------------------------------------------------------------------------
# 1. dados do site
# --------------------------------------------------------------------------
def ler_config():
    """Extrai o bloco `const SITE` do index.html, com fallback nos padrões."""
    dados = dict(PADRAO)
    caminho = os.path.join(RAIZ, "index.html")
    try:
        with open(caminho, encoding="utf-8") as arq:
            fonte = arq.read()
    except OSError:
        print("! index.html não encontrado — usando os valores de exemplo.")
        return dados

    bloco = re.search(r"const SITE\s*=\s*\{(.*?)\n\};", fonte, re.S)
    if not bloco:
        print("! bloco `const SITE` não encontrado — usando os valores de exemplo.")
        return dados

    for chave in PADRAO:
        achou = re.search(rf'\b{chave}\s*:\s*"([^"]*)"', bloco.group(1))
        if achou and achou.group(1).strip():
            dados[chave] = achou.group(1).strip()

    dados["whatsapp"] = re.sub(r"\D", "", dados["whatsapp"])
    return dados


def telefone_legivel(numero):
    achou = re.match(r"^55(\d{2})(\d{4,5})(\d{4})$", numero)
    return f"({achou.group(1)}) {achou.group(2)}-{achou.group(3)}" if achou else numero


def site_legivel(url):
    return re.sub(r"^https?://(www\.)?|/$", "", url)


# --------------------------------------------------------------------------
# 2. fontes embutidas (para o PDF não depender de rede nem do sistema)
# --------------------------------------------------------------------------
def montar_fontes():
    """Baixa as fontes uma vez e guarda em assets/fontes.css já em base64."""
    if os.path.exists(CACHE_FONTES):
        with open(CACHE_FONTES, encoding="utf-8") as arq:
            return arq.read()

    print("· baixando as fontes (só na primeira vez)...")
    try:
        pedido = urllib.request.Request(FONTES_URL, headers={"User-Agent": UA_CHROME})
        css = urllib.request.urlopen(pedido, timeout=30).read().decode("utf-8")
    except Exception as erro:                                    # noqa: BLE001
        print(f"! não deu para baixar as fontes ({erro}). O PDF sai com as do sistema.")
        return ""

    # só os subconjuntos latinos: o resto é peso morto para português
    blocos = []
    for bloco in re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})", css, re.S):
        assunto, regra = bloco
        if assunto not in ("latin", "latin-ext"):
            continue
        url = re.search(r"url\((https://[^)]+)\)", regra)
        if not url:
            continue
        try:
            dados = urllib.request.urlopen(url.group(1), timeout=30).read()
        except Exception:                                        # noqa: BLE001
            continue
        b64 = base64.b64encode(dados).decode("ascii")
        blocos.append(
            re.sub(
                r"url\(https://[^)]+\)",
                f"url(data:font/woff2;base64,{b64})",
                regra,
            )
        )

    embutido = "\n".join(blocos)
    if embutido:
        os.makedirs(os.path.dirname(CACHE_FONTES), exist_ok=True)
        with open(CACHE_FONTES, "w", encoding="utf-8") as arq:
            arq.write(embutido)
        print(f"· fontes guardadas em {os.path.relpath(CACHE_FONTES, RAIZ)}")
    return embutido


# --------------------------------------------------------------------------
# 3. QR codes
# --------------------------------------------------------------------------
def qr_svg(conteudo, cor="#0A2F27"):
    try:
        import segno
    except ImportError:
        print("! segno não instalado (pip install segno) — o convite sai sem QR.")
        return ""
    codigo = segno.make(conteudo, error="m")
    # omitsize preserva o viewBox: sem ele o QR não acompanha o tamanho da caixa
    return codigo.svg_inline(dark=cor, light=None, border=0, omitsize=True)


# --------------------------------------------------------------------------
# 4. conteúdo do convite
# --------------------------------------------------------------------------
# (título, uma linha, mensagem que já chega escrita no WhatsApp)
PROBLEMAS = [
    ("A agenda tem falta e buraco",
     "Paciente que não avisa, horário que fica vago e ninguém teve tempo de mandar o lembrete.",
     "Oi! Minha agenda tem muita falta e buraco de horário. Dá pra resolver?"),
    ("O histórico está espalhado",
     "Cadastro numa planilha, evolução num caderno, exame no WhatsApp. A versão certa está só na sua cabeça.",
     "Oi! O histórico dos meus pacientes está espalhado em vários lugares."),
    ("O dinheiro só aparece no fim do mês",
     "Quando o número chega, já não dá para reagir. E ainda falta saber quem não pagou.",
     "Oi! Só descubro quanto a clínica faturou no fim do mês, e queria mudar isso."),
    ("O paciente some e não volta",
     "Não é falta de demanda. É falta de alguém para chamar de volta quem parou no meio do tratamento.",
     "Oi! Tenho muito paciente que sumiu e não volta. Queria recuperar."),
]

# (código, para quê, uma linha, endereço da apresentação)
SISTEMAS = [
    ("ROTA", "A operação da clínica",
     "Agenda, cadastro, prontuário e evolução do paciente numa tela só, com lembrete automático.",
     "https://rota.jvctrfelix.workers.dev/conhecer"),
    ("BASE", "O financeiro da clínica",
     "O que entrou, o que falta receber e o fechamento do mês — sem planilha, lançando pelo WhatsApp.",
     "https://base.jvctrfelix.workers.dev/como-funciona"),
    ("PROX", "Os pacientes que faltam voltar",
     "Quem entrou em contato, quem parou o tratamento e quem precisa de retorno, com prazo e responsável.",
     "https://prox.jvctrfelix.workers.dev/apresentacao"),
]

PASSOS = [
    ("01", "A gente conversa",
     "Trinta minutos para eu entender como a sua clínica funciona de verdade. Sem custo."),
    ("02", "Você testa em dias",
     "Recebe uma versão navegável rápido e usa com dado de verdade, não com exemplo."),
    ("03", "Entra no ar",
     "Publicado, com a equipe treinada e 30 dias de ajuste incluídos."),
]


def link_wa(numero, mensagem):
    from urllib.parse import quote
    return f"https://wa.me/{numero}?text={quote(mensagem)}"


def montar_html(dados, fontes):
    wa = dados["whatsapp"]
    esc = html.escape

    qr_site = qr_svg(dados["site"])
    qr_wa = qr_svg(link_wa(wa, "Oi! Recebi o seu convite e queria conversar."))

    problemas = "".join(
        f'<a class="dor" href="{esc(link_wa(wa, msg))}">'
        f"<h4>{esc(titulo)}</h4><p>{esc(linha)}</p>"
        f'<span class="go">Resolver isso ›</span></a>'
        for titulo, linha, msg in PROBLEMAS
    )
    sistemas = "".join(
        f'<a class="sis" href="{esc(url)}">'
        f'<div class="cod">{esc(cod)}</div><div class="para">{esc(para)}</div>'
        f"<p>{esc(linha)}</p>"
        f'<span class="go">Conheça de perto ›</span></a>'
        for cod, para, linha, url in SISTEMAS
    )
    passos = "".join(
        f'<div class="passo"><div class="d">{n}</div>'
        f"<h4>{esc(t)}</h4><p>{esc(d)}</p></div>"
        for n, t, d in PASSOS
    )

    substituicoes = {
        "{{FONTES}}": fontes,
        "{{NOME}}": esc(dados["nome"]),
        "{{CIDADE}}": esc(dados["cidade"]),
        "{{EMAIL}}": esc(dados["email"]),
        "{{INSTAGRAM_BLOCO}}": (
            f'<div><div class="k">Instagram</div>'
            f'<a class="v" href="https://instagram.com/{esc(dados["instagram"])}">'
            f'@{esc(dados["instagram"])}</a></div>'
            if dados["instagram"] else ""
        ),
        "{{SITE_URL}}": esc(dados["site"]),
        "{{SITE_TXT}}": esc(site_legivel(dados["site"])),
        "{{WA_TXT}}": esc(telefone_legivel(wa)),
        "{{WA_CAPA}}": esc(link_wa(wa, "Oi! Recebi o seu convite e queria conversar.")),
        "{{WA_DIAG}}": esc(link_wa(wa, "Oi! Queria marcar os 30 minutos de diagnóstico da minha clínica.")),
        "{{WA_OUTRO}}": esc(link_wa(wa, "Oi! O meu problema não está no convite, queria te contar.")),
        "{{QR_SITE}}": qr_site,
        "{{QR_WA}}": qr_wa,
        "{{PROBLEMAS}}": problemas,
        "{{SISTEMAS}}": sistemas,
        "{{PASSOS}}": passos,
    }

    with open(os.path.join(RAIZ, "convite.template.html"), encoding="utf-8") as arq:
        pagina = arq.read()
    for chave, valor in substituicoes.items():
        pagina = pagina.replace(chave, valor)
    return pagina


# --------------------------------------------------------------------------
# 5. PDF
# --------------------------------------------------------------------------
def achar_chrome():
    candidatos = [
        os.environ.get("CHROME_BIN", ""),
        "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for caminho in candidatos:
        if caminho and os.path.exists(caminho):
            return caminho
    for nome in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        achado = shutil.which(nome)
        if achado:
            return achado
    return None


def gerar_pdf(origem, destino):
    chrome = achar_chrome()
    if not chrome:
        print("! Chrome/Chromium não encontrado. Abra o convite.html e imprima em PDF.")
        return False
    subprocess.run(
        [
            chrome, "--headless", "--disable-gpu", "--no-sandbox",
            "--no-pdf-header-footer", "--generate-pdf-document-outline=false",
            f"--print-to-pdf={destino}", f"file://{origem}",
        ],
        check=True,
        capture_output=True,
    )
    return True


def main():
    dados = ler_config()
    for chave in ("email", "instagram"):
        if "exemplo" in dados[chave]:
            print(f"! atenção: `{chave}` ainda é o valor de exemplo do index.html.")

    caminho_html = os.path.join(RAIZ, "convite.html")
    caminho_pdf = os.path.join(RAIZ, "convite.pdf")

    with open(caminho_html, "w", encoding="utf-8") as arq:
        arq.write(montar_html(dados, montar_fontes()))
    print(f"· convite.html gerado ({os.path.getsize(caminho_html) // 1024} KB)")

    if gerar_pdf(caminho_html, caminho_pdf):
        print(f"· convite.pdf gerado ({os.path.getsize(caminho_pdf) // 1024} KB)")
        print(f"\n  Site:     {dados['site']}")
        print(f"  WhatsApp: {telefone_legivel(dados['whatsapp'])}")


if __name__ == "__main__":
    sys.exit(main())
