# Quadros para gerar a animação do mascote

Os PNGs desta pasta são **para subir num gerador de vídeo a partir de imagem**
(no Dola, a opção de foto → vídeo). Cada um já está em 1080×1920, com o mascote
no fundo escuro do próprio reel (`#0B0C0A`) e um brilho verde de leve — assim o
clipe que voltar encaixa no cenário sem emenda.

O mascote foi recuperado do arquivo original do app (`mascote-poses-original`,
1254×1254), não da versão pequena que o reel usa. Por isso está nítido mesmo
ocupando quase a tela inteira.

| Quadro | Para que serve |
|---|---|
| `mascote-comemora.png` | O fecho: o pulinho de comemoração. É o principal. |
| `mascote-joinha.png` | Uma piscadinha com joinha, se quiser algo mais calmo. |
| `mascote-correndo.png` | Entrada: ele chega correndo e freia de frente. |
| `mascote-moeda.png` | Joga a moeda para cima e pega de volta. |

## O que precisa voltar

- **9:16**, de 4 a 6 segundos
- **sem áudio, sem texto na tela e sem marca d'água**
- **fundo escuro e parado** — se o gerador inventar cenário, o clipe não encaixa
- o personagem **igual ao da imagem**: mesma cor, mesmo traço, mesmas proporções

Gerar duas ou três vezes e escolher a mais estável compensa: modelo de vídeo
costuma deformar desenho de linha, principalmente a cara e os tênis.

Os textos de comando (em inglês, que é o que esses geradores entendem melhor)
estão em `comandos.md`.
