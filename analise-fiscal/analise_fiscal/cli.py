"""Linha de comando.

    python3 -m analise_fiscal 00000000000191
    python3 -m analise_fiscal 00.000.000/0001-91 11222333000181 --html saida.html
    python3 -m analise_fiscal --arquivo carteira.txt --json carteira.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from .analise import analisar_carteira
from .fontes import ErroDeFonte, FonteCadastro, FonteSancoes, HttpReal
from .relatorio import pagina, texto, texto_vinculos


def _ler_arquivo(caminho: str) -> list[str]:
    with open(caminho, encoding="utf-8") as arq:
        return [linha.strip() for linha in arq
                if linha.strip() and not linha.startswith("#")]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="analise_fiscal",
        description="Análise cadastral e fiscal a partir de fontes públicas.")
    p.add_argument("cnpjs", nargs="*", help="um ou mais CNPJs")
    p.add_argument("--arquivo", help="arquivo com um CNPJ por linha")
    p.add_argument("--html", help="grava o relatório em HTML no caminho indicado")
    p.add_argument("--json", dest="json_saida", help="grava o resultado em JSON")
    p.add_argument("--base-cadastro", default="https://brasilapi.com.br/api/cnpj/v1",
                   help="endpoint do espelho da base pública do CNPJ")
    p.add_argument("--chave-transparencia",
                   default=os.environ.get("CHAVE_TRANSPARENCIA"),
                   help="chave da API do Portal da Transparência (CEIS/CNEP). "
                        "Sem ela, as sanções não são consultadas.")
    p.add_argument("--sem-cor", action="store_true")
    args = p.parse_args(argv)

    cnpjs = list(args.cnpjs)
    if args.arquivo:
        cnpjs += _ler_arquivo(args.arquivo)
    if not cnpjs:
        p.error("informe ao menos um CNPJ, ou use --arquivo")

    http = HttpReal()
    cadastro = FonteCadastro(http, base=args.base_cadastro)
    sancoes = FonteSancoes(http, chave=args.chave_transparencia)

    analises, vinculos, erros = analisar_carteira(cnpjs, cadastro, sancoes)

    for analise in analises:
        print(texto(analise, cores=not args.sem_cor))
    if len(analises) > 1:
        print(texto_vinculos(vinculos))

    for erro in erros:
        print(f"  falhou — {erro}", file=sys.stderr)

    if args.html:
        with open(args.html, "w", encoding="utf-8") as arq:
            arq.write(pagina(analises, vinculos))
        print(f"  relatório gravado em {args.html}", file=sys.stderr)

    if args.json_saida:
        saida = {
            "analises": [a.como_dict() for a in analises],
            "vinculos": [
                {"socio": v.socio, "documento": v.documento,
                 "empresas": v.empresas, "qualificacoes": v.qualificacoes}
                for v in vinculos],
            "erros": erros,
        }
        with open(args.json_saida, "w", encoding="utf-8") as arq:
            json.dump(saida, arq, ensure_ascii=False, indent=2)
        print(f"  JSON gravado em {args.json_saida}", file=sys.stderr)

    if not analises:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
