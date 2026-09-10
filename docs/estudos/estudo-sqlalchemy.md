# Estudo Teórico: SQLAlchemy

## 1. O que é um ORM (Object-Relational Mapping) e por que ele existe

ORM é uma técnica de programação que faz a "ponte" entre o mundo orientado a objetos (classes, atributos, métodos) e o mundo relacional dos bancos de dados (tabelas, colunas, linhas).

Na prática, um ORM permite que o desenvolvedor trabalhe com objetos Python em vez de escrever SQL diretamente. Por exemplo, em vez de escrever:

```sql
SELECT * FROM usuarios WHERE id = 1;
```

Você escreve algo como:

```python
session.query(Usuario).filter_by(id=1).first()
```

**Por que ele existe:**
- Reduz a quantidade de SQL "cru" espalhado pelo código.
- Torna o código mais legível e mais próximo da lógica da aplicação.
- Facilita a manutenção: se o banco de dados mudar (ex: de SQLite para PostgreSQL), grande parte do código não precisa ser alterada.
- Ajuda a evitar erros comuns, como SQL Injection, já que o ORM trata a parametrização das queries automaticamente.
- Permite pensar no domínio do problema (usuários, pedidos, produtos) em vez de pensar em tabelas e joins o tempo todo.

---

## 2. Diferença entre SQLAlchemy Core e SQLAlchemy ORM

O SQLAlchemy é dividido em duas camadas principais, que podem ser usadas separadamente ou em conjunto:

### SQLAlchemy Core
- É a camada mais baixa e mais próxima do SQL.
- Trabalha com **tabelas, expressões SQL e execução de queries** de forma explícita.
- O desenvolvedor constrói as queries usando uma API do tipo "SQL Expression Language", mas ainda pensando em termos de tabelas e colunas, não de objetos.
- Dá mais controle e performance, sendo indicado para quem precisa de queries muito específicas ou otimizadas.

### SQLAlchemy ORM
- É construído **em cima do Core**.
- Permite mapear classes Python para tabelas do banco de dados.
- O foco passa a ser em **objetos e relacionamentos**, não em SQL puro.
- É mais produtivo para aplicações comuns (CRUD, regras de negócio, relacionamentos entre entidades).

**Resumindo:** o Core é mais "SQL com Python", enquanto o ORM é mais "objetos que viram SQL por baixo dos panos".

---

## 3. Conceito de Engine e como ela representa a conexão com o banco

A **Engine** é o ponto central de conexão do SQLAlchemy com o banco de dados. Ela é responsável por:

- Gerenciar o **pool de conexões** (reaproveitar conexões abertas em vez de criar uma nova a cada operação).
- Traduzir os comandos do SQLAlchemy para o dialeto SQL específico do banco (SQLite, PostgreSQL, MySQL etc.).
- Servir como a "porta de entrada" para executar comandos SQL, seja via Core, seja via ORM.

De forma conceitual, a Engine não abre uma conexão imediatamente ao ser criada — ela é **preguiçosa (lazy)**: só estabelece conexão de fato quando alguma operação é executada.

Exemplo de string de conexão (apenas para entender a estrutura, sem executar):

```
dialeto+driver://usuario:senha@host:porta/banco
```

---

## 4. Conceito de Session e seu papel no gerenciamento de transações

A **Session** é o principal ponto de interação quando se usa o ORM. Ela representa uma espécie de "área de trabalho" onde os objetos Python (instâncias de Models) são:

- **Adicionados** (novos registros a serem inseridos)
- **Modificados** (alterações em objetos já existentes)
- **Removidos** (exclusões)
- **Consultados** (queries)

A Session mantém o controle de todas essas mudanças em memória e só as envia de fato para o banco quando um **commit** é realizado. Caso algo dê errado, é possível fazer um **rollback**, desfazendo as alterações pendentes.

**Papel no gerenciamento de transações:**
- Garante que um conjunto de operações seja tratado como uma unidade (tudo ou nada), respeitando o conceito de transação.
- Evita inconsistências: se uma operação falhar no meio do processo, o rollback impede que o banco fique em um estado parcialmente atualizado.
- Controla o "ciclo de vida" dos objetos (novo, persistente, removido, etc.), sabendo quando sincronizar cada objeto com o banco.

---

## 5. O que são Models/Classes declarativas e como se relacionam com tabelas

