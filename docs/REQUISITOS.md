# Cerradinho — API aberta da UnB

Análise de requisitos e planejamento — MDS, UnB FCTE
Equipe: Vitor, Ítalo, Daniel, Arthur, Gabriel, João Paulo

## 1. Objetivo

API pública que consolida dados da UnB hoje espalhados em vários sistemas: disciplinas, professores, salas/prédios, cardápio do RU, eventos e editais. Todas as fontes usadas são públicas, sem login.

## 2. Fontes de dados

| Domínio | Fonte | Observação |
|---|---|---|
| Disciplinas | sigaa.unb.br/sigaa/public/turmas | JSF (ViewState/postback) — precisa de Playwright |
| Professores | Mesma página + sti.unb.br/portal-publico-sigaa | Vem junto da turma |
| Cursos/Estrutura curricular | sigaa.unb.br/sigaa/public/curso | Complementa Disciplinas |
| Salas/Prédios | Sem fonte própria | Extraído como subproduto do scraper de Disciplinas |
| Cardápio RU | ru.unb.br/cardapio | Aberto, sem login |
| Eventos | noticias.unb.br/agenda | Agenda institucional pública |
| Editais | Portal Público SIGAA (pós-graduação) | Centralizado |
| Complemento | dadosabertos.unb.br (CKAN) | Bom para seed de Unidades/Cursos; Turmas está desatualizado (2022) |

## 3. Requisitos Funcionais — Core

**Disciplinas**
- RF01 — Capturar oferta de disciplinas de todas as unidades (nome, código, turma, horário, vagas), com scraper por unidade e throttling
- RF02 — Associar disciplina a professor
- RF03 — Associar disciplina a sala/prédio

**Professores**
- RF04 — Cadastro de docentes vinculados às disciplinas

**Salas/Prédios**
- RF05 — Localização e identificação de salas e prédios (derivado de RF01)

**Cardápio do RU**
- RF06 — Capturar cardápio diário
- RF07 — Manter histórico de cardápios

**Eventos**
- RF08 — Capturar eventos institucionais (data, local, descrição)

**Editais**
- RF09 — Capturar editais publicados (título, data, link, órgão)

**API pública**
- RF10 — Endpoints REST por domínio
- RF11 — Documentação OpenAPI/Swagger
- RF12 — Versionamento (`/v1/`)
- RF13 — SDK/CLI para integração de terceiros e squads futuros
- RF14 — Portal do desenvolvedor

**Atualização de dados**
- RF15 — Agendamento automático de scraping
- RF16 — Log de sucesso/falha de cada execução

## 4. Features derivadas

Calculadas em cima do que os domínios acima já capturam — baixo esforço extra.

- **RF17 — Salas vazias**: `GET /v1/salas/vazias?dia=segunda&horario=14:00` — cruza Sala com Disciplina no horário pedido. Só reflete aula cadastrada, não reserva informal.
- **RF18 — Agenda do professor**: `GET /v1/professores/{nome}/agenda` — lista as turmas de um docente.
- **RF19 — Cardápio semanal**: `GET /v1/cardapio/semana?data_inicio=...` — agrupa 7 dias de histórico.

## 5. Requisitos Não-Funcionais

| ID | Requisito | Descrição |
|---|---|---|
| RNF01 | Rate limiting | Limitar requisições por cliente/IP |
| RNF02 | Cache | Reduzir tempo de resposta e carga no banco |
| RNF03 | Observabilidade | Monitoramento de uptime e alertas |
| RNF04 | Testes de contrato | API não pode quebrar formato esperado |
| RNF05 | Resiliência | Scraper falha de forma graciosa se a fonte mudar |
| RNF06 | Disponibilidade | Uptime confiável |
| RNF07 | Doc viva | Documentação reflete o estado real da API |

## 6. Repositório e fluxo de Git

Repositório: [github.com/unb-mds/G3-2026-2](https://github.com/unb-mds/G3-2026-2)

- Monorepo — um único repositório com pastas `/frontend` e `/backend`
- Branches: `main` (estável) → `dev` (integração) → `feature/nome-da-tarefa`
- Commits em Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)
- Todo PR precisa de revisão antes de merge
- Organização de tarefas via Issues + board (Projects) do GitHub

