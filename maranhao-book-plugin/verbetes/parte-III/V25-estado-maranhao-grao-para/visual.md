# V25 -- Guia Visual
## O Estado do Maranhao e Grao-Para (1621-1774)

**Cor-acento:** #1B4965 (Azul-mar)
**Parte:** III -- Sangue, Cruz e Coroa

---

## VISUAL 1 -- Mapa: Os dois Brasis

### Descricao
Mapa do Brasil colonial mostrando a divisao entre o Estado do Brasil e o Estado do Maranhao como dois territorios distintos, com codigos de cor diferentes. Deve causar impacto visual: o leitor precisa VER que eram dois mundos.

### Especificacoes

**Dimensoes:** Pagina inteira (210 x 270mm) ou meia pagina horizontal (210 x 135mm)
**Estilo:** Cartografico contemporaneo com textura de mapa antigo. Nao e para parecer um mapa de epoca --- e para ser legivel como infografico moderno com estetica historica.

**Elementos obrigatorios:**

1. **Territorio do Estado do Brasil**
   - Cor de preenchimento: tom quente (ocre/terracota, sugestao #C17817)
   - Litoral de Sao Vicente ate o sul de Itamaraca
   - Capital marcada: Salvador (ate 1763) / Rio de Janeiro (apos 1763)
   - Icone de cana-de-acucar no litoral nordestino

2. **Territorio do Estado do Maranhao**
   - Cor de preenchimento: #1B4965 (azul-mar, cor-acento da Parte III)
   - Litoral do Ceara ate o extremo norte, adentrando pela bacia amazonica
   - Capital marcada: Sao Luis (ate 1751) / Belem (apos 1751)
   - Icone de canoa/rio na regiao amazonica

3. **Setas de navegacao maritima**
   - Sao Luis -> Lisboa: seta curva pelo Atlantico Norte. Legenda: "~30 dias"
   - Sao Luis -> Salvador: seta longa contornando o litoral. Legenda: "60-90 dias"
   - Lisboa -> Salvador: seta para comparacao. Legenda: "~45 dias"
   - As setas devem deixar claro que Sao Luis estava "mais perto" de Lisboa do que de Salvador

4. **Correntes maritimas**
   - Indicar a Corrente Norte do Brasil e a Corrente Equatorial que empurravam navios para noroeste
   - Linhas finas pontilhadas com setas pequenas

5. **Legenda**
   - "Estado do Brasil (capital: Salvador/Rio)"
   - "Estado do Maranhao e Grao-Para (capital: Sao Luis/Belem)"
   - "Limites aproximados, c. 1700"

6. **Texto complementar (caixa inferior)**
   - "De 1621 a 1774, o Maranhao nao respondia a Salvador nem ao Rio de Janeiro. Respondia direto a Lisboa. As correntes maritimas tornavam a viagem a Portugal mais curta do que ao restante do Brasil."

### Paleta
- Azul-mar #1B4965 (Estado do Maranhao)
- Ocre #C17817 (Estado do Brasil)
- Oceano: #E8F0F2 (claro, para contraste)
- Texto: #1A1A1A
- Setas de navegacao: #D94F30 (vermelho cartografico)

---

## VISUAL 2 -- Timeline: 153 anos em paralelo

### Descricao
Linha do tempo horizontal mostrando os eventos do Estado do Maranhao ACIMA da barra e os eventos paralelos do Estado do Brasil / mundo ABAIXO, para que o leitor veja as duas historias correndo em paralelo.

### Especificacoes

**Dimensoes:** Pagina inteira horizontal (270 x 210mm) ou spread (dupla pagina)
**Estilo:** Infografico limpo, tipografico. Minimalista com acentos de cor.

**Estrutura:**

```
[EVENTOS DO ESTADO DO MARANHAO -- acima da linha]

========== 1621 ======================== 1774 ==========
         BARRA TEMPORAL PRINCIPAL

[EVENTOS DO ESTADO DO BRASIL / MUNDO -- abaixo da linha]
```

**Marcos acima da barra (Estado do Maranhao):**

| Ano | Evento | Icone |
|-----|--------|-------|
| 1621 | Criacao do Estado do Maranhao | Documento/alvara |
| 1653 | Vieira chega ao Maranhao | Cruz/pulpito |
| 1661 | Vieira expulso pelos colonos | Navio partindo |
| 1684 | Revolta dos Beckman | Espada/forca |
| 1693 | Jesuitas retornam | Cruz |
| 1751 | Capital transferida para Belem | Seta |
| 1755 | Companhia de Comercio | Navio mercante |
| 1755 | Lei de Liberdade dos Indios | Corrente partida |
| 1759 | Expulsao dos jesuitas | Cruz cortada |
| 1774 | Extincao do Estado | Documento rasgado |

**Marcos abaixo da barra (paralelos):**

| Ano | Evento |
|-----|--------|
| 1620 | Pilgrims em Plymouth Rock |
| 1624 | Holandeses invadem Salvador |
| 1630 | Holandeses ocupam Pernambuco |
| 1640 | Restauracao portuguesa |
| 1648 | Paz de Vestfalia |
| 1694 | Destruicao de Palmares |
| 1763 | Capital do Brasil transferida para o Rio |
| 1774 | Intolerable Acts (America do Norte) |

**Codificacao de cor:**
- Marcos do Estado do Maranhao: #1B4965 (azul-mar)
- Marcos paralelos: #6B7280 (cinza neutro)
- Barra temporal: gradiente de #1B4965 (inicio) a #C17817 (fim, simbolizando a reunificacao)
- Destaques (Vieira, Beckman, Pombal): circulos maiores

**Texto complementar (caixa lateral ou inferior):**
"Durante 153 anos, o Maranhao e o Brasil correram em paralelo --- como dois rios que so se encontram na foz. Esta timeline mostra o que acontecia em cada um enquanto o outro seguia seu caminho."

### Paleta
- Azul-mar #1B4965
- Cinza #6B7280
- Ocre #C17817
- Fundo: #FAFAF8 (off-white)
- Texto: #1A1A1A

---

## Notas gerais de producao visual

- Ambos os visuais devem funcionar em impressao (CMYK) e digital (RGB).
- O mapa e a timeline devem ser legíveis em reducao a 50% (para versao e-book).
- Fontes: usar a mesma familia tipografica do projeto (definida no manual de estilo do livro).
- Os visuais podem ser produzidos em Figma, Illustrator ou Canva Pro.
- Exportar em SVG (para edicao) e PNG 300dpi (para diagramacao).
