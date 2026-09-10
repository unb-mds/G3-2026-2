# Estudo Teórico: BeautifulSoup

## 1. O que é web scraping e para que ele é usado

**Web scraping** é a técnica de extrair dados de páginas web de forma automatizada, geralmente lendo o HTML de uma página e coletando informações específicas dela (textos, preços, links, imagens, tabelas etc.).

Em vez de um humano copiar e colar informações manualmente de um site, um programa faz esse trabalho de forma automática e em escala.

**Para que é usado:**
- Coleta de dados para pesquisa ou análise (preços de produtos, notícias, avaliações).
- Monitoramento de mudanças em páginas (ex: acompanhar variação de preços).
- Agregação de conteúdo de múltiplas fontes (ex: comparadores de preços).
- Automatização de tarefas repetitivas que envolveriam navegação manual.
- Alimentar bancos de dados ou aplicações com dados que não possuem uma API pública.

---

## 2. Diferença entre web scraping e uso de APIs

Embora os dois sirvam para obter dados de sistemas externos, a abordagem é bem diferente:

### API (Application Programming Interface)
- É uma forma **oficial e estruturada** de acessar dados, disponibilizada pelo próprio site/serviço.
- Retorna dados em formatos previsíveis (geralmente JSON ou XML).
- Costuma ter documentação, regras de uso claras e, muitas vezes, autenticação.
- É a forma **preferida** de obter dados quando disponível, por ser mais estável e permitida.

### Web Scraping
- É usado quando **não existe uma API disponível** (ou ela é limitada) para os dados que se deseja obter.
- Consiste em "ler" o HTML da página como ela é exibida no navegador e extrair as informações manualmente da estrutura.
- É mais **frágil**: se o site mudar o layout/HTML, o scraper pode parar de funcionar.
- Pode envolver questões **legais e éticas**, já que nem todo site permite ser "raspado".

**Resumindo:** API é uma porta aberta e documentada pelo próprio site; scraping é "entrar pela estrutura visual" quando essa porta não existe.

---

## 3. O que é HTML parsing e como o BeautifulSoup interpreta a estrutura de uma página

**HTML parsing** é o processo de analisar o código HTML de uma página e transformá-lo em uma estrutura de dados organizada, que pode ser percorrida e manipulada pelo código.

O HTML é, em sua essência, um documento com tags aninhadas (como `<div>`, `<p>`, `<a>`, `<table>`), formando uma hierarquia — parecida com uma árvore genealógica, onde cada tag pode ter "tags filhas" dentro dela.

O **BeautifulSoup** pega esse HTML "cru" (texto) e o transforma em um objeto Python navegável, onde:
- Cada tag vira um "nó" dentro dessa estrutura.
- É possível acessar tags filhas, tags irmãs e tags pai.
- É possível buscar tags por nome, atributo, classe, id, entre outros critérios.

Ou seja, o BeautifulSoup não interpreta a página como uma imagem visual, mas sim como uma **árvore de elementos estruturados**, permitindo navegação programática por ela.

---

## 4. Diferença entre os parsers disponíveis (`html.parser`, `lxml`, `html5lib`)

O BeautifulSoup não interpreta o HTML sozinho — ele depende de um **parser** (um motor de análise) para transformar o texto HTML em uma árvore de elementos. Existem diferentes parsers, cada um com características próprias:

### `html.parser`
- Vem **embutido no próprio Python** (não precisa instalar nada além do BeautifulSoup).
- É razoavelmente rápido e suficiente para a maioria dos casos simples.
- Pode ser um pouco menos tolerante a HTML malformado do que outras opções.

### `lxml`
- É uma biblioteca externa, muito conhecida por ser **rápida e eficiente**.
- Lida bem com HTML malformado (tags mal fechadas, por exemplo).
- É uma das opções mais usadas em projetos de scraping por conta do desempenho.
- Também pode ser usada para processar XML.