No SQLAlchemy ORM, uma **Model** é uma classe Python comum que é "mapeada" para uma tabela do banco de dados usando o sistema **declarativo** (`declarative_base`).

Cada classe representa uma tabela, e cada atributo da classe representa uma coluna dessa tabela. Por exemplo, conceitualmente:

- Classe `Usuario` → tabela `usuarios`
- Atributo `id` → coluna `id`
- Atributo `nome` → coluna `nome`

Esse mapeamento permite que uma instância da classe (um objeto Python) corresponda a uma **linha** da tabela, e que os atributos desse objeto correspondam aos **valores das colunas** naquela linha.

A grande vantagem conceitual é que o desenvolvedor pode manipular esses objetos usando lógica orientada a objetos (herança, métodos, propriedades), enquanto o SQLAlchemy cuida de traduzir isso para operações SQL por trás dos panos.

---

## 6. Conceito de relacionamentos entre tabelas (1:1, 1:N, N:N) na teoria do ORM

Bancos relacionais frequentemente precisam representar relações entre entidades. O ORM permite modelar essas relações diretamente entre classes, refletindo os relacionamentos entre tabelas:

### Um-para-um (1:1)
Cada registro de uma tabela está associado a **no máximo um** registro de outra tabela.
Exemplo conceitual: um `Usuario` tem um único `Perfil`.

### Um-para-muitos (1:N)
Um registro de uma tabela pode estar associado a **vários** registros de outra tabela, mas cada registro da segunda tabela pertence a apenas um da primeira.
Exemplo conceitual: um `Usuario` pode ter vários `Post`s, mas cada `Post` pertence a um único `Usuario`.

### Muitos-para-muitos (N:N)
Vários registros de uma tabela podem se relacionar com vários registros de outra tabela. Esse tipo de relacionamento normalmente exige uma **tabela intermediária (tabela de associação)**.
Exemplo conceitual: `Aluno`s podem estar matriculados em vários `Curso`s, e cada `Curso` pode ter vários `Aluno`s.

No ORM, esses relacionamentos são representados através de **chaves estrangeiras (Foreign Keys)** no nível das tabelas, e através do conceito de `relationship` no nível dos objetos — que permite "navegar" de um objeto para outro relacionado (ex: acessar `usuario.posts` para obter todos os posts daquele usuário).

---

## 7. Vantagens e desvantagens de usar um ORM em vez de SQL puro

### Vantagens
- **Produtividade:** menos código repetitivo para operações comuns (CRUD).
- **Legibilidade:** o código fica mais próximo da lógica de negócio, menos "SQL disperso".
- **Portabilidade:** trocar de banco de dados costuma exigir poucas mudanças no código.
- **Segurança:** reduz o risco de SQL Injection, pois as queries são parametrizadas automaticamente.
- **Manutenção:** alterações no modelo de dados (ex: adicionar uma coluna) tendem a ser mais fáceis de propagar pelo código.
- **Relacionamentos facilitados:** navegar entre entidades relacionadas é mais natural do que escrever joins manualmente.

### Desvantagens
- **Curva de aprendizado:** entender como o ORM traduz objetos em SQL exige tempo, além de aprender a própria linguagem SQL.
- **Performance:** em queries muito complexas ou otimizadas, o SQL gerado automaticamente pode ser menos eficiente do que um SQL escrito manualmente.
- **Abstração excessiva:** pode "esconder" o que está realmente acontecendo no banco, dificultando a depuração de problemas de performance.
- **Overhead:** para operações muito simples, o uso do ORM pode adicionar uma camada de complexidade desnecessária.
- **Casos avançados:** certas queries muito específicas do banco (funções nativas, otimizações particulares) podem ser mais difíceis de expressar via ORM, exigindo cair para SQL puro (via Core ou `text()`).

---

## Resumo Final

| Conceito | Ideia Central |
|---|---|
| ORM | Traduz objetos Python em operações de banco relacional |
| Core vs ORM | Core = SQL com Python / ORM = objetos com relacionamentos |
| Engine | Ponto de conexão e tradução para o dialeto do banco |
| Session | Área de trabalho que controla transações (commit/rollback) |
| Models | Classes que representam tabelas; instâncias representam linhas |
| Relacionamentos | 1:1, 1:N, N:N — modelados via Foreign Keys e `relationship` |
| ORM vs SQL puro | Produtividade e segurança x controle fino de performance |