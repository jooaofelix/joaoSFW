"""Testes offline: nenhuma chamada de rede real.

O HTTP é substituído por um dublê que devolve fixtures, então dá para rodar
em qualquer lugar e a suíte não quebra quando uma API de terceiro cai.
"""

import json
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analise_fiscal.analise import (analisar, analisar_carteira,  # noqa: E402
                                    cruzar_vinculos)
from analise_fiscal.fontes import (ErroDeFonte, FonteCadastro,  # noqa: E402
                                   FonteSancoes, normalizar_empresa)
from analise_fiscal.modelo import cnpj_formatado, cnpj_valido  # noqa: E402
from analise_fiscal.relatorio import pagina, texto, texto_vinculos  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"

ATIVA = "11222333000181"
BAIXADA = "44555666000181"
MEI = "77888999000181"


def carregar(nome: str) -> dict:
    return json.loads((FIXTURES / nome).read_text(encoding="utf-8"))


class HttpFalso:
    """Devolve a fixture correspondente ao CNPJ pedido."""

    def __init__(self, mapa: dict[str, object], sancoes: object = None):
        self.mapa = mapa
        self.sancoes = sancoes if sancoes is not None else []
        self.chamadas: list[str] = []

    def __call__(self, url, cabecalhos=None):
        self.chamadas.append(url)
        if "portaldatransparencia" in url:
            if isinstance(self.sancoes, Exception):
                raise self.sancoes
            return self.sancoes
        for cnpj, dados in self.mapa.items():
            if cnpj in url:
                if isinstance(dados, Exception):
                    raise dados
                return dados
        raise ErroDeFonte("não encontrado")


def cadastro_padrao(**extra):
    mapa = {
        ATIVA: carregar("cadastro_ativa_simples.json"),
        BAIXADA: carregar("cadastro_baixada.json"),
        MEI: carregar("cadastro_mei_campos_alternativos.json"),
    }
    mapa.update(extra)
    http = HttpFalso(mapa)
    return FonteCadastro(http), http


# --------------------------------------------------------------------------
class TestCnpj(unittest.TestCase):
    def test_valida_digitos(self):
        self.assertTrue(cnpj_valido(ATIVA))
        self.assertTrue(cnpj_valido("00.000.000/0001-91"))

    def test_rejeita_invalidos(self):
        for ruim in ["11111111111111", "1122233300018", "", "abc", "11222333000180"]:
            self.assertFalse(cnpj_valido(ruim), ruim)

    def test_formata(self):
        self.assertEqual(cnpj_formatado(ATIVA), "11.222.333/0001-81")


class TestNormalizacao(unittest.TestCase):
    def test_campos_principais(self):
        e = normalizar_empresa(carregar("cadastro_ativa_simples.json"))
        self.assertEqual(e.razao_social, "CLINICA EXEMPLO LTDA")
        self.assertEqual(e.situacao, "ATIVA")
        self.assertTrue(e.ativa)
        self.assertEqual(e.data_abertura, date(2019, 3, 12))
        self.assertEqual(e.capital_social, 50000.0)
        self.assertEqual(e.cnae_principal.codigo, "8630501")
        self.assertEqual(len(e.cnaes_secundarios), 1)
        self.assertEqual(len(e.socios), 2)
        self.assertTrue(e.simples.optante)

    def test_aceita_nomes_alternativos_de_campo(self):
        """Fontes diferentes nomeiam o mesmo campo de jeitos diferentes."""
        e = normalizar_empresa(carregar("cadastro_mei_campos_alternativos.json"))
        self.assertEqual(e.razao_social, "JOSE DA SILVA 12345678900")
        self.assertEqual(e.nome_fantasia, "Contabil Silva")
        self.assertEqual(e.data_abertura, date(2024, 7, 24))   # dd/mm/aaaa
        self.assertEqual(e.capital_social, 1000.0)             # "1.000,00"
        self.assertEqual(e.municipio, "JACAREI")
        self.assertTrue(e.simples.optante)                     # "S"
        self.assertTrue(e.mei.optante)

    def test_campos_ausentes_nao_quebram(self):
        e = normalizar_empresa({})
        self.assertEqual(e.razao_social, "")
        self.assertIsNone(e.capital_social)
        self.assertIsNone(e.simples.optante)
        self.assertEqual(e.socios, [])


class TestRegras(unittest.TestCase):
    def codigos(self, analise):
        return {a.codigo for a in analise.achados}

    def test_empresa_ativa_no_simples(self):
        cadastro, _ = cadastro_padrao()
        a = analisar(ATIVA, cadastro)
        self.assertIn("situacao_ativa", self.codigos(a))
        self.assertIn("simples_optante", self.codigos(a))
        self.assertEqual(a.pior_nivel, "info")

    def test_baixada_vira_alerta(self):
        cadastro, _ = cadastro_padrao()
        a = analisar(BAIXADA, cadastro)
        self.assertIn("situacao_baixada", self.codigos(a))
        self.assertEqual(a.pior_nivel, "alerta")

    def test_exclusao_do_simples_e_capital_zero(self):
        cadastro, _ = cadastro_padrao()
        a = analisar(BAIXADA, cadastro)
        self.assertIn("simples_excluido", self.codigos(a))
        self.assertIn("capital_zerado", self.codigos(a))
        self.assertIn("porte_incoerente", self.codigos(a))

    def test_achados_ordenados_por_gravidade(self):
        cadastro, _ = cadastro_padrao()
        a = analisar(BAIXADA, cadastro)
        pesos = [x.peso for x in a.achados]
        self.assertEqual(pesos, sorted(pesos, reverse=True))

    def test_vedacao_de_cnae_diz_que_nao_verificou(self):
        """Sem lista carregada, a análise não pode dar um 'ok' falso."""
        cadastro, _ = cadastro_padrao()
        a = analisar(ATIVA, cadastro)
        self.assertIn("vedacao_nao_verificada", self.codigos(a))

    def test_cnpj_invalido_nao_chega_na_rede(self):
        cadastro, http = cadastro_padrao()
        with self.assertRaises(ValueError):
            analisar("11111111111111", cadastro)
        self.assertEqual(http.chamadas, [])