### `html5lib`
- É o parser mais **tolerante e rigoroso em relação às regras do HTML5**.
- Tenta interpretar a página exatamente como um navegador moderno interpretaria.
- É o mais **lento** entre os três, mas o mais preciso em casos de HTML muito "bagunçado".

**Resumindo:** a escolha do parser é um equilíbrio entre **velocidade** e **tolerância a erros** no HTML da página.

---

## 5. Conceito de árvore de elementos (tags, atributos, hierarquia)

Quando o BeautifulSoup faz o parsing de uma página, ele organiza o conteúdo como uma **árvore de elementos**, seguindo a mesma lógica de aninhamento do HTML.

Principais conceitos dessa árvore:

### Tags
São os elementos HTML em si, como `<div>`, `<p>`, `<a>`, `<table>`. Cada tag pode conter texto e/ou outras tags dentro dela.

### Atributos
São informações adicionais dentro de uma tag, como `href` em um link (`<a href="...">`) ou `class`/`id` em uma `<div>`. Eles funcionam como "metadados" daquele elemento.

### Hierarquia (pai, filho, irmão)
- **Tag pai:** a tag que contém outra tag dentro dela.
- **Tag filha:** a tag que está dentro de outra.
- **Tags irmãs:** tags que estão no mesmo nível dentro do mesmo pai.

Essa estrutura hierárquica é o que permite ao BeautifulSoup (e a quem está programando) "navegar" pela página: descer para dentro de uma seção específica, subir para o elemento pai, ou percorrer elementos vizinhos, até chegar exatamente na informação desejada.

---

## 6. Considerações éticas e legais do web scraping (robots.txt, termos de uso)

Fazer scraping de um site não é uma prática neutra — existem aspectos éticos e legais importantes a considerar:

### `robots.txt`
- É um arquivo que muitos sites disponibilizam (geralmente em `/robots.txt`) informando quais partes do site podem ou não ser acessadas por robôs/crawlers.
- Embora seja apenas uma "convenção" (não um bloqueio técnico obrigatório), respeitá-lo é considerado uma boa prática e um sinal de scraping responsável.

### Termos de uso (Terms of Service)
- Muitos sites proíbem explicitamente scraping em seus termos de uso.
- Descumprir esses termos pode gerar consequências que vão desde o bloqueio do acesso até questões legais, dependendo da jurisdição e do uso dado aos dados.

### Outras considerações importantes
- **Dados pessoais:** coletar informações pessoais de usuários pode esbarrar em leis de proteção de dados (como a LGPD no Brasil ou o GDPR na Europa).
- **Sobrecarga no servidor:** fazer muitas requisições em pouco tempo pode prejudicar o funcionamento do site (é considerado boa prática limitar a frequência das requisições).
- **Uso dos dados coletados:** mesmo que a coleta seja tecnicamente possível, o uso comercial ou a redistribuição desses dados pode ter implicações legais (direitos autorais, concorrência desleal, etc.).
- **Transparência:** identificar o scraper (por exemplo, com um `User-Agent` apropriado) é considerado uma prática mais ética do que se passar por um navegador comum de forma dissimulada.

**Resumindo:** antes de fazer scraping de um site, é importante verificar se isso é permitido (robots.txt e termos de uso), respeitar limites técnicos (não sobrecarregar o servidor) e ter cuidado redobrado ao lidar com dados pessoais.

---

## Resumo Final

| Conceito | Ideia Central |
|---|---|
| Web Scraping | Extração automatizada de dados a partir do HTML de páginas |
| Scraping vs API | Scraping "lê" a página; API entrega dados de forma oficial e estruturada |
| HTML Parsing | Transformação do HTML em uma estrutura navegável (árvore) |
| Parsers | `html.parser` (nativo), `lxml` (rápido), `html5lib` (mais tolerante e preciso) |
| Árvore de Elementos | Tags, atributos e hierarquia (pai, filho, irmãos) |
| Ética e Legalidade | Respeitar `robots.txt`, termos de uso, dados pessoais e limites do servidor |