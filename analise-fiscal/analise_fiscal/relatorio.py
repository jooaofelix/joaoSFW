"""Saída legível: terminal e HTML."""

from __future__ import annotations

import html
from datetime import date

from .modelo import Analise, Vinculo, cnpj_formatado

MARCA = {"alerta": "!!", "atencao": " !", "info": "  "}
COR = {"alerta": "\033[31m", "atencao": "\033[33m", "info": "\033[2m"}
FIM = "\033[0m"


def _dinheiro(valor: float | None) -> str:
    if valor is None:
        return "—"
    return f"R$ {valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


# --------------------------------------------------------------------------
# terminal
# --------------------------------------------------------------------------
def texto(analise: Analise, cores: bool = True) -> str:
    e = analise.empresa
    def pinta(nivel: str, txt: str) -> str:
        return f"{COR[nivel]}{txt}{FIM}" if cores else txt

    linhas = [
        "=" * 72,
        f"{e.razao_social or '(sem razão social)'}",
        f"{cnpj_formatado(e.cnpj)}"
        + (f"  ·  {e.nome_fantasia}" if e.nome_fantasia else ""),
        "=" * 72,
        f"  Situação      {e.situacao or '—'}",
        f"  Porte         {e.porte or '—'}",
        f"  Natureza      {e.natureza_juridica or '—'}",
        f"  Capital       {_dinheiro(e.capital_social)}",
        f"  Município     {e.municipio or '—'}{('/' + e.uf) if e.uf else ''}",
        f"  Atividade     {e.cnae_principal or '—'}",
    ]
    if e.cnaes_secundarios:
        linhas.append(f"  Secundárias   {len(e.cnaes_secundarios)} CNAE(s)")

    linhas.append("")
    linhas.append("  ANÁLISE")
    for a in analise.achados:
        linhas.append(pinta(a.nivel, f"  {MARCA[a.nivel]} {a.titulo}"))
        if a.detalhe:
            linhas.append(f"       {a.detalhe}")

    if e.socios:
        linhas += ["", f"  QUADRO SOCIETÁRIO ({len(e.socios)})"]
        for s in e.socios:
            entrada = f" · desde {s.entrada.strftime('%d/%m/%Y')}" if s.entrada else ""
            linhas.append(f"     {s.nome}")
            linhas.append(f"       {s.qualificacao or '—'}{entrada}")

    if analise.falhas:
        linhas += ["", "  NÃO VERIFICADO"]
        linhas += [f"     {f}" for f in analise.falhas]

    linhas += ["", f"  Fontes: {'; '.join(analise.fontes)}",
               f"  Gerado em {analise.gerado_em.strftime('%d/%m/%Y')}", ""]
    return "\n".join(linhas)


def texto_vinculos(vinculos: list[Vinculo]) -> str:
    if not vinculos:
        return "\n  Nenhum sócio em comum entre as empresas consultadas.\n"
    linhas = ["", "=" * 72, "  VÍNCULOS SOCIETÁRIOS", "=" * 72]
    for v in vinculos:
        linhas.append(f"  {v.socio}  ({len(v.empresas)} empresas)")
        for cnpj in v.empresas:
            linhas.append(f"     {cnpj_formatado(cnpj)} — "
                          f"{v.qualificacoes.get(cnpj, '—')}")
        linhas.append("")
    linhas.append("  O CPF na base pública vem mascarado: o cruzamento usa nome +")
    linhas.append("  máscara. Trate como indício a conferir, não como prova.")
    linhas.append("")
    return "\n".join(linhas)


# --------------------------------------------------------------------------
# HTML
# --------------------------------------------------------------------------
ESTILO = """
:root{--ink:#131A18;--pine:#0F4A3E;--pine-d:#0A2F27;--ochre:#8A5F17;
  --paper:#FCFBF6;--rule:#DFDACD;--mute:#5E635E;--wash:#F1EEE4;
  --alerta:#9B2C1E;--atencao:#8A5F17;}
*{box-sizing:border-box;margin:0;padding:0}
body{font:16px/1.55 system-ui,sans-serif;color:var(--ink);background:var(--paper);padding:32px}
.folha{max-width:900px;margin:0 auto 40px;border:1px solid var(--rule);border-radius:3px;
  background:#fff;overflow:hidden}
.topo{background:var(--pine-d);color:#FBF9F2;padding:24px 28px}
.topo h1{font-size:22px;line-height:1.2;font-weight:600}
.topo .doc{font-family:ui-monospace,monospace;font-size:13px;color:#C7A05A;margin-top:8px}
.campos{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
  background:#fff;border-bottom:1px solid var(--rule)}
.campo{padding:14px 18px;border-right:1px solid var(--rule);border-top:1px solid var(--rule)}
.campo:last-child{border-right:none}
.campo .k{font-family:ui-monospace,monospace;font-size:10px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ochre);margin-bottom:4px}
.campo .v{font-size:15px}
.bloco{padding:22px 28px;border-top:1px solid var(--rule)}
.bloco h2{font-size:11px;font-family:ui-monospace,monospace;letter-spacing:.16em;
  text-transform:uppercase;color:var(--ochre);margin-bottom:14px}
.achado{display:flex;gap:12px;padding:9px 0;border-bottom:1px solid var(--wash)}
.achado:last-child{border-bottom:none}
.tag{font-family:ui-monospace,monospace;font-size:9.5px;letter-spacing:.1em;
  text-transform:uppercase;padding:3px 7px;border-radius:2px;height:fit-content;
  flex-shrink:0;min-width:64px;text-align:center}
.n-alerta .tag{background:var(--alerta);color:#fff}
.n-atencao .tag{background:#F3E4C4;color:#6B4A11}
.n-info .tag{background:var(--wash);color:var(--mute)}
.achado .txt strong{font-weight:600;display:block}
.achado .txt span{font-size:14px;color:var(--mute)}
table{width:100%;border-collapse:collapse;font-size:14.5px}
th{font-family:ui-monospace,monospace;font-size:10px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--ochre);text-align:left;padding:0 0 8px}
td{padding:9px 0;border-top:1px solid var(--wash);vertical-align:top}
.rodape{padding:16px 28px;background:var(--wash);font-size:12.5px;color:var(--mute)}
.aviso{background:#FBF3E2;border-left:3px solid var(--ochre);padding:12px 16px;
  font-size:14px;color:#5C430F;margin-top:14px}
"""