class TestSancoes(unittest.TestCase):
    def test_sem_chave_registra_falha_sem_derrubar(self):
        cadastro, http = cadastro_padrao()
        a = analisar(ATIVA, cadastro, FonteSancoes(http, chave=None))
        self.assertEqual(a.sancoes, [])
        self.assertTrue(any("sem chave" in f for f in a.falhas))
        self.assertIn("situacao_ativa", {x.codigo for x in a.achados})

    def test_sancao_vigente_vira_alerta(self):
        http = HttpFalso(
            {ATIVA: carregar("cadastro_ativa_simples.json")},
            sancoes=[{"tipoSancao": "Inidoneidade", "orgaoSancionador": "CGU",
                      "dataInicioSancao": "2024-01-01", "dataFimSancao": "2099-01-01",
                      "textoPublicacao": "..."}])
        a = analisar(ATIVA, FonteCadastro(http), FonteSancoes(http, chave="x"))
        self.assertTrue(any(s.vigente for s in a.sancoes))
        self.assertIn("sancao_vigente", {x.codigo for x in a.achados})
        self.assertEqual(a.pior_nivel, "alerta")

    def test_sancao_encerrada_e_so_atencao(self):
        http = HttpFalso(
            {ATIVA: carregar("cadastro_ativa_simples.json")},
            sancoes=[{"tipoSancao": "Multa", "dataInicioSancao": "2015-01-01",
                      "dataFimSancao": "2016-01-01"}])
        a = analisar(ATIVA, FonteCadastro(http), FonteSancoes(http, chave="x"))
        self.assertIn("sancao_encerrada", {x.codigo for x in a.achados})
        self.assertNotIn("sancao_vigente", {x.codigo for x in a.achados})

    def test_falha_da_fonte_nao_derruba_analise(self):
        http = HttpFalso({ATIVA: carregar("cadastro_ativa_simples.json")},
                         sancoes=ErroDeFonte("limite de consultas excedido"))
        a = analisar(ATIVA, FonteCadastro(http), FonteSancoes(http, chave="x"))
        self.assertTrue(a.achados)
        self.assertTrue(any("limite" in f for f in a.falhas))


class TestVinculos(unittest.TestCase):
    def test_encontra_socio_em_comum(self):
        cadastro, _ = cadastro_padrao()
        analises, vinculos, erros = analisar_carteira([ATIVA, BAIXADA], cadastro)
        self.assertEqual(erros, [])
        self.assertEqual(len(vinculos), 1)
        self.assertEqual(vinculos[0].socio, "MARIA SOUZA")
        self.assertCountEqual(vinculos[0].empresas, [ATIVA, BAIXADA])

    def test_socio_de_uma_empresa_so_nao_vira_vinculo(self):
        cadastro, _ = cadastro_padrao()
        analises, vinculos, _ = analisar_carteira([ATIVA], cadastro)
        self.assertEqual(vinculos, [])

    def test_ordena_por_quantidade_de_empresas(self):
        base = carregar("cadastro_ativa_simples.json")
        terceira = dict(base, cnpj=MEI, razao_social="TERCEIRA LTDA",
                        qsa=[base["qsa"][0]])
        cadastro, _ = cadastro_padrao(**{MEI: terceira})
        _, vinculos, _ = analisar_carteira([ATIVA, BAIXADA, MEI], cadastro)
        self.assertEqual(vinculos[0].socio, "MARIA SOUZA")
        self.assertEqual(len(vinculos[0].empresas), 3)

    def test_cnpj_invalido_no_meio_da_carteira_nao_para_o_resto(self):
        cadastro, _ = cadastro_padrao()
        analises, _, erros = analisar_carteira([ATIVA, "11111111111111"], cadastro)
        self.assertEqual(len(analises), 1)
        self.assertEqual(len(erros), 1)

    def test_cruzar_lista_vazia(self):
        self.assertEqual(cruzar_vinculos([]), [])


class TestRelatorio(unittest.TestCase):
    def test_texto_traz_dados_e_analise(self):
        cadastro, _ = cadastro_padrao()
        saida = texto(analisar(ATIVA, cadastro), cores=False)
        self.assertIn("CLINICA EXEMPLO LTDA", saida)
        self.assertIn("11.222.333/0001-81", saida)
        self.assertIn("MARIA SOUZA", saida)

    def test_html_e_bem_formado_e_escapa(self):
        http = HttpFalso({ATIVA: dict(carregar("cadastro_ativa_simples.json"),
                                      razao_social="A & B <script>x</script>")})
        a = analisar(ATIVA, FonteCadastro(http))
        html = pagina([a])
        self.assertIn("<!DOCTYPE html>", html)
        self.assertEqual(html.count("<html"), 1)
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn("<script>x</script>", html)

    def test_texto_vinculos_sem_vinculo(self):
        self.assertIn("Nenhum sócio em comum", texto_vinculos([]))

    def test_json_serializavel(self):
        cadastro, _ = cadastro_padrao()
        d = analisar(ATIVA, cadastro).como_dict()
        json.dumps(d, ensure_ascii=False)          # não pode levantar
        self.assertEqual(d["empresa"]["data_abertura"], "2019-03-12")


if __name__ == "__main__":
    unittest.main(verbosity=2)
