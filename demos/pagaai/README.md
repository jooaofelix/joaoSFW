# Reel do pagaAí

Vídeo de 35s (41s com a assinatura da Desata), vertical, sem narração — texto
na tela, no ritmo de corte rápido de comercial de fintech.

```bash
node demos/gravar.js pagaai pagaai-reel          # regera o vídeo
node demos/assinar.js demos/pagaai/pagaai-reel.mp4 demos/pagaai/pagaai-reel-assinado.mp4
```

| Arquivo | O que é |
|---|---|
| `pagaai-reel.mp4` | O vídeo sem o fecho da Desata. |
| `pagaai-reel-assinado.mp4` | O mesmo, com a assinatura no fim. É o que se posta. |
| `palco.html` | As 13 cenas. Mudar texto é aqui. |
| `roteiro.js` | Quanto tempo cada cena fica na tela. Mudar ritmo é aqui. |
| `assets/` | Logo e mascote, copiados do app (repositório Controle-financeiro). |

## A estrutura

Segue a forma de comercial de app que funciona em Reels:

| Trecho | Cenas | O que faz |
|---|---|---|
| Gancho | 1 a 4 | Mostra a bagunça que o casal reconhece: você pagou, ela pagou, ninguém anotou, e a fatura vence. |
| Virada | 5 | "Agora elas se anotam sozinhas." |
| Desenvolvimento | 6 a 11 | A compra virando registro, a categoria sozinha, de dia e de noite, quem gastou o quê, o que vence, o total do mês. |
| Fecho | 12 e 13 | "Enquanto vocês vivem, o pagaAí anota" e a assinatura da marca. |

O gancho corta a cada 1,5 a 2,6 segundos; as cenas com mais o que ler ganham
um pouco mais de ar. Sem narração: o vídeo tem de funcionar mudo, que é como
a maioria assiste no feed.

Cores e mascote saem do próprio app, não de uma paleta inventada: fundo
`#0B0C0A`, verde `#C5F439`, cartões `#171915`.

Os valores na tela são ilustrativos, e isso está escrito no último quadro.
