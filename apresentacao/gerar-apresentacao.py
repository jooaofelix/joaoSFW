#!/usr/bin/env python3
"""
Gera as apresentações de venda em PDF.

    python3 apresentacao/gerar-apresentacao.py            # todos os perfis
    python3 apresentacao/gerar-apresentacao.py psicologia # só um

Cada perfil em PERFIS aponta para um template e um PDF de saída: para quem é,
o segmento e os valores. O texto de cada apresentação fica no seu template; o
visual, em estilo.css, compartilhado por todas.

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
# EDITE AQUI — um bloco por apresentação
# --------------------------------------------------------------------------
NOME = "João Félix · Desata"

VALORES_PADRAO = {
    "preco_site": "R$ 900",            # "a partir de"
    "preco_site_cheio": "R$ 1.800",    # valor de tabela; "" = sem desconto
    "selo_site": "condição de primeiro projeto",   # "" = sem selo
    "preco_mensal": "R$ 150",          # acompanhamento opcional
}

PERFIS = {
    "sst": {
        "template": "apresentacao.template.html",
        "saida": "apresentacao-desata.pdf",
        "empresa": "Vallemed",
        "destinatario": "medicina e segurança do trabalho",
    },
    "psicologia": {
        "template": "psicologia.template.html",
        "saida": "apresentacao-psicologia.pdf",
        "empresa": "Alvo Psicologia",
        "destinatario": "psicologia clínica",
    },
}

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


def gerar(nome_perfil, perfil, dados, comuns):
    precos = dict(VALORES_PADRAO)
    precos.update({k: v for k, v in perfil.items() if k in VALORES_PADRAO})

    cheio, selo, preco = precos["preco_site_cheio"], precos["selo_site"], precos["preco_site"]
    de_site = f'<small class="de">de {cheio}</small>' if cheio else ""
    selo_site = f'<span class="selo">{selo}</span>' if selo else ""
    nota_desconto = (
        f" O valor de {preco} é uma condição de abertura, para os primeiros "
        "projetos da Desata, e vale para o escopo descrito nesta apresentação."
    ) if cheio else ""

    valores = dict(comuns)
    valores.update({
        "EMPRESA": perfil["empresa"],
        "DESTINATARIO": perfil["destinatario"],
        "PRECO_SITE": preco,
        "DE_SITE": de_site,
        "SELO_SITE": selo_site,
        "NOTA_DESCONTO": nota_desconto,
        "PRECO_MENSAL": precos["preco_mensal"],
    })

    with open(os.path.join(AQUI, perfil["template"]), encoding="utf-8") as arq:
        html = arq.read()
    for chave, valor in valores.items():
        html = html.replace("{{" + chave + "}}", valor)

    sobraram = re.findall(r"\{\{(\w+)\}\}", html)
    if sobraram:
        print("! marcadores sem valor em " + perfil["template"] + ": "
              + ", ".join(sorted(set(sobraram))))

    caminho_html = os.path.join(AQUI, f"_{nome_perfil}.html")
    caminho_pdf = os.path.join(AQUI, perfil["saida"])
    with open(caminho_html, "w", encoding="utf-8") as arq:
        arq.write(html)

    if not gerar_pdf(caminho_html, caminho_pdf):
        return False
    de = f" (de {cheio})" if cheio else ""
    print(f"· {perfil['saida']} ({os.path.getsize(caminho_pdf) // 1024} KB)"
          f" — {perfil['empresa']}: site {preco}{de} · mensal {precos['preco_mensal']}")
    return True


def main():
    dados = ler_config()
    faltando = [c for c in ("whatsapp", "email") if not dados[c]]
    if faltando:
        print("! faltam contatos em assets/js/config.js: " + ", ".join(faltando))
        return 1

    pedidos = sys.argv[1:] or list(PERFIS)
    desconhecidos = [p for p in pedidos if p not in PERFIS]
    if desconhecidos:
        print("! perfil desconhecido: " + ", ".join(desconhecidos))
        print("  disponíveis: " + ", ".join(PERFIS))
        return 1

    hoje = datetime.date.today()
    logo = os.path.join(RAIZ, "assets", "img", "logo-desata-colorido.png")
    logo_branco = os.path.join(RAIZ, "assets", "img", "logo-desata-branco.png")

    with open(os.path.join(AQUI, "estilo.css"), encoding="utf-8") as arq:
        estilo = arq.read()

    comuns = {
        "FONTES": montar_fontes(),
        "ESTILO": estilo,
        "LOGO_COR": embutir(logo, "image/png"),
        "LOGO_BRANCO": embutir(logo_branco, "image/png"),
        "NOME": NOME,
        "CIDADE": dados["local"],
        "DATA": f"{hoje.day} de {MESES[hoje.month - 1]} de {hoje.year}",
        "WHATSAPP": telefone_legivel(dados["whatsapp"]),
        "EMAIL": dados["email"],
        "SITE": dados["site"],
    }

    ok = all([gerar(nome, PERFIS[nome], dados, comuns) for nome in pedidos])
    return 0 if ok else 1



if __name__ == "__main__":
    sys.exit(main())
