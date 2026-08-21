# Site — gestão clínica

Página única, estática, sem build. Posicionamento: **resolutor de problemas de
gestão clínica**. Tudo que falava com outro público (profissional liberal
genérico, escritório contábil, gestão financeira) saiu — está no histórico do
git se precisar.

A régua é venda rápida: **451 palavras, 5 seções, ~3 telas.** Antes eram 2.229
palavras e 11 telas. Toda vez que for acrescentar coisa, pergunte o que sai no
lugar.

## Antes de publicar

Edite **só o bloco `const SITE`** no topo do `index.html`:

```js
const SITE = {
  nome:      "João Félix",
  whatsapp:  "5512991338866",          // só números: 55 + DDD + número
  email:     "jvctrfelix@gmail.com",
  instagram: "",                       // sem o @; vazio não exibe a linha
  cidade:    "São José dos Campos · SP",
  site:      "https://futuro.jvctrfelix.workers.dev"
};
```

Esse mesmo bloco alimenta o convite em PDF — depois de editar, rode
`python3 gerar-convite.py`.

Confira à mão, porque nada disso o código valida:

- [ ] O que ROTA, BASE e PROX fazem bate com o que as apresentações mostram.
- [ ] Os prazos e os 30 dias de ajuste são o que você cumpre.
- [ ] O FAQ sobre LGPD descreve o que você realmente faz.
- [ ] O link `convite.pdf` funciona depois de publicado (é caminho relativo —
      se o Worker não servir o arquivo, quebra).

## Colocar no ar

**Git push não publica o site.** Ele manda o código para o GitHub; quem coloca
no ar é o deploy. Para publicar em `futuro.jvctrfelix.workers.dev`:

```bash
npx wrangler deploy
```

Sobem só `index.html` e `convite.pdf` — o `.assetsignore` deixa de fora código,
fontes e o resto. Como o PDF passa a ser servido no mesmo endereço, o botão
"Baixar a apresentação" funciona sem ajuste.

> **Isto substitui o Worker chamado `futuro` que já está no ar.** Se o atual foi
> publicado de outro jeito (script colado no painel do Cloudflare, outro
> repositório), o conteúdo dele é trocado pelo daqui. Confira antes de rodar.

Para o deploy acontecer sozinho a cada push, é preciso um workflow do GitHub
Actions com um token da API do Cloudflare guardado nos segredos do repositório.
Não está configurado.

## A estrutura, e o porquê

| # | Seção | O que ela faz |
|---|---|---|
| 1 | **Hero** | Diz em uma linha quem é e o que resolve. Um CTA principal, um secundário. |
| 2 | **Toque no que está doendo hoje** | Quatro problemas de clínica, cada card é um link de WhatsApp com a mensagem pronta. A pessoa aciona apontando a dor, sem formular pedido. |
| 3 | **Três sistemas** | ROTA, BASE e PROX em uma frase cada, levando à apresentação aberta. Prova concreta sem parágrafo. |
| 4 | **Como funciona** | Três passos de uma linha, preço em uma frase e três perguntas recolhidas. |
| 5 | **Próximo passo** | Fecha no diagnóstico gratuito, com os contatos. |

Sem menu de navegação: numa página de três telas, âncora é ruído. Só a marca e
o botão de contato ficam fixos no topo.

## Detalhes de implementação

- **Cada link de WhatsApp abre com mensagem própria**, no atributo `data-wa`.
  Você recebe a conversa já sabendo de qual ponto da página a pessoa saiu.
- **Os links de ROTA, BASE e PROX** ficam no HTML da seção `#sistemas` — são
  endereços de sistemas, não dados de contato. Abrem em aba nova.
- Se o JavaScript não carregar, os textos caem no padrão escrito no HTML; só os
  links de contato ficam inertes.

## O convite em PDF

`convite.pdf` — duas páginas A4 para mandar no WhatsApp ou por e-mail.
Página 1: promessa, os dois QR codes (site e WhatsApp) e os três passos.
Página 2: os quatro problemas clicáveis, os três sistemas e o fechamento.

```bash
pip install segno      # só na primeira vez
python3 gerar-convite.py
```

Lê os dados do `index.html`, então não existe segunda lista de contatos para
manter. O texto do convite (problemas, sistemas, passos) fica no topo do
`gerar-convite.py`; o layout, em `convite.template.html`.

> As páginas têm altura fixa e cortam o que sobra. Depois de mexer no texto,
> confira se nada estourou — `.page` tem `overflow:hidden`.

| Arquivo | O que é |
|---|---|
| `gerar-convite.py` | O gerador, e os textos do convite. |
| `convite.template.html` | O layout das duas páginas. |
| `assets/fontes.css` | Fontes em base64, baixadas uma vez. PDF idêntico em qualquer máquina, e regerável sem internet. |
| `convite.pdf` | O que você envia. |
| `convite.html` | Intermediário, sobrescrito a cada execução (fora do git). |

## `analise-fiscal/`

Ferramenta de consulta de CNPJ em fontes públicas, com cruzamento de sócios.
**Não está mais no site** — é produto para escritório contábil, fora do foco de
gestão clínica. O código fica aqui, funcionando e testado, para o dia em que
virar um projeto próprio. Tem README dedicado.

## Próximo passo, em ordem de retorno

1. **Print de tela do ROTA, BASE e PROX** dentro dos cards. A página é toda
   texto, e quem vende software vende a tela.
2. **Um depoimento de uma clínica**, curto, logo abaixo dos sistemas.
3. **Um número concreto** ("reduziu a falta de 30% para 8%").
