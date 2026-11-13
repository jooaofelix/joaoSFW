# Instagram da Desata

Artes e textos do perfil **@desatasistemas**. O que escrever — bio, @, legendas e a ordem
de postagem — está em [`textos.md`](textos.md).

```bash
npm i playwright                      # uma vez
node instagram/gerar-artes.js         # regera tudo que está em artes/
```

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `arte.html` | Todas as artes, uma por bloco. É aqui que se muda o texto de um post. |
| `gerar-artes.js` | Vira cada bloco em PNG, na pasta `artes/`. |
| `artes/` | Os PNGs prontos para postar. |
| `artes-fonte/icone.png` | O símbolo recortado do logo. Serve de máscara para as fotos de perfil — a cor vem do CSS, então não existe um arquivo por variação. |
| `textos.md` | Bio, nome do perfil, legendas e calendário das três primeiras semanas. |
| `estrategia.md` | Ganchos de abertura, regra de música, o passo a passo de cada publicação e a rotina semanal. |

## As artes

Sete publicações, sendo uma delas um carrossel de cinco telas, e quatro capas
de destaque:

| Arte | Para quê |
|---|---|
| `01-manifesto` | O primeiro post: o que é a Desata e de onde vem o nome. |
| `02-no-presenca`, `03-no-repeticao`, `04-no-memoria` | Série "nós do dia a dia": cada post é um problema real que o cliente reconhece. |
| `05-servicos` | O que a Desata faz, em três linhas. |
| `06-fundador` | Quem atende é quem desenvolve. |
| `07-processo-1` … `11-processo-5` | Carrossel de como funciona contratar. |
| `destaque-*` | Capas dos destaques: Serviços, Como funciona, Dúvidas, Contato. |
| `perfil-*` | Quatro opções de foto de perfil, só com o símbolo. |
| `story-*` | Doze telas de story, em 1080×1920, para encher os quatro destaques. |

## Formatos

As publicações saem em **1080×1350** (proporção 4:5), que é o formato que ocupa
mais tela no celular de quem rola o feed. As capas de destaque saem em
**1080×1080**, com o texto centralizado para sobreviver ao corte redondo.

As três artes do kit original (`marca/desata-post-0*.png`) são quadradas. Pode
misturar: na grade do perfil o corte é igual para todas.

## Mexer no texto de um post

É no `arte.html`, dentro do bloco com o `data-nome` correspondente. A gramática
visual de cada arte segue o kit aprovado: logo no topo, frase forte no meio,
assinatura no pé e o laço saindo pela borda. Os três fundos alternam entre
off-white, grafite e laranja — o mesmo rodízio das artes do kit.

Depois de mexer, rode o gerador de novo e confira se a frase não estourou a
caixa: frases longas pedem a classe `frase--media`.
