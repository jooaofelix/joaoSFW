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
    "email": "contato@exemplo.com.br",
    "instagram": "joaofelix",
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
# (rótulo visível, mensagem que já chega escrita no WhatsApp)
AREAS = [
    ("01", "Financeiro", [
        ("Fechar o mês sem perder um sábado", "Oi! Queria resolver o fechamento do mês — hoje me toma tempo demais."),
        ("Saber quem ainda não pagou", "Oi! Queria conseguir ver quem ainda não me pagou, sem caçar em planilha."),
        ("Lançar pelo WhatsApp, sem planilha", "Oi! Queria lançar entrada e saída pelo WhatsApp, sem abrir planilha."),
        ("Organizar notas e XML de NF-e", "Oi! Queria organizar as notas fiscais e os XMLs automaticamente."),
    ]),
    ("02", "Organização e agenda", [
        ("Tudo do paciente numa tela só", "Oi! Queria juntar cadastro, agenda e histórico num lugar só."),
        ("Agenda que o paciente marca sozinho", "Oi! Queria uma agenda em que o próprio paciente marca o horário."),
        ("Parar de redigitar o mesmo dado", "Oi! Queria parar de redigitar o mesmo dado em lugares diferentes."),
        ("Sair da planilha sem perder nada", "Oi! Queria tirar meu controle da planilha sem perder o que já tenho."),
    ]),
    ("03", "Documentos", [
        ("Documento que se preenche sozinho", "Oi! Queria que meus documentos saíssem preenchidos automaticamente."),
        ("Relatório pronto em um clique", "Oi! Queria gerar relatório de evolução sem montar do zero toda vez."),
        ("Achar o arquivo assinado na hora", "Oi! Queria um lugar único pra guardar e achar documento assinado."),
        ("Coletar assinatura e consentimento", "Oi! Queria coletar assinatura e consentimento de forma digital."),
    ]),
    ("04", "Mensagens", [
        ("Lembrete de consulta automático", "Oi! Queria enviar lembrete de consulta automaticamente."),
        ("Reduzir falta com confirmação", "Oi! Queria reduzir as faltas com confirmação automática."),
        ("Cobrar sem ter que cobrar", "Oi! Queria avisar quem está com pagamento em aberto, sem cobrar na mão."),
        ("Chamar de volta quem sumiu", "Oi! Queria chamar de volta paciente que sumiu faz tempo."),
    ]),
    ("05", "Acompanhamento", [
        ("Ver a evolução em gráfico", "Oi! Queria acompanhar a evolução do paciente ao longo do tempo."),
        ("Paciente registra entre as sessões", "Oi! Queria que o paciente registrasse dados entre as sessões."),
        ("Questionário com resultado somado", "Oi! Queria aplicar questionário ou escala e ver o resultado somado."),
        ("Painel com os números do mês", "Oi! Queria um painel com os números do meu consultório."),
    ]),
    ("06", "Equipe e processos", [
        ("Ver em que pé está cada caso", "Oi! Queria ver em que pé está cada processo da minha equipe."),
        ("Responsável e prazo por etapa", "Oi! Queria definir responsável e prazo pra cada etapa do processo."),
        ("Alerta antes de vencer o prazo", "Oi! Queria receber alerta antes de vencer prazo importante."),
        ("Controlar quem vê o quê", "Oi! Queria controlar quem da equipe vê o quê."),
    ]),
]

PASSOS = [
    ("01", "Conversa de diagnóstico",
     "Uma conversa para eu entender o processo real — inclusive as gambiarras. Sem custo."),
    ("02", "Protótipo funcionando",
     "Uma primeira versão navegável em poucos dias, testada com dado de verdade."),
    ("03", "Ajuste e entrega",
     "A gente refina em cima do uso. Entrego publicado, com treinamento."),
    ("04", "O sistema é seu",
     "Sem mensalidade de plataforma. Roda em infraestrutura sua, com os seus dados."),
]

CASOS = [
    ("Prática clínica", "Acompanhamento diário de bem-estar",
     "A sessão começa com o histórico já na mesa."),
    ("Escritório contábil", "Central de processos societários",
     "Ninguém mais pergunta “em que pé está?”."),
    ("Gestão financeira", "Controle de caixa pelo WhatsApp",
     "Fechamento do mês deixou de ser um sábado."),
]


def link_wa(numero, mensagem):
    from urllib.parse import quote
    return f"https://wa.me/{numero}?text={quote(mensagem)}"


def montar_html(dados, fontes):
    wa = dados["whatsapp"]
    esc = html.escape

    qr_site = qr_svg(dados["site"])
    qr_wa = qr_svg(link_wa(wa, "Oi! Recebi o seu convite e queria conversar."))

    areas = []
    for numero, titulo, itens in AREAS:
        linhas = "".join(
            f'<li><a href="{esc(link_wa(wa, msg))}">{esc(rotulo)}'
            f'<span class="go">›</span></a></li>'
            for rotulo, msg in itens
        )
        areas.append(
            f'<div class="area"><div class="n">{numero}</div>'
            f"<h3>{esc(titulo)}</h3><ul>{linhas}</ul></div>"
        )

    passos = "".join(
        f'<div class="passo"><div class="d">{n}</div>'
        f"<h4>{esc(t)}</h4><p>{esc(d)}</p></div>"
        for n, t, d in PASSOS
    )
    casos = "".join(
        f'<div class="caso"><div class="who">{esc(q)}</div>'
        f"<h4>{esc(t)}</h4><p>{esc(r)}</p></div>"
        for q, t, r in CASOS
    )

    substituicoes = {
        "{{FONTES}}": fontes,
        "{{NOME}}": esc(dados["nome"]),
        "{{CIDADE}}": esc(dados["cidade"]),
        "{{EMAIL}}": esc(dados["email"]),
        "{{INSTAGRAM}}": esc(dados["instagram"]),
        "{{SITE_URL}}": esc(dados["site"]),
        "{{SITE_TXT}}": esc(site_legivel(dados["site"])),
        "{{WA_TXT}}": esc(telefone_legivel(wa)),
        "{{WA_CAPA}}": esc(link_wa(wa, "Oi! Recebi o seu convite e queria conversar.")),
        "{{WA_DIAG}}": esc(link_wa(wa, "Oi! Queria marcar os 30 minutos de diagnóstico.")),
        "{{WA_OUTRO}}": esc(link_wa(wa, "Oi! A minha situação não está no convite, queria te contar o meu caso.")),
        "{{QR_SITE}}": qr_site,
        "{{QR_WA}}": qr_wa,
        "{{AREAS}}": "".join(areas),
        "{{PASSOS}}": passos,
        "{{CASOS}}": casos,
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
