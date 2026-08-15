# Site de apresentação — sistemas sob medida

Página única, estática. Sem build, sem dependência. É só abrir o `index.html` no
navegador ou subir o arquivo em qualquer hospedagem (GitHub Pages, Netlify,
Vercel, ou um servidor comum).

## Antes de publicar

Edite **só o bloco `const SITE`** no topo do `index.html`. Ele preenche nome,
WhatsApp, e-mail, Instagram, cidade e preços na página inteira:

```js
const SITE = {
  nome:      "João Félix",
  whatsapp:  "5512991338866",          // só números: 55 + DDD + número
  email:     "jvctrfelix@gmail.com",
  instagram: "",                       // sem o @; vazio não exibe a linha
  cidade:    "São José dos Campos · SP",
  site:      "https://futuro.jvctrfelix.workers.dev",
  precos: { 1: "", 2: "", 3: "" }      // vazio = não exibe valor (recomendado)
};
```

Esse mesmo bloco alimenta o convite em PDF — depois de editar, rode
`python3 gerar-convite.py` para o PDF sair com os dados novos.

Confira à mão, porque nada disso o código valida:

- [ ] **As funções listadas em ROTA, BASE e PROX existem mesmo.** A lista foi
      montada a partir do que a própria página já afirmava nas áreas e nos
      casos — se algum item ainda não está construído, tire, porque é a
      primeira coisa que o cliente vai pedir para ver na demonstração.
- [ ] Os três casos descrevem trabalhos que você entregou mesmo. Se algum for
      hipotético, troque ou tire — o resto da página perde força se um for
      descoberto como inventado.
- [ ] Os prazos citados (1–2 semanas, 4–8 semanas, 30 dias de ajuste) são os
      que você consegue cumprir.
- [ ] O FAQ sobre LGPD e dados descreve o que você realmente faz, e o backup
      diário prometido na assinatura acontece de verdade.

## A estrutura da página, e o porquê de cada bloco

A ordem é um funil: cada seção responde à pergunta que a anterior levanta.

| # | Seção | O que ela resolve |
|---|---|---|
| 1 | **Hero** | Diz em uma frase para quem é e o que muda. Dois botões: um para quem já decidiu, outro para quem quer prova. |
| 2 | **Se algum desses for você** | O visitante precisa se reconhecer antes de te ouvir. Quatro sinais concretos, não adjetivos. |
| 3 | **Onde eu costumo entrar** | Seis áreas (financeiro, agenda, documentos, mensagens, acompanhamento, equipe). Cada um dos 24 itens é um link de WhatsApp com a mensagem pronta — a pessoa aciona apontando a dor, sem precisar formular o pedido. |
| 4 | **Sistemas prontos** | ROTA, BASE e PROX como bases já construídas, cada um levando à sua apresentação aberta. Corta a objeção de prazo e preço sem contradizer o "sob medida": a base é ponto de partida, o que muda é feito, não configurado. |
| 5 | **Casos** | Prova. Cada card termina no resultado, não na funcionalidade. |
| 6 | **Como funciona + comparativo** | Tira o medo do processo e responde "por que não um pronto?" no mesmo bloco. |
| 7 | **Faixa de CTA** | Ponto de saída no meio da página, para quem já se convenceu e não vai rolar até o fim. |
| 8 | **Investimento** | Qualifica o lead detalhando o que entra em cada escopo, e explica a lógica do preço em vez de exibir "sob consulta" num slot vazio. Cada card sai direto para a conversa. Se você preencher `precos`, o valor aparece; vazio, o slot nem existe. |
| 9 | **FAQ** | As seis objeções que aparecem na conversa. Respondidas aqui, a reunião começa mais adiante. |
| 10 | **Indicação + contato** | Fecha pedindo o compartilhamento, que é de onde vem boa parte do trabalho. |

## Detalhes de implementação

- **Botões de WhatsApp** já abrem com mensagem escrita, diferente por
  contexto — dá para saber de qual ponto da página a pessoa saiu, e a primeira
  mensagem já chega dizendo qual é o problema. A frase fica no atributo
  `data-wa` de cada link; para editar um item da seção de áreas, mude o texto
  visível e o `data-wa` junto.
- **"Baixar o convite em PDF"** aponta para `convite.pdf` em caminho relativo.
  Se a hospedagem não servir esse arquivo, o link quebra — confira depois de
  publicar. A página também tem um `@media print` que esconde menu e botões,
  caso você prefira imprimir o site direto.
- **Menu fixo** com âncoras para as cinco seções principais. Some no celular
  para não competir com o botão de contato.
- **Os links de ROTA, BASE e PROX** ficam no HTML da seção `#sistemas`, não no
  `const SITE` — são endereços de sistemas diferentes, não dados de contato.
  Abrem em aba nova para não tirar a pessoa da página.
- Se o JavaScript não carregar, os textos caem no valor padrão escrito no HTML
  e a página continua legível — só os links de contato ficam inertes.

## O convite em PDF

`convite.pdf` é a versão para enviar no WhatsApp ou por e-mail: três páginas A4
com **duas saídas em toda página** — o site (para ver com calma) e o WhatsApp
(para falar agora). Links de PDF são clicáveis, então os 24 itens da página 2
abrem a conversa com a mensagem já escrita, igual ao site. E há QR code na capa
e no fechamento, para funcionar também impresso ou mostrado numa tela.

Para regerar depois de mexer no `const SITE`:

```bash
pip install segno      # só na primeira vez
python3 gerar-convite.py
```

O script lê os dados direto do `index.html`, então **não existe uma segunda
lista de contatos para manter em dia** — muda num lugar, sai nos dois.

| Arquivo | O que é |
|---|---|
| `gerar-convite.py` | O gerador. Aqui ficam os textos das seis áreas. |
| `convite.template.html` | O layout das três páginas. |
| `assets/fontes.css` | Fontes embutidas em base64, baixadas uma vez. Deixa o PDF idêntico em qualquer máquina e permite regerar sem internet. |
| `convite.pdf` | O que você envia. |
| `convite.html` | Intermediário, sobrescrito a cada execução (fora do git). |

Se o Chrome não for encontrado, o script avisa e você ainda pode abrir o
`convite.html` no navegador e imprimir em PDF na mão.

## Sugestões de próximo passo

Em ordem de retorno, se quiser evoluir:

1. **Print de tela do ROTA, do BASE e do PROX.** Cada card já leva à
   apresentação do sistema, mas o clique é um pedágio: uma imagem no próprio
   card faz a pessoa querer clicar. Quem vende software vende a tela.
2. **Um depoimento real**, mesmo que curto, logo abaixo dos casos.
3. **Um número concreto** em pelo menos um caso ("reduziu o fechamento de 6h
   para 20min").
4. **Levar ROTA, BASE e PROX para o convite em PDF**, provavelmente como uma
   quarta página. Hoje o convite não menciona que existem sistemas prontos.
