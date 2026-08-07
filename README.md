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
  whatsapp:  "5512999999999",          // só números: 55 + DDD + número
  email:     "contato@exemplo.com.br",
  instagram: "joaofelix",              // sem o @
  cidade:    "São José dos Campos · SP",
  site:      "https://...",            // endereço público da página
  precos: { 1: "", 2: "", 3: "" }      // vazio = mostra "sob consulta"
};
```

Esse mesmo bloco alimenta o convite em PDF — depois de editar, rode
`python3 gerar-convite.py` para o PDF sair com os dados novos.

Depois disso, confira à mão:

- [ ] `email`, `instagram` e `site` ainda estão com valor de exemplo.
      O `site` precisa do endereço real assim que a página estiver publicada,
      senão o QR code do convite não leva a lugar nenhum.

- [ ] Os três casos da seção **Casos** descrevem trabalhos que você entregou
      mesmo. Se algum for hipotético, troque ou tire — o resto da página perde
      força se um for descoberto como inventado.
- [ ] Os prazos citados (1–2 semanas, 4–8 semanas, 30 dias de ajuste) são os
      que você consegue cumprir.
- [ ] O FAQ sobre LGPD e dados descreve o que você realmente faz.

## A estrutura da página, e o porquê de cada bloco

A ordem é um funil: cada seção responde à pergunta que a anterior levanta.

| # | Seção | O que ela resolve |
|---|---|---|
| 1 | **Hero** | Diz em uma frase para quem é e o que muda. Dois botões: um para quem já decidiu, outro para quem quer prova. |
| 2 | **Se algum desses for você** | O visitante precisa se reconhecer antes de te ouvir. Quatro sinais concretos, não adjetivos. |
| 3 | **Onde eu costumo entrar** | Seis áreas (financeiro, agenda, documentos, mensagens, acompanhamento, equipe). Cada um dos 24 itens é um link de WhatsApp com a mensagem pronta — a pessoa aciona apontando a dor, sem precisar formular o pedido. |
| 4 | **Casos** | Prova. Cada card termina no resultado, não na funcionalidade. |
| 5 | **Como funciona + comparativo** | Tira o medo do processo e responde "por que não um pronto?" no mesmo bloco. |
| 6 | **Faixa de CTA** | Ponto de saída no meio da página, para quem já se convenceu e não vai rolar até o fim. |
| 7 | **Investimento** | Qualifica o lead. Três escopos, sem obrigar a mostrar número — mas mostrando a lógica do preço. |
| 8 | **FAQ** | As seis objeções que aparecem na conversa. Respondidas aqui, a reunião começa mais adiante. |
| 9 | **Indicação + contato** | Fecha pedindo o compartilhamento, que é de onde vem boa parte do trabalho. |

## Detalhes de implementação

- **Botões de WhatsApp** já abrem com mensagem escrita, diferente por
  contexto — dá para saber de qual ponto da página a pessoa saiu, e a primeira
  mensagem já chega dizendo qual é o problema. A frase fica no atributo
  `data-wa` de cada link; para editar um item da seção de áreas, mude o texto
  visível e o `data-wa` junto.
- **"Salvar em PDF"** usa a impressão do próprio navegador, com um
  `@media print` que esconde menu e botões e clareia os blocos escuros.
  Não precisa manter um PDF separado atualizado.
- **Menu fixo** com âncoras para as quatro seções principais. Some no celular
  para não competir com o botão de contato.
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

1. **Um depoimento real**, mesmo que curto, logo abaixo dos casos. É o que mais
   move a agulha e é a única coisa que a página não tem hoje.
2. **Um número concreto** em pelo menos um caso ("reduziu o fechamento de 6h
   para 20min").
3. **Print ou GIF de tela** de um dos sistemas. A página hoje é toda texto;
   quem vende software ganha muito com uma imagem do produto.
