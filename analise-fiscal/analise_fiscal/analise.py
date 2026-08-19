"""Orquestração, regras e vínculos societários.

A parte que gera valor não é buscar o dado — é a conclusão em cima dele.
Cada regra vira um `Achado` com nível, para a tela poder ordenar por gravidade.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date

from .fontes import ErroDeFonte, FonteCadastro, FonteSancoes
from .modelo import (Achado, Analise, Empresa, Vinculo, cnpj_formatado,
                     cnpj_valido, so_digitos)

# CNAEs impedidos de optar pelo Simples Nacional.
# Deixado vazio de propósito: a lista muda por lei complementar e depende de
# interpretação. Preencha com a relação que o seu escritório usa — enquanto
# estiver vazia, a análise diz que não verificou, em vez de dar um falso "ok".
CNAES_VEDADOS_SIMPLES: set[str] = set()


# --------------------------------------------------------------------------
# regras
# --------------------------------------------------------------------------
def _situacao(empresa: Empresa) -> list[Achado]:
    situacao = empresa.situacao.strip().upper()
    if not situacao:
        return [Achado("atencao", "situacao_ausente",
                       "Situação cadastral não informada pela fonte")]
    if situacao == "ATIVA":
        return [Achado("info", "situacao_ativa", "Situação cadastral ativa")]

    detalhe = empresa.motivo_situacao or "sem motivo informado"
    if empresa.data_situacao:
        detalhe += f" · desde {empresa.data_situacao.strftime('%d/%m/%Y')}"
    return [Achado("alerta", f"situacao_{situacao.lower()}",
                   f"Situação cadastral: {empresa.situacao}", detalhe)]


def _regime(empresa: Empresa) -> list[Achado]:
    achados: list[Achado] = []
    simples, mei = empresa.simples, empresa.mei
    hoje = date.today()

    if simples.optante:
        quando = (f" desde {simples.data_opcao.strftime('%d/%m/%Y')}"
                  if simples.data_opcao else "")
        achados.append(Achado("info", "simples_optante",
                              f"Optante pelo Simples Nacional{quando}"))
    elif simples.optante is False:
        achados.append(Achado("info", "simples_nao_optante",
                              "Não optante pelo Simples Nacional"))
    else:
        achados.append(Achado("atencao", "simples_indefinido",
                              "Opção pelo Simples não informada pela fonte"))

    if simples.data_exclusao and simples.data_exclusao <= hoje:
        achados.append(Achado(
            "atencao", "simples_excluido",
            f"Excluído do Simples em {simples.data_exclusao.strftime('%d/%m/%Y')}",
            "Confirme o motivo e se houve reinclusão."))

    if mei.optante:
        quando = (f" desde {mei.data_opcao.strftime('%d/%m/%Y')}"
                  if mei.data_opcao else "")
        achados.append(Achado("info", "mei", f"Enquadrado como MEI{quando}"))

    if simples.optante and (empresa.porte or "").strip().upper().startswith("DEMAIS"):
        achados.append(Achado(
            "atencao", "porte_incoerente",
            "Optante pelo Simples com porte 'DEMAIS'",
            "O porte no cadastro costuma acompanhar o enquadramento. "
            "Vale conferir se o cadastro está desatualizado."))
    return achados


def _atividade(empresa: Empresa) -> list[Achado]:
    achados: list[Achado] = []
    if not empresa.cnae_principal.codigo:
        achados.append(Achado("atencao", "cnae_ausente",
                              "CNAE principal não informado pela fonte"))
        return achados

    achados.append(Achado("info", "cnae_principal",
                          f"Atividade principal: {empresa.cnae_principal}"))

    if not CNAES_VEDADOS_SIMPLES:
        achados.append(Achado(
            "info", "vedacao_nao_verificada",
            "Vedação do Simples por CNAE não verificada",
            "A lista de CNAEs vedados está vazia nesta instalação. "
            "Preencha CNAES_VEDADOS_SIMPLES para ativar a checagem."))
        return achados

    codigos = {so_digitos(empresa.cnae_principal.codigo)} | {
        so_digitos(c.codigo) for c in empresa.cnaes_secundarios}
    vedados = sorted(codigos & {so_digitos(c) for c in CNAES_VEDADOS_SIMPLES})
    if vedados and empresa.simples.optante:
        achados.append(Achado(
            "alerta", "cnae_vedado_optante",
            "Optante pelo Simples com CNAE na lista de vedados",
            f"CNAEs: {', '.join(vedados)}. Confira a atividade efetiva."))
    elif vedados:
        achados.append(Achado("atencao", "cnae_vedado",
                              "Possui CNAE na lista de vedados ao Simples",
                              f"CNAEs: {', '.join(vedados)}"))
    return achados


def _perfil(empresa: Empresa) -> list[Achado]:
    achados: list[Achado] = []
    idade = empresa.idade_anos
    if empresa.data_abertura:
        achados.append(Achado(
            "info", "abertura",
            f"Aberta em {empresa.data_abertura.strftime('%d/%m/%Y')}"
            + (f" · {idade} ano(s)" if idade is not None else "")))
        if idade == 0:
            achados.append(Achado("info", "empresa_nova",
                                  "Empresa aberta há menos de um ano"))

    if empresa.capital_social is not None and empresa.capital_social <= 0:
        achados.append(Achado("atencao", "capital_zerado",
                              "Capital social igual a zero no cadastro"))

    if not empresa.socios:
        achados.append(Achado("info", "sem_qsa",
                              "Quadro societário não retornado",
                              "Normal para MEI e empresário individual."))
    return achados


def _sancoes(analise: Analise) -> list[Achado]:
    vigentes = [s for s in analise.sancoes if s.vigente]
    if vigentes:
        return [Achado(
            "alerta", "sancao_vigente",
            f"{len(vigentes)} sanção(ões) vigente(s)",
            "; ".join(f"{s.fonte}: {s.tipo or 'sem tipo'}" for s in vigentes[:3]))]
    if analise.sancoes:
        return [Achado("atencao", "sancao_encerrada",
                       f"{len(analise.sancoes)} sanção(ões) já encerrada(s)")]
    return []


REGRAS_EMPRESA = (_situacao, _regime, _atividade, _perfil)


def avaliar(analise: Analise) -> list[Achado]:
    achados: list[Achado] = []
    for regra in REGRAS_EMPRESA:
        achados.extend(regra(analise.empresa))
    achados.extend(_sancoes(analise))
    achados.sort(key=lambda a: -a.peso)
    return achados


# --------------------------------------------------------------------------
# consulta
# --------------------------------------------------------------------------
def analisar(cnpj: str, cadastro: FonteCadastro,
             sancoes: FonteSancoes | None = None) -> Analise:
    """Consulta as fontes de nível 1 e devolve a análise consolidada.

    A falha de uma fonte não derruba as outras: ela é registrada em `falhas`
    para o relatório poder dizer o que não foi verificado.
    """
    if not cnpj_valido(cnpj):
        raise ValueError(f"CNPJ inválido: {cnpj}")

    empresa = cadastro.consultar(cnpj)
    if not empresa.cnpj:
        empresa.cnpj = so_digitos(cnpj)
    analise = Analise(empresa=empresa, fontes=[cadastro.nome])

    if sancoes is not None:
        try:
            analise.sancoes = sancoes.consultar(cnpj)
            analise.fontes.append(sancoes.nome)
        except ErroDeFonte as erro:
            analise.falhas.append(f"{sancoes.nome}: {erro}")

    analise.achados = avaliar(analise)
    return analise


# --------------------------------------------------------------------------
# vínculos societários
# --------------------------------------------------------------------------
def cruzar_vinculos(analises: list[Analise]) -> list[Vinculo]:
    """Encontra sócios que aparecem em mais de uma das empresas consultadas.

    Cuidado ao ler o resultado: o CPF na base pública vem mascarado, então o
    cruzamento usa nome + máscara. Homônimo com a mesma máscara é raro, mas
    possível — trate como indício a conferir, não como prova.
    """
    por_socio: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for analise in analises:
        for socio in analise.empresa.socios:
            if not socio.nome.strip():
                continue
            por_socio[socio.chave].append(
                (analise.empresa.cnpj, socio.nome, socio.qualificacao))

    vinculos: list[Vinculo] = []
    for chave, ocorrencias in por_socio.items():
        cnpjs = sorted({cnpj for cnpj, _, _ in ocorrencias})
        if len(cnpjs) < 2:
            continue
        nome = ocorrencias[0][1]
        vinculos.append(Vinculo(
            socio=nome,
            documento=chave.split("|", 1)[1],
            empresas=cnpjs,
            qualificacoes={cnpj: qual for cnpj, _, qual in ocorrencias},
        ))
    vinculos.sort(key=lambda v: (-len(v.empresas), v.socio))
    return vinculos


def analisar_carteira(cnpjs: list[str], cadastro: FonteCadastro,
                      sancoes: FonteSancoes | None = None
                      ) -> tuple[list[Analise], list[Vinculo], list[str]]:
    """Analisa vários CNPJs e cruza o quadro societário entre eles."""
    analises: list[Analise] = []
    erros: list[str] = []
    for cnpj in cnpjs:
        try:
            analises.append(analisar(cnpj, cadastro, sancoes))
        except (ValueError, ErroDeFonte) as erro:
            erros.append(f"{cnpj_formatado(cnpj)}: {erro}")
    return analises, cruzar_vinculos(analises), erros
