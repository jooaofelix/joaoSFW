# Instagram da Desata — o que escrever

Tudo aqui é para copiar e colar. As artes estão em `artes/`.

---

## 1. O perfil

### Foto
Quatro opções em `artes/perfil-*.png`, todas só com o símbolo: em 32px, que é
o tamanho que aparece nos comentários, o logo inteiro com a palavra vira um
borrão — o símbolo sozinho continua legível.

| Arquivo | Fundo e símbolo |
|---|---|
| `perfil-grafite.png` | Grafite com símbolo laranja. **A que eu usaria**: círculo escuro se destaca na interface branca do Instagram, e o laranja faz o trabalho da marca. |
| `perfil-laranja.png` | Laranja com símbolo off-white. A mais barulhenta; combina com o kit original. |
| `perfil-off-white.png` | Off-white com símbolo laranja. A mais discreta — some um pouco no fundo branco do app. |
| `perfil-laranja-grafite.png` | Laranja com símbolo grafite. Maior contraste dos quatro. |

Testei os quatro reduzidos a 32px: todos continuam reconhecíveis.

### Nome (o campo "Nome", não o @)
Esse campo entra na busca do Instagram, e o @ já diz "sistemas" — então use o
campo Nome para o que o @ não cobre:

```
Desata · Sites e sistemas sob medida
```

### @ (nome de usuário)
```
@desatasistemas
```
Já está nas artes de fecho e no rodapé do site. Se ele estiver ocupado na hora
de criar, me avise: tenho de trocar em três lugares (artes, `config.js` do site
e este arquivo).

### Bio

**Opção A — direta** (a que eu usaria)
```
Tecnologia que descomplica.
Sites e sistemas sob medida para pequenos negócios.
São José dos Campos · SP
```

**Opção B — pela dor**
```
Seu negócio pode fluir melhor.
Sites, sistemas e automações sem complicação.
Fale comigo ↓
```

**Opção C — curta**
```
Menos nós. Mais possibilidades.
Sites e sistemas para quem empreende.
```

Não escrevi "atendo todo o Brasil" nem prazo de entrega: só entra se for o que
você cumpre.

### Link
Um só, o do site. **Confirme que o endereço abre antes de colocar** — link
quebrado na bio é pior do que bio sem link. Se o site ainda não estiver no ar,
use o link direto do WhatsApp:

```
https://wa.me/5512991338866?text=Ol%C3%A1!%20Vim%20pelo%20Instagram%20da%20Desata
```

### Destaques

O nome do destaque é o texto embaixo da bolinha, e o Instagram corta por volta
de 10 caracteres. Por isso os quatro são curtos:

| Capa | Nome |
|---|---|
| `artes/destaque-servicos.png` | Serviços |
| `artes/destaque-processo.png` | Processo |
| `artes/destaque-duvidas.png` | Dúvidas |
| `artes/destaque-contato.png` | Contato |

**Um destaque não existe sem story dentro.** Primeiro publique o story, depois
crie o destaque a partir dele e só então troque a capa (Editar destaque →
Editar capa → escolher da galeria).

**Crie na ordem inversa**: Contato, Dúvidas, Processo, Serviços. O destaque mais
recente fica à esquerda, então criando ao contrário eles acabam na ordem certa.

As telas de story já estão prontas em `artes/story-*.png`, em 1080x1920 — as
artes dos posts são 4:5 e ficariam com tarja no story.

| Destaque | Stories, nesta ordem |
|---|---|
| Serviços | `story-servicos-1` · `-2` · `-3` (sites, sistemas, automações) |
| Processo | `story-processo-1` a `-5` (os cinco passos) |
| Dúvidas | `story-duvidas-1` · `-2` · `-3` (preço, prazo, domínio) |
| Contato | `story-contato` + o sticker de link e o de WhatsApp por cima |

No story de contato, acrescente o **sticker de link** apontando para o site (ou
para o WhatsApp) antes de publicar: dentro do destaque ele continua clicável.

---

## 2. As legendas

A primeira linha de cada uma já é o gancho — é o que aparece no feed antes do
"... mais". Não comece por outra coisa. O porquê de cada gancho está no
`estrategia.md`.

Cada parágrafo é **uma linha só**: copie e cole inteiro, sem mexer. Quebra de
linha no meio da frase, no celular, parece texto quebrado.

