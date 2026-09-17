# Site da Desata

Site da **Desata** — *Tecnologia que descomplica*. Página única, estática, sem
build: HTML, CSS e JavaScript puros. É o que está publicado na raiz deste
repositório e o que vai para o ar no Worker `futuro`.

O repositório também guarda o convite em PDF e a ferramenta de análise fiscal,
descritos mais abaixo.

> O site anterior — página de venda com posicionamento de gestão clínica
> (ROTA, BASE e PROX) — saiu do ar quando o site da Desata assumiu a raiz.
> Ele está no histórico do git: `git log -- index.html`.

## Antes de publicar

Os dados de contato ficam em **`assets/js/config.js`**, e só ali:

```js
window.DESATA_CONFIG = {
  whatsapp: "5512991338866",              // só números: 55 + DDD + número
  email:    "jvctrfelix@gmail.com",
  instagram: "",                          // sem o @; vazio não exibe a linha
  local:    "São José dos Campos · SP"
};
```

Se o WhatsApp ou o e-mail ficarem vazios, a seção de contato mostra um aviso
listando o que falta, em vez de um botão que não abre conversa nenhuma. O
`gerar-convite.py` lê esse mesmo arquivo, então não existe segunda lista de
contatos para manter.

Ainda em aberto:

- **Instagram** — o campo está vazio, então a linha não aparece. Preencher
  quando o perfil existir.
- **Domínio próprio** — hoje o endereço é `futuro.jvctrfelix.workers.dev`. Ao
  trocar, atualize `og:url`, `og:image` e o `<link rel="canonical">` no
  `index.html`.
- **Portfólio** — não existe seção de portfólio. Ela entra quando houver
  projeto real para mostrar; demonstração precisa estar identificada como
  demonstração.

Nada de preço, prazo, cliente, depoimento ou número de projeto foi inventado no
site. O que não está confirmado não está lá.

## Colocar no ar

**Git push não publica o site.** Ele manda o código para o GitHub; quem coloca
no ar é o deploy:

```bash
npx wrangler deploy
```

Sobem o `index.html`, a pasta `assets/` e o `convite.pdf` — o `.assetsignore`
deixa de fora código, originais da marca e o resto.

> **Isto substitui o conteúdo do Worker `futuro`, que já está no ar.** Confira
> antes de rodar.

Deploy automático a cada push exigiria um workflow do GitHub Actions com um
token da API do Cloudflare nos segredos do repositório. Não está configurado.

Para ver localmente:

```bash
python3 -m http.server 8000     # abre http://localhost:8000
```

## A estrutura do site

| # | Seção | O que ela faz |
|---|---|---|
| 1 | **Abertura** | "Seu negócio pode fluir melhor" + o que a Desata faz, em duas linhas, e o botão de conversa. |
| 2 | **O que trava o dia** | Seis situações concretas do cotidiano de quem empreende. A pessoa se reconhece antes de ouvir a oferta. |
| 3 | **Serviços** | Criação de sites em destaque; sistemas web e automações em seguida. Diz também o que a Desata ainda não vende. |
| 4 | **Como funciona** | Entender, definir escopo, desenvolver, validar, entregar. Suporte posterior é definido na proposta. |
| 5 | **A Desata** | A ideia de desatar nós e quem está por trás. |
| 6 | **Dúvidas** | Sete perguntas sobre contratação: preço, prazo, domínio, textos, alterações. |
| 7 | **Contato** | Fecha no WhatsApp, com a mensagem já escrita. |

### Onde mexer em cada coisa

| O que | Onde |
|---|---|
| Textos, seções, dúvidas | `index.html` |
| Cores e tipografia | bloco `:root`, no topo de `assets/css/estilo.css` |
| Contatos | `assets/js/config.js` |
| Menu, animações, links de contato | `assets/js/main.js` |
| Originais da identidade visual | `marca/` (não vai para o ar) |

### Cores da marca

| Cor | Código | Uso |
|---|---|---|
| Off-white | `#F4F0E8` | fundo principal |
| Grafite | `#242424` | texto e seções de contraste |
| Laranja queimado | `#E66A35` | destaques, botões e os laços gráficos |

Laranja com texto **grafite** dá contraste 4,8:1 (WCAG AA). Laranja com texto
**branco** só passa em tamanho grande, por isso branco sobre laranja aparece só
em títulos. Para texto pequeno em laranja sobre o off-white, o site usa o tom
mais escuro `#A34517`.

### Detalhes de implementação

- Fonte Figtree servida pelo próprio site (~30 KB em `assets/fonts/`): nenhuma
  requisição a terceiros, em nenhum lugar da página.
- Sem JavaScript a página continua inteira e navegável — só os links de contato
  ficam inertes. As dúvidas são `<details>`, funcionam sem script.
- Menu mobile com `aria-expanded`, fechamento por `Esc` e por clique fora.
- Animações discretas, todas desligadas com `prefers-reduced-motion`.
- Não há formulário. Se um dia entrar, precisa de destino de envio real e
  mensagem de sucesso e de erro de verdade — nada de simular envio concluído.

## O convite em PDF

`convite.pdf` — duas páginas A4 para mandar no WhatsApp ou por e-mail. O texto
é o da apresentação de gestão clínica, anterior ao site da Desata.

```bash
pip install segno      # só na primeira vez
python3 gerar-convite.py
```

Lê os contatos de `assets/js/config.js`; nome e endereço do site ficam em
`PADRAO`, no topo do script. O texto do convite fica no próprio
`gerar-convite.py`; o layout, em `convite.template.html`.

> As páginas têm altura fixa e cortam o que sobra. Depois de mexer no texto,
> confira se nada estourou — `.page` tem `overflow:hidden`.

| Arquivo | O que é |
|---|---|
| `gerar-convite.py` | O gerador, e os textos do convite. |
| `convite.template.html` | O layout das duas páginas. |
| `assets/fontes.css` | Fontes em base64 do convite, baixadas uma vez. PDF idêntico em qualquer máquina, regerável sem internet. Não confunda com `assets/css/fontes.css`, que é a fonte do site. |
| `convite.pdf` | O que você envia. Continua servido em `/convite.pdf`. |
| `convite.html` | Intermediário, sobrescrito a cada execução (fora do git). |

## `analise-fiscal/`

Ferramenta de consulta de CNPJ em fontes públicas, com cruzamento de sócios.
Não está no site. O código fica aqui, funcionando e testado, para o dia em que
virar um projeto próprio. Tem README dedicado.
