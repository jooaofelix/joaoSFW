#!/usr/bin/env python3
"""
Gera a apresentação de venda em PDF (apresentacao-desata.pdf).

    python3 apresentacao/gerar-apresentacao.py

O texto fica em apresentacao.template.html. Aqui ficam só os dados que mudam
de um envio para o outro: para quem é, o segmento e os valores.

Os contatos vêm de assets/js/config.js — o mesmo arquivo que o site usa.
Requisito: Chromium ou Google Chrome instalado.
"""

import base64
import datetime
import os
import re
import shutil
import subprocess
import sys

# --------------------------------------------------------------------------
# EDITE AQUI
# --------------------------------------------------------------------------
EMPRESA = "Vallemed"                                  # quem vai receber
DESTINATARIO = "medicina e segurança do trabalho"     # aparece na capa
PRECO_SITE = "R$ 1.800"                               # "a partir de"
PRECO_MENSAL = "R$ 150"                               # acompanhamento opcional
NOME = "João Félix · Desata"

# --------------------------------------------------------------------------
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AQUI = os.path.dirname(os.path.abspath(__file__))

MESES = ("janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro")

PADRAO = {"whatsapp": "", "email": "", "local": "", "site": "desata.jvctrfelix.workers.dev"}


def ler_config():
    """Lê os contatos de assets/js/config.js — mesma fonte do site."""
    dados = dict(PADRAO)
    caminho = os.path.join(RAIZ, "assets", "js", "config.js")
    try:
        with open(caminho, encoding="utf-8") as arq:
            fonte = arq.read()
    except OSError:
        print("! assets/js/config.js não encontrado.")
        return dados

    bloco = re.search(r"DESATA_CONFIG\s*=\s*\{(.*?)\n\};", fonte, re.S)
    if not bloco:
        print("! bloco `DESATA_CONFIG` não encontrado.")
        return dados

    for chave in ("whatsapp", "email", "local"):
        achou = re.search(rf'\b{chave}\s*:\s*"([^"]*)"', bloco.group(1))
        if achou:
            dados[chave] = achou.group(1).strip()
    dados["whatsapp"] = re.sub(r"\D", "", dados["whatsapp"])
    return dados


def telefone_legivel(numero):
    achou = re.match(r"^55(\d{2})(\d{4,5})(\d{4})$", numero)
    return f"({achou.group(1)}) {achou.group(2)}-{achou.group(3)}" if achou else numero


def embutir(caminho, tipo):
    """Arquivo -> data URI, para o PDF não depender de rede nem de caminho."""
    with open(caminho, "rb") as arq:
        return f"data:{tipo};base64," + base64.b64encode(arq.read()).decode("ascii")


def montar_fontes():
    """@font-face da Figtree com os woff2 do site embutidos em base64."""
    blocos = []
    for nome, faixa in (
        ("figtree-latin.woff2", "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, "
                                "U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, "
                                "U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"),
        ("figtree-latin-ext.woff2", "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, "
                                    "U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, "
                                    "U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, "
                                    "U+2113, U+2C60-2C7F, U+A720-A7FF"),
    ):
        caminho = os.path.join(RAIZ, "assets", "fonts", nome)
        if not os.path.exists(caminho):
            print(f"! fonte não encontrada: {caminho}")
            continue
        uri = embutir(caminho, "font/woff2")
        blocos.append(
            "@font-face{font-family:'Figtree';font-style:normal;font-weight:400 900;"
            f"src:url({uri}) format('woff2');unicode-range:{faixa};}}"
        )
    return "\n".join(blocos)


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
        print("! Chrome/Chromium não encontrado. Abra o HTML gerado e imprima em PDF.")
        return False
    subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox",
         "--no-pdf-header-footer", "--generate-pdf-document-outline=false",
         f"--print-to-pdf={destino}", f"file://{origem}"],
        check=True, capture_output=True,
    )
    return True


def main():
    dados = ler_config()
    faltando = [c for c in ("whatsapp", "email") if not dados[c]]
    if faltando:
        print("! faltam contatos em assets/js/config.js: " + ", ".join(faltando))
        return 1

    hoje = datetime.date.today()
    logo = os.path.join(RAIZ, "assets", "img", "logo-desata-colorido.png")
    logo_branco = os.path.join(RAIZ, "assets", "img", "logo-desata-branco.png")

    valores = {
        "FONTES": montar_fontes(),
        "LOGO_COR": embutir(logo, "image/png"),
        "LOGO_BRANCO": embutir(logo_branco, "image/png"),
        "EMPRESA": EMPRESA,
        "DESTINATARIO": DESTINATARIO,
        "NOME": NOME,
        "CIDADE": dados["local"],
        "DATA": f"{hoje.day} de {MESES[hoje.month - 1]} de {hoje.year}",
        "WHATSAPP": telefone_legivel(dados["whatsapp"]),
        "EMAIL": dados["email"],
        "SITE": dados["site"],
        "PRECO_SITE": PRECO_SITE,
        "PRECO_MENSAL": PRECO_MENSAL,
    }

    with open(os.path.join(AQUI, "apresentacao.template.html"), encoding="utf-8") as arq:
        html = arq.read()
    for chave, valor in valores.items():
        html = html.replace("{{" + chave + "}}", valor)

    sobraram = re.findall(r"\{\{(\w+)\}\}", html)
    if sobraram:
        print("! marcadores sem valor no template: " + ", ".join(sorted(set(sobraram))))

    caminho_html = os.path.join(AQUI, "apresentacao.html")
    caminho_pdf = os.path.join(AQUI, "apresentacao-desata.pdf")
    with open(caminho_html, "w", encoding="utf-8") as arq:
        arq.write(html)
    print(f"· apresentacao.html gerado ({os.path.getsize(caminho_html) // 1024} KB)")

    if gerar_pdf(caminho_html, caminho_pdf):
        print(f"· apresentacao-desata.pdf gerado ({os.path.getsize(caminho_pdf) // 1024} KB)")
        print(f"\n  Para:     {EMPRESA}")
        print(f"  Site:     {PRECO_SITE} · Mensal: {PRECO_MENSAL}")
        print(f"  WhatsApp: {valores['WHATSAPP']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