### 01 · Manifesto — `01-manifesto.png`
```
A Desata nasceu de uma irritação: tecnologia que dá mais trabalho do que resolve.

Eu desenvolvo sites e sistemas para pequenos negócios e prestadores de serviço — do jeito que a sua rotina já funciona, não do jeito que um software genérico manda.

O nome vem de desatar nós. Os nós são aquelas coisas que travam o dia: informação espalhada, tarefa repetitiva, cliente sem saber o que você faz.

Me conta qual é o seu nó aqui nos comentários ou no direct.

#tecnologia #pequenosnegocios #sitesprofissionais #saojosedoscampos
```

### 02 · Nó 01, presença — `02-no-presenca.png`
```
Pesquise o nome do seu negócio no Google agora. O que aparece?

Se veio um perfil parado — ou nada —, é disso que este post fala. Um perfil parado há três meses não responde as perguntas que o cliente tem: o que você faz, como funciona, quanto custa, como falar com você.

Um site responde isso enquanto você trabalha.

#sitesprofissionais #presencadigital #pequenosnegocios
```

### 03 · Nó 02, repetição — `03-no-repeticao.png`
```
Se você copia e cola a mesma explicação no WhatsApp, esse post é sobre você.

Mesmo texto, mesmas perguntas, do zero, cada vez. Isso é tempo que sai do atendimento de quem já é cliente.

Uma página bem feita explica uma vez e continua explicando sozinha.

#atendimento #whatsappbusiness #sitesprofissionais
```

### 04 · Nó 03, memória — `04-no-memoria.png`
```
Funciona bem. Até o dia em que você esquece.

Você sabe o que está pendente porque lembra — e lembrar é um trabalho a mais.

Pedido no WhatsApp, anotação no caderno, planilha no computador. A informação existe; o que falta é um lugar só.

Dá para resolver sem virar uma empresa cheia de sistema.

#organizacao #gestao #sistemas #pequenosnegocios
```

### 05 · Serviços — `05-servicos.png`
```
Três coisas que eu faço — e uma que eu me recuso a fazer.

SITES — a página que apresenta sua empresa, explica os serviços e facilita o pedido de orçamento. É por onde quase todo projeto começa.

SISTEMAS — ferramentas sob medida para organizar a operação por dentro: pedidos, acompanhamento, formulários, informação centralizada.

AUTOMAÇÕES — o que você repete toda semana virando rotina automática.

E o que eu não faço: vender sistema pronto como se servisse para toda empresa igual. Cada projeto é avaliado conforme a necessidade — e se não for o melhor caminho para você, eu digo antes de você gastar.

#desenvolvimentoweb #sitesprofissionais #automacao
```

### 06 · Fundador — `06-fundador.png`
```
Você vai falar comigo o tempo todo. Não tem equipe de atendimento no meio.

Sou o João. Venho da área comercial e convivi de perto com a rotina de empresas — por isso costumo entender o problema antes de falar de tecnologia.

Na prática: você conversa comigo, eu entendo a necessidade e eu desenvolvo. Sem intermediário e sem palavra difícil no meio da conversa.

#empreendedorismo #desenvolvedor #saojosedoscampos
```

### 07 · Carrossel, como funciona — `07-processo-1` a `11-processo-5`
```
Ninguém devia contratar nada sem saber o que vem depois. Então, o passo a passo:

Arrasta para o lado. Sem mistério e sem surpresa: a conversa é de graça, o escopo vai por escrito antes de qualquer trabalho começar, e você valida tudo antes de ir ao ar.

O suporte depois da entrega fica definido na proposta — o que inclui, por quanto tempo e como pedir.

Quer conversar sobre o seu projeto? Chama no direct.

#comofunciona #sitesprofissionais #pequenosnegocios
```

---

## 3. As três primeiras semanas

Uma postagem a cada dois ou três dias é suficiente no começo. Esta ordem abre
com o posicionamento e só depois vende:

| Dia | Post |
|---|---|
| 1 | Manifesto — explica quem é a Desata |
| 3 | Nó 01, presença |
| 5 | Fundador — gente compra de gente |
| 8 | Nó 02, repetição |
| 11 | Carrossel: como funciona |
| 14 | Nó 03, memória |
| 17 | Serviços |

As três artes do kit original (`marca/desata-post-0*.png`) são quadradas e
entram quando quiser respiro entre os assuntos.

### Sobre o que não postar ainda
Sem cliente, sem depoimento, sem "projeto entregue" e sem número de resultado
enquanto não houver. A Desata está começando, e o perfil pode dizer isso sem
perder autoridade — o que dá autoridade agora é explicar bem o problema.

Quando o primeiro projeto sair, aí sim: print da tela, o antes e o depois, e o
que mudou na rotina do cliente — com a autorização dele.
