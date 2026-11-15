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
| `pagaai/` | **Reel do pagaAí**: comercial de 35s em motion, sem narração, na identidade do próprio app. |

Peças iguais em todos os vídeos:

| Arquivo | O que é |
|---|---|
| `palco.css` | A cena: abertura, celular, legendas e fecho, na identidade da Desata. |
| `assinar.js` | Cola a assinatura da Desata no fim de **qualquer** vídeo, inclusive de cliente. |
| `fecho/fecho.html` | A assinatura em si: laço, logo, frase e contatos. |
| `gravar.js` | Grava e converte. Recebe a pasta do demo como argumento. |
| `<pasta>/palco.html` | A cena daquele vídeo (textos da abertura e qual página entra no celular). |
| `<pasta>/roteiro.js` | O tempo de cada passo e o texto das legendas. É aqui que se muda o ritmo. |

Nenhuma marca real é usada: as lojas, as peças e os preços são fictícios, e
não há foto de estoque — as roupas são desenhos em SVG feitos no código.

Os contatos do fecho saem de `assets/js/config.js`, como no resto do repositório.
