# Comandos para o gerador

Colar junto com o PNG correspondente. Estão em inglês de propósito: é a língua
em que esses modelos foram treinados e em que erram menos.

O começo é igual em todos — é ele que segura o personagem no lugar:

> Animate this exact 2D flat-vector cartoon character. Do not redraw it, do not
> change its style, colors, proportions or line weight, and do not add any new
> object, text or background element. Keep the background solid dark and
> completely static. 2D cel animation, clean vector line art, flat colors, no
> 3D, no camera move, no lighting change, no motion blur.

## 1. `mascote-comemora.png` — o pulinho (o do fecho)

> Animate this exact 2D flat-vector cartoon character. Do not redraw it, do not
> change its style, colors, proportions or line weight, and do not add any new
> object, text or background element. Keep the background solid dark and
> completely static. Motion: the character does three small happy hops in
> place; on each hop it squashes slightly before pushing off, stretches in the
> air and lands with a soft bounce; the arms swing up on the way up; the cards
> tucked in its top flutter a little; the small green motion ticks beside it
> pop and fade on each landing. Nothing else moves. 2D cel animation, clean
> vector line art, flat colors, no 3D, no camera move, no lighting change, no
> motion blur. Loopable: the last frame matches the first.

## 2. `mascote-joinha.png` — a piscadinha

> Animate this exact 2D flat-vector cartoon character. Do not redraw it, do not
> change its style, colors, proportions or line weight, and do not add any new
> object, text or background element. Keep the background solid dark and
> completely static. Motion: the character leans slightly toward the camera,
> winks once, raises its thumb a little higher and holds the pose; a tiny green
> sparkle pops next to the thumb and fades. A gentle idle breathing throughout.
> Nothing else moves. 2D cel animation, clean vector line art, flat colors, no
> 3D, no camera move, no lighting change, no motion blur.

## 3. `mascote-correndo.png` — a chegada

> Animate this exact 2D flat-vector cartoon character. Do not redraw it, do not
> change its style, colors, proportions or line weight, and do not add any new
> object, text or background element. Keep the background solid dark and
> completely static. Motion: the character runs in place with a looping cartoon
> run cycle for about two seconds, then skids to a stop facing the camera with
> its arms out and holds, with a small idle bounce; a little puff of green dust
> appears at its feet on the skid and fades. Nothing else moves. 2D cel
> animation, clean vector line art, flat colors, no 3D, no camera move, no
> lighting change, no motion blur.

## 4. `mascote-moeda.png` — a moeda

> Animate this exact 2D flat-vector cartoon character. Do not redraw it, do not
> change its style, colors, proportions or line weight, and do not add any new
> object, text or background element. Keep the background solid dark and
> completely static. Motion: the character tosses the gold coin a short way up
> and catches it again; the coin spins once in the air; the green ticks beside
> the character pulse once on the catch. Nothing else moves. 2D cel animation,
> clean vector line art, flat colors, no 3D, no camera move, no lighting
> change, no motion blur.

## O que aprendemos com os três primeiros clipes

O da **corrida** deu certo e está no vídeo. Os outros dois quebraram, e sempre
do mesmo jeito. Vale saber onde olhar:

- o **botãozinho quadrado** do lado direito da carteira vira uma etiqueta
  pendurada — é o primeiro defeito a aparecer, e o mais fácil de conferir;
- os **cartões** de cima viram papel branco com desenhos impressos, e em um
  deles viraram uma cédula com rosto;
- os **olhos fechados de sorriso** abrem e viram olhos redondos grandes;
- a **câmera dá zoom** mesmo com o comando pedindo para não dar.

E tem uma diferença de fundo entre o que funcionou e o que não funcionou: a
corrida é um **movimento que se repete**. Por isso dá para pegar um ciclo
inteiro no trecho limpo e rodar em laço — o defeito fica para trás. Quando o
movimento não se repete, como no da moeda, só sobra meio segundo aproveitável.

Então, de agora em diante, peça sempre **movimento que volta ao ponto de
partida** e diga isso com todas as letras no comando.

## Comando corrigido da moeda (pedindo laço)

> Animate this exact 2D flat-vector cartoon character as a short seamless loop.
> The character must stay IDENTICAL to the image in every frame: same shape,
> same colors, same line weight, same closed smiling eyes, same small square
> button on its right side, same two cards tucked in the top, same gold coin in
> its hand. Do not redraw the face, do not open the eyes, do not turn the cards
> into paper or banknotes, do not add or remove any object or text, and do not
> move or zoom the camera — the framing stays exactly as in the image. Keep the
> background solid dark and completely static. Motion: only a gentle up and
> down bob in place, about one cycle per second, with a small squash as it
> comes down and a small stretch as it goes up; the green ticks beside its head
> pulse once per cycle. The last frame must match the first frame exactly, so
> the clip loops seamlessly. 2D cel animation, flat colors, no 3D, no shading
> change, no motion blur, minimum motion.

Se o gerador tiver um controle de intensidade de movimento, ponha no mínimo.
Gere umas cinco vezes e escolha pelo botãozinho do lado: se ele virar etiqueta
pendurada em algum quadro, descarte.

## Se o gerador só aceitar texto, sem imagem

Não use. Sem a imagem ele desenha **outro** personagem, e aí não é o mascote do
pagaAí — é um mascote qualquer. O valor da peça é a marca aparecer igual.