## 7. Equipe

| Pessoa | Área | Responsabilidade | Tecnologias |
|---|---|---|---|
| Vitor | Backend | Scraping de Disciplinas/Professores/Salas + endpoints | FastAPI, Playwright, SQLAlchemy |
| Ítalo | Backend | Scraping de RU/Eventos/Editais + endpoints | FastAPI, BeautifulSoup, SQLAlchemy |
| Daniel | Frontend | Telas de consulta + portal do dev | Next.js, Axios, Swagger UI |
| Arthur | Infra de jobs | Celery/Redis, cache, rate limit | Celery, Redis, slowapi |
| Gabriel | Banco/Deploy/Scrum Master | Modelagem, Docker, deploy, facilitação do squad | PostgreSQL, SQLAlchemy, Alembic, Docker, Railway |
| João Paulo | QA/Integração | Investigação de fontes, testes de contrato, observabilidade | DevTools, Postman, Pytest, schemathesis, UptimeRobot |

## 8. Requisito → responsável

| Pessoa | Requisitos |
|---|---|
| Vitor | RF01-05, RF17, RF18, RF13 (SDK) |
| Ítalo | RF06-09, RF19, RF13 (CLI) |
| Daniel | RF10, RF11, RF14 |
| Arthur | RF15, RF16, RNF01, RNF02 |
| Gabriel | RF12, RNF06, modelagem |
| João Paulo | RNF03, RNF04, RNF05, RNF07 |

## 9. Cronograma por ciclo

O projeto está dividido em 3 ciclos mensais. A quebra de cada ciclo em sprints semanais ainda será definida pelo time.

### Ciclo 1 — Fundação

- **Vitor**: spike de viabilidade no SIGAA (Playwright), scraper de Disciplinas funcional, expansão para todas as unidades, associações Disciplina↔Professor↔Sala (RF01-05)
- **Ítalo**: scraper de RU funcional e estabilizado, início do scraper de Eventos
- **Daniel**: setup do Next.js, telas com dados mockados, integração com API real de RU
- **Arthur**: sobe Celery + Redis, agenda scrapers de RU e Disciplinas, log de execuções (RF16)
- **Gabriel**: schema inicial, Docker Compose, rotas sob /v1/, documentação das decisões de schema
- **João Paulo**: investigação das 5 fontes de dado, relatório de risco

### Ciclo 2 — Core + features derivadas

- **Vitor**: fecha RF04 (Professores), implementa RF17 (salas vazias) e RF18 (agenda do professor)
- **Ítalo**: fecha Eventos e Editais, implementa RF19 (cardápio semanal)
- **Daniel**: conecta todas as telas na API real, inclusive as features derivadas
- **Arthur**: agenda os domínios restantes no Celery, ajusta throttling com volume real
- **Gabriel**: migrations dos novos domínios, performance do banco, índices para RF17/RF18
- **João Paulo**: testes de contrato em todos os domínios já publicados

### Ciclo 3 — Maturidade da API + entrega

- **Vitor**: SDK Python
- **Ítalo**: CLI (Typer) em cima do SDK
- **Daniel**: portal do desenvolvedor
- **Arthur**: cache Redis e rate limit (slowapi)
- **Gabriel**: ambiente de produção e deploy final
- **João Paulo**: observabilidade (UptimeRobot + alertas), testes de contrato finais, checklist board vs. entrega


## 10. Riscos técnicos

| Risco | Impacto |
|---|---|
| SIGAA em JSF | Exige Playwright, não scraping simples |
| Sem fonte pública de Salas | Resolvido por derivação, sem cadastro próprio |
| Sites mudam sem aviso | Manutenção contínua (RNF05) |
| Todas as unidades da UnB | Throttling e agendamento fora de pico; falha isolada não trava o resto |
| Gabriel acumula técnico + Scrum Master | Risco de sobrecarga; mitigado pela distribuição de carga entre ciclos |
