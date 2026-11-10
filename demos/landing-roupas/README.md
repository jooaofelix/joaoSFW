# Landing page de funil — marca de roupas

Página única que existe para uma coisa só: levar quem chega do perfil até uma
conversa no WhatsApp, já sabendo qual peça a pessoa quer.

`pagina.html` roda sozinha no navegador. **Trama** é uma marca fictícia.

## Por que ela não usa as cores da Desata

A Desata é quem faz o site; a marca do cliente é outra. Esta página tem
identidade própria — papel greige `#E5E1D6`, tinta `#191917` e cobalto
`#2538C9`, com a Fraunces nos títulos — justamente para mostrar que o cliente
recebe uma identidade dele, e não um site pintado com as cores do fornecedor.
A identidade da Desata aparece no vídeo: abertura, legendas e fecho.

## O funil, seção por seção

| Seção | O que faz |
|---|---|
| Perfil | Onde o funil começa de verdade: o link do perfil. |
| Capa | O tamanho da leva, a promessa e o que esperar. Sem menu: numa página de funil, âncora é fuga. |
| A leva | As peças com preço e número de edição. Cada botão abre o WhatsApp **dizendo qual peça é**. |
| Como funciona | Três passos, para quem nunca comprou assim. |
| Antes de perguntar | As três objeções que travam a compra: troca, prazo e ver antes. |
| Fecho | Última chamada, e a barra de WhatsApp que acompanha a rolagem inteira. |

## Ao usar com um cliente de verdade

- Trocar os desenhos por **fotos reais** das peças (é mexer em `pagina.html`).
- Os botões levam a `api.pedir()` porque isto é uma demonstração. No site real,
  viram links `https://wa.me/<número>?text=<mensagem>` — mesma mensagem pronta.
- Prazo de troca, formas de pagamento e entrega precisam ser **os que o cliente
  cumpre**. Os textos daqui são exemplo.
