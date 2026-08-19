"""Estruturas do resultado consolidado.

Tudo aqui é dado puro, sem I/O — o que permite testar as regras de análise
sem tocar na rede.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Any


# --------------------------------------------------------------------------
# CNPJ
# --------------------------------------------------------------------------
def so_digitos(valor: str) -> str:
    return re.sub(r"\D", "", valor or "")


def cnpj_valido(cnpj: str) -> bool:
    """Valida os dois dígitos verificadores."""
    n = so_digitos(cnpj)
    if len(n) != 14 or n == n[0] * 14:
        return False
    for tamanho in (12, 13):
        pesos = list(range(tamanho - 7, 1, -1)) + list(range(9, 1, -1))
        soma = sum(int(d) * p for d, p in zip(n[:tamanho], pesos))
        resto = soma % 11
        digito = 0 if resto < 2 else 11 - resto
        if int(n[tamanho]) != digito:
            return False
    return True


def cnpj_formatado(cnpj: str) -> str:
    n = so_digitos(cnpj)
    if len(n) != 14:
        return cnpj
    return f"{n[:2]}.{n[2:5]}.{n[5:8]}/{n[8:12]}-{n[12:]}"


def cpf_mascarado(doc: str) -> str:
    """A Receita já publica o CPF do sócio mascarado; normaliza o formato."""
    n = so_digitos(doc)
    if len(n) == 11:
        return f"***{n[3:9]}**"
    return doc or ""


# --------------------------------------------------------------------------
# entidades
# --------------------------------------------------------------------------
@dataclass
class Cnae:
    codigo: str = ""
    descricao: str = ""

    def __str__(self) -> str:
        return f"{self.codigo} — {self.descricao}".strip(" —")


@dataclass
class Socio:
    nome: str = ""
    documento: str = ""
    qualificacao: str = ""
    entrada: date | None = None
    pais: str = ""

    @property
    def chave(self) -> str:
        """Identificador para cruzar sócios entre empresas.

        O CPF vem mascarado na base pública (só os 6 dígitos do meio), então
        sozinho ele não identifica. Nome + máscara erra bem menos.
        """
        return f"{self.nome.strip().upper()}|{so_digitos(self.documento)}"


@dataclass
class Simples:
    optante: bool | None = None
    data_opcao: date | None = None
    data_exclusao: date | None = None


@dataclass
class Empresa:
    cnpj: str = ""
    razao_social: str = ""
    nome_fantasia: str = ""
    situacao: str = ""
    data_situacao: date | None = None
    motivo_situacao: str = ""
    data_abertura: date | None = None
    porte: str = ""
    natureza_juridica: str = ""
    capital_social: float | None = None
    cnae_principal: Cnae = field(default_factory=Cnae)
    cnaes_secundarios: list[Cnae] = field(default_factory=list)
    municipio: str = ""
    uf: str = ""
    simples: Simples = field(default_factory=Simples)
    mei: Simples = field(default_factory=Simples)
    socios: list[Socio] = field(default_factory=list)

    @property
    def ativa(self) -> bool:
        return self.situacao.strip().upper() == "ATIVA"

    @property
    def idade_anos(self) -> int | None:
        if not self.data_abertura:
            return None
        hoje = date.today()
        return hoje.year - self.data_abertura.year - (
            (hoje.month, hoje.day) < (self.data_abertura.month, self.data_abertura.day)
        )


@dataclass
class Sancao:
    fonte: str = ""
    tipo: str = ""
    orgao: str = ""
    inicio: date | None = None
    fim: date | None = None
    descricao: str = ""

    @property
    def vigente(self) -> bool:
        hoje = date.today()
        if self.inicio and self.inicio > hoje:
            return False
        return self.fim is None or self.fim >= hoje


NIVEIS = ("info", "atencao", "alerta")


@dataclass
class Achado:
    """Uma conclusão da análise, não um dado bruto."""
    nivel: str
    codigo: str
    titulo: str
    detalhe: str = ""

    def __post_init__(self) -> None:
        if self.nivel not in NIVEIS:
            raise ValueError(f"nível inválido: {self.nivel}")

    @property
    def peso(self) -> int:
        return NIVEIS.index(self.nivel)


@dataclass
class Vinculo:
    """Duas empresas que compartilham a mesma pessoa no quadro societário."""
    socio: str
    documento: str
    empresas: list[str] = field(default_factory=list)   # CNPJs
    qualificacoes: dict[str, str] = field(default_factory=dict)


@dataclass
class Analise:
    empresa: Empresa
    sancoes: list[Sancao] = field(default_factory=list)
    achados: list[Achado] = field(default_factory=list)
    fontes: list[str] = field(default_factory=list)
    falhas: list[str] = field(default_factory=list)
    gerado_em: date = field(default_factory=date.today)

    @property
    def pior_nivel(self) -> str:
        return max((a.nivel for a in self.achados), key=NIVEIS.index, default="info")

    def como_dict(self) -> dict[str, Any]:
        def converte(o: Any) -> Any:
            if isinstance(o, date):
                return o.isoformat()
            if isinstance(o, dict):
                return {k: converte(v) for k, v in o.items()}
            if isinstance(o, list):
                return [converte(v) for v in o]
            return o
        return converte(asdict(self))
