# Demonstração — loja de roupas (148)

Vídeo de 42 segundos, vertical, sem narração, para mandar no WhatsApp a quem
está avaliando um site de venda de roupas. Tudo é **demonstração**: as peças,
os preços e a loja não existem.

```bash
node demos/loja-roupas/gravar.js     # regera 148-demonstracao.mp4
```

| Arquivo | O que é |
|---|---|
| `148-demonstracao.mp4` | O vídeo pronto (1080×1920, H.264, sem áudio). |
| `loja.html` | A loja de demonstração: vitrine, filtro por tamanho, página da peça, sacola e pedido no WhatsApp. Roda sozinha no navegador. |
| `palco.html` | A cena do vídeo: abertura, celular, legendas e fecho, na identidade da Desata. |
| `roteiro.js` | O tempo de cada passo. É aqui que se muda o ritmo ou o texto das legendas. |
| `gravar.js` | Abre o palco num servidor local, filma e converte para MP4. Precisa de `playwright` e `ffmpeg`. |

Não há foto de produto: as peças são desenhos em SVG, feitos no próprio
código. Trocar por fotos reais é mexer em `loja.html`.

Os contatos do fecho saem de `assets/js/config.js`, como no resto do
repositório.
