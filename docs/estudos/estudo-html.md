# Estudo de HTML — Fundamentos

## 1. O que é HTML

**HTML** define o **conteúdo e a estrutura** do site.

- **HT** vem de *Hyper Text*, o mesmo conceito usado nos **hyperlinks**.
- O conteúdo é construído por meio de **tags**.

---

## 2. Heading Elements (Títulos)

```html
<h1>Hello World</h1>
```

A tag de abertura, o conteúdo e a tag de fechamento juntos formam o **elemento**.

```
<h1>   Hello World   </h1>
 ↑          ↑            ↑
open tag  conteúdo   close tag
```

- `<h1>` se refere a um heading de nível 1 — o maior de todos.
- `<h2>` é um heading menor, "dentro" do `<h1>`, e assim por diante até o nível 6 (`<h6>`).
  - É como um sumário: `1`, `1.1`, `1.2`, `2`...
- Conforme o nível aumenta, o tamanho da fonte vai ficando menor — mas a ideia central é a **hierarquia**, não o tamanho.
- **Não deve haver mais de um `<h1>`** por página.
- **Não pule níveis de hierarquia** (não vá de `<h1>` direto para `<h3>`, por exemplo).

---

## 3. Paragraph Element

```html
<p>Isso é um parágrafo</p>
```

- Para testar a formatação de parágrafos antes de ter o conteúdo definitivo, pode-se usar um gerador de **Lorem Ipsum**.

---

## 4. Void Elements

São chamados assim porque **não têm conteúdo entre suas tags** — ou seja, não têm tag de fechamento separada.

```html
<hr />  <!-- Horizontal Rule: cria uma linha horizontal -->
<br />  <!-- Break Element: quebra de linha -->
```

- A barra `/` no final é opcional, mas recomendada.

---

## 5. Listas

### Unordered List — `<ul>`

A ordem dos itens **não importa**.

```html
<ul>
  <li>Conteúdo 1</li>
  <li>Conteúdo 2</li>
</ul>
```

A lista aparece com marcadores (pontinhos):
- Conteúdo 1
- Conteúdo 2

### Ordered List — `<ol>`

A ordem dos itens **importa**.

```html
<ol>
  <li>Conteúdo 1</li>
  <li>Conteúdo 2</li>
</ol>
```

A lista aparece numerada:
1. Conteúdo 1
2. Conteúdo 2

### Listas aninhadas

É possível colocar uma lista dentro da outra, fazendo a identação (indentação) correta dos elementos `<li>`.

---

## 6. Atributos em HTML

```html
<tag atributo="valor">Conteúdo</tag>
```

Existem vários atributos possíveis para cada tag — é preciso pesquisar quais se aplicam a cada elemento.

---

## 7. Anchor Element (Hyperlinks)

```html
<a href="link">Nome</a>
```

- `href` define o **alvo** do hyperlink (para onde ele aponta).

---

## 8. Imagens

```html
<img src="url" />
```

- `src` é a origem (fonte) da imagem.
- É possível acrescentar um atributo `alt="..."` para descrever a imagem (importante para acessibilidade e SEO).

---

## Referências

Anotações manuscritas próprias, feitas durante o estudo inicial de HTML.
