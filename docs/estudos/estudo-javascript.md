# Estudo de JavaScript — Fundamentos (Parte Inicial)

## 1. O que é JavaScript

JavaScript (JS) é a linguagem que roda **junto com HTML e CSS** para construir sites e aplicações:

- **HTML** → conteúdo ("substantivo")
- **CSS** → apresentação/layout do conteúdo ("adjetivo")
- **JS** → a programação em si, o comportamento ("verbo")

Características gerais:
- Não é preciso se preocupar com gestão de memória manualmente (o motor da linguagem cuida disso).
- Suporta diferentes estilos de programação (não é só orientado a objetos — ver seção 2).
- Existem frameworks/bibliotecas (React, Angular, Vue...) que facilitam a programação e o desenvolvimento — todos ainda baseados em JS puro por baixo.
- JS também roda **fora do navegador**, através do **Node.js**, permitindo criar aplicações **back-end** (inclusive com interface com bancos de dados). Os navegadores, nesse contexto, são o **front-end**.
- Saída no console: `console.log(...)`.

---

## 2. Tipos e Tipagem

JS **não é orientado a objetos por natureza** (é multi-paradigma), mas seus tipos primitivos lembram bastante os de outras linguagens:

- **Number**: unifica float e int (não existe tipo `int` separado).
  - `.length` não se aplica a number — é usado para descobrir o tamanho de strings/arrays.
- **String** e **Boolean**.
- **Undefined**: variável foi declarada mas não recebeu valor atribuído — parecido com `null`, mas não é a mesma coisa (`null` é a ausência de valor atribuída intencionalmente; `undefined` é a ausência por falta de atribuição).
- **BigInt**: usado para números muito grandes, além do limite seguro de `Number`.

Um ponto importante: **o valor tem um tipo, não a variável** — os tipos são atribuídos automaticamente (tipagem dinâmica), diferente de linguagens com tipagem estática.

- `typeof variavel` retorna o tipo do valor atualmente armazenado na variável.

---

## 3. Declaração de Variáveis

- `let` — declara uma variável que **pode ser alterada** depois.
- `var` — forma antiga, ainda funciona, mas é considerada legada (evitar em código novo, por causa de comportamento de escopo menos previsível).
- `const` — declara uma variável **imutável** (não pode ser reatribuída depois de criada).

---

## 4. Operadores

Os operadores aritméticos básicos são os mesmos de outras linguagens (`+`, `-`, `*`, `/`), com alguns detalhes:

- **Exponenciação**: `2 ** 3` equivale a 2³.
- **Concatenação**: somar (`+`) duas strings as une (concatena) em vez de somar numericamente.

### Template Strings

Com crase (`` ` ``) é possível criar uma string e inserir variáveis dentro dela usando `${...}`:

```js
`Oi ${nome}!`
```

### Métodos de String

- `.slice(inicio, fim)` — corta um trecho da string.
- `.toUpperCase()` — transforma tudo em caixa alta.

---

## 5. Conversão e Coerção de Tipos

JS, assim como outras linguagens (ex: Java), tem tanto **conversão explícita** quanto **coerção implícita** de tipos:

| Conversão | Sintaxe |
|---|---|
| String → Number | `Number(string)` |
| Number → String | `String(numero)` |
| Qualquer → Boolean | `Boolean(qualquerValor)` |

- A coerção acontece de forma parecida com Java (o próprio JS converte o tipo automaticamente quando necessário em uma expressão).
- Na conversão para **Boolean**: são considerados **falsy** (viram `false`): `0`, string vazia `""`, `undefined`, `null` e `NaN`. Todo o resto é **truthy** (vira `true`).

### Igualdade: `==` vs `===`

- `===` (**igualdade estrita**) — **não faz coerção de tipo**. É a forma recomendada/mais indicada de comparar.
- `==` (**igualdade solta**) — **faz coerção de tipo** antes de comparar (ex: `1 == "1"` é considerado igual, porque o JS converte a string para número antes de comparar). Por isso é uma prática evitada por muitos desenvolvedores.

---

## 6. Entrada e Saída (interação com o usuário)

- `prompt("mensagem")` — abre um pop-up pedindo uma entrada de valor do usuário.
- `alert("mensagem")` — abre um pop-up mostrando uma mensagem (sem pedir entrada).

---

## 7. Operadores Lógicos

- `&&` (**AND**, "e comercial") — verdadeiro somente se **todos** os operandos forem verdadeiros.
- `||` (**OR**) — verdadeiro se **pelo menos um** operando for verdadeiro.
- `!` (**NOT**) — inverte o valor lógico.

---

## 8. Estruturas Condicionais

### if / else

Funciona exatamente da mesma forma que em C.

### switch-case

Também é igual ao de C:

```js
switch (variavel) {
  case "situacao":
    // ...
    break;
  default:
    // "caso inválido"
}
```

- `default` funciona como o caso que trata qualquer valor não previsto nos `case`s anteriores.

### Ternary Operator

Permite reduzir um bloco `if/else` simples numa única linha, atribuindo uma condição seguida de `?` e depois o caso verdadeiro e o caso falso:

```js
condicao ? valorSeVerdadeiro : valorSeFalso;
```

---

## 9. Funções

Em JS, **funções são valores, não apenas tipos/estruturas** — ou seja, podem ser atribuídas a variáveis, passadas como parâmetro etc.

### Declaração (forma normal)

```js
function calc(ano) {
  return 2026 - ano;
}
```

- Os parâmetros são automáticos, não é preciso declarar tipo.
- Se a função retorna algo, usa-se `return` ao final.

### Expressão de função

A função é atribuída a uma variável, e a função passa a "ter" o nome dessa variável:

```js
const calc = function (ano) {
  return 2026 - ano;
};
```

### Arrow Function

```js
variavel = (parametro) => metodo;
```

- Se o corpo for uma expressão única (sem chaves), o `return` é **implícito**.
- Se for necessário um corpo com múltiplas linhas, as chaves `{}` continuam sendo usadas normalmente, e nesse caso o `return` deixa de ser implícito (precisa ser escrito).

### Strict Mode

Declarado no início do código (`"use strict";`). Ajuda a evidenciar erros no código, funcionando de forma parecida com um compilador mais rígido (evita atribuições silenciosas a variáveis não declaradas, entre outras validações).

---

## 10. Objeto `Math`

- `Math.round(x)` — arredonda para o número inteiro mais próximo (não é só "para cima": só arredonda para cima quando a parte decimal é `.5` ou maior).
- `Math.floor(x)` — **sempre** arredonda para baixo.
- `Math.random()` — gera um número pseudoaleatório entre `0` (inclusive) e `1` (exclusive).
  - Combinando com `Math.floor()`, é possível gerar números inteiros aleatórios num intervalo: multiplica-se o resultado de `Math.random()` por outro número para escalar o intervalo antes de aplicar o `floor` — **importante não esquecer essa escala**, senão o resultado fica sempre entre 0 e 1.

```js
Math.floor(Math.random() * 10); // inteiro aleatório entre 0 e 9
```

---

## 11. Arrays

- Declarado de forma parecida com C, usando `nome[]`.
- `nome.includes(coisa)` — pesquisa se determinado valor existe dentro do array.
- `nome.push(coisa)` — adiciona um item ao **final** do array.
- `nome.pop()` — remove o **último** item do array.

---

## 12. Loops

- `while (...)` — funciona exatamente igual ao de C.
- `for (inicio; fim; incremento)` — também igual ao de C.

---

## Referências

Anotações próprias feitas durante o estudo inicial de JavaScript.
