"""Adaptadores das fontes públicas (nível 1).

Toda chamada de rede passa pelo objeto `http` injetado, então a análise inteira
roda offline nos testes. Os normalizadores aceitam vários nomes para o mesmo
campo porque as fontes que espelham a base da Receita divergem no detalhe —
confira contra uma resposta real antes de colocar em produção.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from typing import Any, Protocol

from .modelo import Cnae, Empresa, Sancao, Simples, Socio, so_digitos

TEMPO_LIMITE = 20


class ErroDeFonte(Exception):
    """Falha ao consultar uma fonte. Nunca derruba a análise inteira."""


class Http(Protocol):
    def __call__(self, url: str, cabecalhos: dict[str, str] | None = None) -> Any: ...


class HttpReal:
    """Cliente HTTP mínimo. Sem dependência externa de propósito."""

    def __init__(self, agente: str = "analise-fiscal/1.0") -> None:
        self.agente = agente

    def __call__(self, url: str, cabecalhos: dict[str, str] | None = None) -> Any:
        pedido = urllib.request.Request(url, headers={"User-Agent": self.agente,
                                                      **(cabecalhos or {})})
        try:
            with urllib.request.urlopen(pedido, timeout=TEMPO_LIMITE) as resposta:
                return json.loads(resposta.read().decode("utf-8"))
        except urllib.error.HTTPError as erro:
            if erro.code == 404:
                raise ErroDeFonte("não encontrado") from erro
            if erro.code == 429:
                raise ErroDeFonte("limite de consultas excedido") from erro
            raise ErroDeFonte(f"HTTP {erro.code}") from erro
        except (urllib.error.URLError, TimeoutError) as erro:
            raise ErroDeFonte(f"rede indisponível ({erro})") from erro
        except json.JSONDecodeError as erro:
            raise ErroDeFonte("resposta não era JSON") from erro


# --------------------------------------------------------------------------
# leitura tolerante
# --------------------------------------------------------------------------
def _campo(dados: dict, *nomes: str, padrao: Any = None) -> Any:
    for nome in nomes:
        if nome in dados and dados[nome] not in (None, ""):
            return dados[nome]
    return padrao


def _data(valor: Any) -> date | None:
    if not valor:
        return None
    if isinstance(valor, date):
        return valor
    texto = str(valor).strip()[:10]
    for formato in ("%Y-%m-%d", "%d/%m/%Y", "%Y%m%d"):
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            continue
    return None


def _decimal(valor: Any) -> float | None:
    if valor in (None, ""):
        return None
    if isinstance(valor, (int, float)):
        return float(valor)
    texto = str(valor).strip().replace(".", "").replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return None


def _booleano(valor: Any) -> bool | None:
    if valor in (None, ""):
        return None
    if isinstance(valor, bool):
        return valor
    return str(valor).strip().upper() in {"S", "SIM", "TRUE", "1", "T"}


# --------------------------------------------------------------------------
# cadastro do CNPJ (base pública da Receita, via espelho)
# --------------------------------------------------------------------------
def normalizar_empresa(bruto: dict) -> Empresa:
    """Converte a resposta de um espelho da base pública em `Empresa`."""
    cnae_principal = Cnae(
        codigo=str(_campo(bruto, "cnae_fiscal", "cnae_principal_codigo",
                          "codigo_cnae_fiscal", padrao="")),
        descricao=str(_campo(bruto, "cnae_fiscal_descricao", "cnae_principal_descricao",
                             "descricao_cnae_fiscal", padrao="")),
    )

    secundarios = []
    for item in _campo(bruto, "cnaes_secundarios", "cnaes_secundarias", padrao=[]) or []:
        if isinstance(item, dict):
            secundarios.append(Cnae(
                codigo=str(_campo(item, "codigo", "cnae", padrao="")),
                descricao=str(_campo(item, "descricao", "texto", padrao="")),
            ))

    socios = []
    for item in _campo(bruto, "qsa", "socios", padrao=[]) or []:
        if not isinstance(item, dict):
            continue
        socios.append(Socio(
            nome=str(_campo(item, "nome_socio", "nome", padrao="")),
            documento=str(_campo(item, "cnpj_cpf_do_socio", "documento_socio",
                                 "cpf_cnpj_socio", padrao="")),
            qualificacao=str(_campo(item, "qualificacao_socio", "qualificacao",
                                    padrao="")),
            entrada=_data(_campo(item, "data_entrada_sociedade", "data_entrada")),
            pais=str(_campo(item, "pais", padrao="")),
        ))

    return Empresa(
        cnpj=so_digitos(str(_campo(bruto, "cnpj", "cnpj_raiz", padrao=""))),
        razao_social=str(_campo(bruto, "razao_social", "nome", padrao="")),
        nome_fantasia=str(_campo(bruto, "nome_fantasia", "fantasia", padrao="")),
        situacao=str(_campo(bruto, "descricao_situacao_cadastral", "situacao_cadastral",
                            "situacao", padrao="")),
        data_situacao=_data(_campo(bruto, "data_situacao_cadastral", "data_situacao")),
        motivo_situacao=str(_campo(bruto, "descricao_motivo_situacao_cadastral",
                                   "motivo_situacao_cadastral", padrao="")),
        data_abertura=_data(_campo(bruto, "data_inicio_atividade", "data_abertura")),
        porte=str(_campo(bruto, "descricao_porte", "porte", padrao="")),
        natureza_juridica=str(_campo(bruto, "natureza_juridica", padrao="")),
        capital_social=_decimal(_campo(bruto, "capital_social")),
        cnae_principal=cnae_principal,
        cnaes_secundarios=secundarios,
        municipio=str(_campo(bruto, "municipio", "cidade", padrao="")),
        uf=str(_campo(bruto, "uf", "estado", padrao="")),
        simples=Simples(
            optante=_booleano(_campo(bruto, "opcao_pelo_simples", "simples_optante")),
            data_opcao=_data(_campo(bruto, "data_opcao_pelo_simples",
                                    "simples_data_opcao")),
            data_exclusao=_data(_campo(bruto, "data_exclusao_do_simples",
                                       "simples_data_exclusao")),
        ),
        mei=Simples(
            optante=_booleano(_campo(bruto, "opcao_pelo_mei", "mei_optante")),
            data_opcao=_data(_campo(bruto, "data_opcao_pelo_mei", "mei_data_opcao")),
            data_exclusao=_data(_campo(bruto, "data_exclusao_do_mei",
                                       "mei_data_exclusao")),
        ),
        socios=socios,
    )


class FonteCadastro:
    """Cadastro completo + opção pelo Simples/MEI.

    Consulta ao vivo, boa para volume baixo. Para escritório com centenas de
    clientes, o caminho é carregar o dump mensal dos Dados Abertos da Receita
    e consultar o próprio banco — veja `dados_abertos.py`.
    """

    nome = "Cadastro CNPJ (base pública da Receita)"

    def __init__(self, http: Http, base: str = "https://brasilapi.com.br/api/cnpj/v1"):
        self.http = http
        self.base = base.rstrip("/")

    def consultar(self, cnpj: str) -> Empresa:
        bruto = self.http(f"{self.base}/{so_digitos(cnpj)}")
        if not isinstance(bruto, dict):
            raise ErroDeFonte("formato inesperado")
        return normalizar_empresa(bruto)


# --------------------------------------------------------------------------
# sanções (Portal da Transparência)
# --------------------------------------------------------------------------
class FonteSancoes:
    """CEIS e CNEP. Exige chave gratuita do Portal da Transparência.

    Sem chave a fonte é simplesmente pulada — a análise continua e registra
    a ausência, em vez de fingir que não há sanção.
    """

    nome = "Sanções (CEIS/CNEP — Portal da Transparência)"

    def __init__(self, http: Http, chave: str | None = None,
                 base: str = "https://api.portaldatransparencia.gov.br/api-de-dados"):
        self.http = http
        self.chave = chave
        self.base = base.rstrip("/")

    @property
    def disponivel(self) -> bool:
        return bool(self.chave)

    def consultar(self, cnpj: str) -> list[Sancao]:
        if not self.disponivel:
            raise ErroDeFonte("sem chave de API configurada")
        achados: list[Sancao] = []
        for caminho, rotulo in (("ceis", "CEIS"), ("cnep", "CNEP")):
            consulta = urllib.parse.urlencode({"cnpjSancionado": so_digitos(cnpj),
                                               "pagina": 1})
            dados = self.http(f"{self.base}/{caminho}?{consulta}",
                              {"chave-api-dados": self.chave})
            for item in dados or []:
                if not isinstance(item, dict):
                    continue
                sancao = item.get("sancao") or {}
                achados.append(Sancao(
                    fonte=rotulo,
                    tipo=str(_campo(item, "tipoSancao", padrao="") or
                             _campo(sancao, "tipoSancao", padrao="")),
                    orgao=str(_campo(item, "orgaoSancionador", padrao="")),
                    inicio=_data(_campo(item, "dataInicioSancao",
                                        "dataPublicacaoSancao")),
                    fim=_data(_campo(item, "dataFimSancao")),
                    descricao=str(_campo(item, "textoPublicacao", padrao=""))[:400],
                ))
        return achados
