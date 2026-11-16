# Demonstrações

Vídeos curtos, verticais e sem narração, para mandar no WhatsApp a quem está
avaliando um site. Todos trazem a identidade da Desata na abertura, nas
legendas e no fecho — e deixam claro que são **demonstração**.

```bash
npm i playwright                                      # uma vez
node demos/gravar.js landing-roupas landing-demonstracao
node demos/gravar.js loja-roupas    148-demonstracao
```

O `gravar.js` serve o repositório num servidor local, abre o palco da pasta
indicada, filma a tela e converte para MP4 (1080×1920, H.264, sem áudio).
Precisa do `ffmpeg` no PATH.

Para assinar um vídeo que já existe — um vídeo de cliente, por exemplo:

```bash
node demos/assinar.js video.mp4                      # salva video-assinado.mp4
node demos/assinar.js video.mp4 saida.mp4 --seg 4    # fecho mais curto
node demos/assinar.js video.mp4 saida.mp4 --arroba   # mostra o @ no lugar do site
```

O fecho é gravado na resolução e na taxa de quadros do próprio vídeo, entra
com meio segundo de passagem cruzada, e o áudio do original é preservado (o
fecho recebe uma trilha de silêncio, senão a junção derruba o som).

| Pasta | O que mostra |
|---|---|
| `landing-roupas/` | **Landing page de funil** para marca de roupas: do link do perfil até o pedido escrito no WhatsApp. É o formato de venda mais simples — uma página, um destino. |
| `loja-roupas/` | Loja com vitrine, filtro por tamanho, sacola e pedido no WhatsApp. Um passo além da landing page. |
| `pagaai/` | **Reel do pagaAí**: plano-sequência de ~34s, sem narração, na identidade do próprio app. Mistura motion com três clipes filmados. |

Peças iguais em todos os vídeos:

| Arquivo | O que é |
|---|---|
| `palco.css` | A cena: abertura, celular, legendas e fecho, na identidade da Desata. |
| `assinar.js` | Cola a assinatura da Desata no fim de **qualquer** vídeo, inclusive de cliente. |
| `fecho/fecho.html` | A assinatura em si: laço, logo, frase e contatos. |
| `gravar.js` | Grava e converte. Recebe a pasta do demo como argumento. |
| `<pasta>/palco.html` | A cena daquele vídeo (textos da abertura e qual página entra no celular). |
| `<pasta>/roteiro.js` | O tempo de cada passo e o texto das legendas. É aqui que se muda o ritmo. |
| `<pasta>/clipes/` | Os clipes filmados que entram na cena, já em H.264 e no tamanho certo. |
| `pagaai/para-gerar/` | Quadros do mascote prontos para subir num gerador de vídeo, com os comandos. |

## O reel do pagaAí é um plano-sequência

Os outros vídeos são uma sequência de passos. O do pagaAí é um movimento só:
existe um cenário de 2000×9200 e uma câmera que desce por ele, interpolando as
marcas de `CAMERA` no `roteiro.js`. Em cada marca a câmera enxerga `1080/z` por
`1920/z` do cenário — é essa conta que diz se alguma coisa entra cortada.

Os clipes filmados ficam **dentro** do cenário, como janelas que a câmera
atravessa. Cada janela tem a borda dissolvida por uma vinheta, então não
aparece um retângulo: o filme flutua no escuro e a passagem para a parte
gráfica é movimento, não corte. Quem já cumpriu o papel sai de cena pelo
`data-ate`, em vez de ficar pendurado no canto dos planos abertos.

O mascote do fecho é um ciclo de corrida gerado a partir do desenho do app,
mas só os quinze primeiros quadros entram: dali em diante o gerador troca a
cara do personagem e transforma os cartões numa cédula com rosto impresso.
Quinze quadros é exatamente um ciclo de passada, então o trecho limpo roda em
laço e o defeito nunca aparece.

Esse clipe não leva a vinheta das outras janelas: o fundo dele foi igualado ao
preto da cena dentro do próprio arquivo — primeiro esmagando o brilho que
sobrou do quadro enviado, depois levantando o preto de volta para `#0B0C0A`.
Por isso `.janela--mascote` também não recebe o ajuste de brilho das outras:
mexer nele reabriria o retângulo.

Para trocar um clipe, basta pôr outro arquivo em `clipes/` com o mesmo nome. O
formato que encaixa é **1080×1768, H.264, 30 fps, sem áudio e sem marca
d'água** — o enquadramento dentro da janela é `object-fit: cover`, então o
assunto precisa estar no centro.

Nenhuma marca real é usada: as lojas, as peças e os preços são fictícios, e
não há foto de estoque — as roupas são desenhos em SVG feitos no código.

As pessoas que aparecem no reel do pagaAí são geradas por IA, não são clientes
e não são depoimento: é ilustração, e o rodapé do vídeo diz **demonstração ·
valores ilustrativos**. Os valores da tela do app também são inventados.

Os contatos do fecho saem de `assets/js/config.js`, como no resto do repositório.
