# Demonstração — loja de roupas (148)

Vídeo de 42 segundos, vertical, sem narração, para mandar no WhatsApp a quem
está avaliando um site de venda de roupas. Tudo é **demonstração**: as peças,
os preços e a loja não existem.

```bash
node demos/gravar.js loja-roupas 148-demonstracao
```

| Arquivo | O que é |
|---|---|
| `148-demonstracao.mp4` | O vídeo pronto (1080×1920, H.264, sem áudio). |
| `loja.html` | A loja de demonstração: vitrine, filtro por tamanho, página da peça, sacola e pedido no WhatsApp. Roda sozinha no navegador. |
| `palco.html` | A cena do vídeo. O visual dela fica em `../palco.css`, e o gravador em `../gravar.js`. |
| `roteiro.js` | O tempo de cada passo. É aqui que se muda o ritmo ou o texto das legendas. |

Não há foto de produto: as peças são desenhos em SVG, feitos no próprio
código. Trocar por fotos reais é mexer em `loja.html`.

Os contatos do fecho saem de `assets/js/config.js`, como no resto do
repositório.
