#!/usr/bin/env python3
"""Roda a análise com dados de exemplo, sem tocar na rede.

    python3 exemplo.py            # imprime no terminal
    python3 exemplo.py --html     # gera exemplo.html

Serve para ver o formato da saída e para demonstrar a ferramenta para um
cliente antes de ligar nas fontes de verdade.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from analise_fiscal.analise import analisar_carteira
from analise_fiscal.fontes import FonteCadastro
from analise_fiscal.relatorio import pagina, texto, texto_vinculos

RAIZ = Path(__file__).parent
FIXTURES = RAIZ / "tests" / "fixtures"

EXEMPLOS = {
    "11222333000181": "cadastro_ativa_simples.json",
    "44555666000181": "cadastro_baixada.json",
    "77888999000181": "cadastro_mei_campos_alternativos.json",
}


class HttpDeExemplo:
    def __call__(self, url, cabecalhos=None):
        for cnpj, arquivo in EXEMPLOS.items():
            if cnpj in url:
                return json.loads((FIXTURES / arquivo).read_text(encoding="utf-8"))
        raise RuntimeError(f"sem exemplo para {url}")


def main() -> int:
    cadastro = FonteCadastro(HttpDeExemplo())
    analises, vinculos, erros = analisar_carteira(list(EXEMPLOS), cadastro)

    if "--html" in sys.argv:
        destino = RAIZ / "exemplo.html"
        destino.write_text(pagina(analises, vinculos), encoding="utf-8")
        print(f"gerado: {destino}")
        return 0

    for analise in analises:
        print(texto(analise, cores=sys.stdout.isatty()))
    print(texto_vinculos(vinculos))
    for erro in erros:
        print(f"  falhou — {erro}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
