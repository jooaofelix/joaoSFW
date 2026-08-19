# Análise cadastral e fiscal — nível 1

Consulta um ou vários CNPJs em **fontes públicas**, consolida numa análise com
achados classificados por gravidade, e cruza o quadro societário para achar
**sócios em comum entre as empresas**.

Sem dependência externa: só a biblioteca padrão do Python.

```bash
python3 exemplo.py                       # vê a saída com dados de exemplo
python3 exemplo.py --html                # gera exemplo.html

python3 -m analise_fiscal 11222333000181
python3 -m analise_fiscal 11222333000181 44555666000181 --html carteira.html
python3 -m analise_fiscal --arquivo clientes.txt --json carteira.json
```

## O que ele responde

| Pergunta | Fonte |
|---|---|
| A empresa está ativa? Desde quando, e por que não? | Cadastro público do CNPJ |
| É optante do Simples? Do MEI? Desde quando? | Cadastro público do CNPJ |
| Foi excluída do Simples? Quando? | Cadastro público do CNPJ |
| Qual a atividade principal e as secundárias? | Cadastro público do CNPJ |
| Quem são os sócios, e desde quando? | Quadro societário público |
| **Quais clientes meus têm sócio em comum?** | Cruzamento local |
| Tem sanção vigente (CEIS/CNEP)? | Portal da Transparência |

O valor não está em buscar o dado — está em transformar em conclusão. Cada
achado sai com nível (`alerta`, `atencao`, `info`) e a lista vem ordenada por
gravidade, então quem abre o relatório vê o problema primeiro.

Regras implementadas hoje: situação cadastral diferente de ativa, exclusão do
Simples, incoerência entre porte e enquadramento, capital social zerado, empresa
recém-aberta, ausência de quadro societário, sanção vigente e sanção encerrada.

## Vínculos societários

Passando mais de um CNPJ, o relatório ganha um bloco extra com as pessoas que
aparecem em mais de uma empresa, e a qualificação em cada uma.

Para um escritório contábil isso responde de graça uma pergunta que hoje
ninguém consegue responder: *quais dos meus clientes são do mesmo grupo?* —
o que muda planejamento tributário, risco e até cobrança.

> **Leia com cuidado:** o CPF do sócio vem mascarado na base pública (só os seis
> dígitos do meio). O cruzamento usa nome + máscara, então homônimo com a mesma
> máscara é raro mas possível. É indício a conferir, não prova.

## Configuração

| Variável | Para quê |
|---|---|
| `--base-cadastro` | Endpoint do espelho da base do CNPJ. Padrão: BrasilAPI. |
| `--chave-transparencia` / `CHAVE_TRANSPARENCIA` | Chave gratuita do Portal da Transparência. **Sem ela as sanções não são consultadas** — e o relatório diz isso, em vez de dar um "nada consta" falso. |

## Antes de usar em produção

- [ ] **Confira os nomes dos campos** contra uma resposta real da fonte que você
      escolher. O normalizador aceita vários apelidos para o mesmo campo
      (`data_inicio_atividade` / `data_abertura`, `qsa` / `socios`, …) porque as
      fontes divergem, mas não dá para prever todas.
- [ ] **Preencha `CNAES_VEDADOS_SIMPLES`** em `analise_fiscal/analise.py` com a
      relação que o seu escritório usa. Enquanto estiver vazia, a análise diz
      explicitamente que não verificou a vedação — nunca um "ok" falso.
- [ ] **Decida a fonte para volume.** Consulta ao vivo serve para dezenas de
      CNPJs. Para centenas, carregue o dump mensal dos Dados Abertos da Receita
      num banco seu e consulte local: some captcha, rate limit e dependência de
      terceiro, e fica muito mais rápido.

## Limites honestos

Isto é **nível 1: só dado público**. Não consulta e-CAC, não vê débito, não vê
parcelamento, não emite certidão. Para isso é preciso procuração eletrônica e a
API oficial do Serpro (Integra Contador) — outro projeto, com contrato e
guarda de certificado digital.

## Testes

```bash
python3 -m unittest discover -s tests -v
```

25 testes, todos offline: o HTTP é substituído por um dublê que devolve
fixtures. A suíte não quebra quando uma API de terceiro sai do ar, e as regras
de análise podem ser testadas sem rede.