def _achado_html(a) -> str:
    detalhe = f"<span>{html.escape(a.detalhe)}</span>" if a.detalhe else ""
    return (f'<div class="achado n-{a.nivel}"><span class="tag">{a.nivel}</span>'
            f'<div class="txt"><strong>{html.escape(a.titulo)}</strong>{detalhe}</div></div>')


def _folha(analise: Analise) -> str:
    e = analise.empresa
    campos = [("Situação", e.situacao), ("Porte", e.porte),
              ("Natureza jurídica", e.natureza_juridica),
              ("Capital social", _dinheiro(e.capital_social)),
              ("Município", f"{e.municipio}{('/' + e.uf) if e.uf else ''}"),
              ("Atividade principal", str(e.cnae_principal))]

    partes = [
        '<div class="folha">',
        f'<div class="topo"><h1>{html.escape(e.razao_social or "(sem razão social)")}</h1>',
        f'<div class="doc">{cnpj_formatado(e.cnpj)}'
        + (f' · {html.escape(e.nome_fantasia)}' if e.nome_fantasia else '')
        + '</div></div>',
        '<div class="campos">',
    ]
    for k, v in campos:
        partes.append(f'<div class="campo"><div class="k">{html.escape(k)}</div>'
                      f'<div class="v">{html.escape(str(v) or "—")}</div></div>')
    partes.append('</div>')

    partes.append('<div class="bloco"><h2>Análise</h2>')
    partes += [_achado_html(a) for a in analise.achados]
    partes.append('</div>')

    if e.socios:
        partes.append(f'<div class="bloco"><h2>Quadro societário ({len(e.socios)})</h2>'
                      '<table><tr><th>Sócio</th><th>Qualificação</th><th>Entrada</th></tr>')
        for s in e.socios:
            entrada = s.entrada.strftime("%d/%m/%Y") if s.entrada else "—"
            partes.append(f'<tr><td>{html.escape(s.nome)}</td>'
                          f'<td>{html.escape(s.qualificacao or "—")}</td>'
                          f'<td>{entrada}</td></tr>')
        partes.append('</table></div>')

    if analise.falhas:
        partes.append('<div class="bloco"><h2>Não verificado</h2>'
                      + "".join(f'<div class="aviso">{html.escape(f)}</div>'
                                for f in analise.falhas) + '</div>')

    partes.append(f'<div class="rodape">Fontes: {html.escape("; ".join(analise.fontes))}'
                  f' · gerado em {analise.gerado_em.strftime("%d/%m/%Y")}</div></div>')
    return "".join(partes)


def _folha_vinculos(vinculos: list[Vinculo]) -> str:
    if not vinculos:
        return ""
    linhas = ['<div class="folha"><div class="topo"><h1>Vínculos societários</h1>'
              f'<div class="doc">{len(vinculos)} pessoa(s) em mais de uma empresa</div>'
              '</div><div class="bloco"><table>'
              '<tr><th>Sócio</th><th>Empresas</th></tr>']
    for v in vinculos:
        empresas = "<br>".join(
            f'{cnpj_formatado(c)} — {html.escape(v.qualificacoes.get(c, "—"))}'
            for c in v.empresas)
        linhas.append(f'<tr><td><strong>{html.escape(v.socio)}</strong></td>'
                      f'<td>{empresas}</td></tr>')
    linhas.append('</table><div class="aviso">O CPF na base pública vem mascarado. '
                  'O cruzamento usa nome + máscara, então homônimo é possível: '
                  'trate como indício a conferir, não como prova.</div>'
                  '</div></div>')
    return "".join(linhas)


def pagina(analises: list[Analise], vinculos: list[Vinculo] | None = None,
           titulo: str = "Análise cadastral e fiscal") -> str:
    corpo = "".join(_folha(a) for a in analises)
    corpo += _folha_vinculos(vinculos or [])
    return (f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(titulo)}</title><style>{ESTILO}</style></head>'
            f'<body>{corpo}</body></html>')
