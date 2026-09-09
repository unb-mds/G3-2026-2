# Cerradinho - API aberta da UnB

Análise de requisitos e planejamento - MDS, UnB FCTE
Equipe: Vitor, Ítalo, Daniel, Arthur, Gabriel, João Paulo

Fluxo de trabalho do time, padrões de repositório e governança de projeto estão em [`PROCESSO.md`](PROCESSO.md).

## 1. Objetivo

API pública que consolida dados da UnB hoje espalhados em vários sistemas: disciplinas, professores, salas/prédios, cardápio do RU, eventos e editais. Todas as fontes usadas são públicas, sem login.

## 2. Fontes de dados

| Domínio | Fonte | Observação |
|---|---|---|
| Disciplinas | sigaa.unb.br/sigaa/public/turmas | JSF (ViewState/postback) - precisa de Playwright |
| Professores | Mesma página + sti.unb.br/portal-publico-sigaa | Vem junto da turma |
| Cursos/Estrutura curricular | sigaa.unb.br/sigaa/public/curso | Complementa Disciplinas |
| Salas/Prédios | Sem fonte própria | Extraído como subproduto do scraper de Disciplinas |
| Cardápio RU | ru.unb.br/cardapio | Aberto, sem login |
| Eventos | noticias.unb.br/agenda | Agenda institucional pública |
| Editais | Portal Público SIGAA (pós-graduação) | Centralizado |
| Complemento | dadosabertos.unb.br (CKAN) | Bom para seed de Unidades/Cursos; Turmas está desatualizado (2022) |

## 3. Requisitos Funcionais - Core

**Disciplinas**
- RF01 - Capturar oferta de disciplinas de todas as unidades (nome, código, turma, horário, vagas), com scraper por unidade e throttling
- RF02 - Associar disciplina a professor
- RF03 - Associar disciplina a sala/prédio

**Professores**
- RF04 - Cadastro de docentes vinculados às disciplinas

**Salas/Prédios**
- RF05 - Localização e identificação de salas e prédios (derivado de RF01)

**Cardápio do RU**
- RF06 - Capturar cardápio diário
- RF07 - Manter histórico de cardápios

**Eventos**
- RF08 - Capturar eventos institucionais (data, local, descrição)

**Editais**
- RF09 - Capturar editais publicados (título, data, link, órgão)

**API pública**
- RF10 - Endpoints REST por domínio
- RF11 - Documentação OpenAPI/Swagger
- RF12 - Versionamento (`/v1/`)
- RF13 - SDK/CLI para integração de terceiros e squads futuros
- RF14 - Portal do desenvolvedor

**Atualização de dados**
- RF15 - Agendamento automático de scraping
- RF16 - Log de sucesso/falha de cada execução

## 4. Features derivadas

Calculadas em cima do que os domínios acima já capturam - baixo esforço extra.

- **RF17 - Salas vazias**: `GET /v1/salas/vazias?dia=segunda&horario=14:00` - cruza Sala com Disciplina no horário pedido. Só reflete aula cadastrada, não reserva informal.
- **RF18 - Agenda do professor**: `GET /v1/professores/{nome}/agenda` - lista as turmas de um docente.
- **RF19 - Cardápio semanal**: `GET /v1/cardapio/semana?data_inicio=...` - agrupa 7 dias de histórico.

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
| RNF08 | CI/CD | Pipeline de integração contínua (lint, testes, cobertura) configurado desde o Release 1 |
| RNF09 | Cobertura de testes | Cobertura mínima de 90% no backend, com testes de integração além dos unitários |

## 6. Equipe

| Pessoa | Área | Responsabilidade | Tecnologias |
|---|---|---|---|
| Vitor | Backend / Scrum Master | Scraping de Disciplinas/Professores/Salas + endpoints; facilitação do squad (rituais, board) | FastAPI, Playwright, SQLAlchemy |
| Ítalo | Backend | Scraping de RU/Eventos/Editais + endpoints | FastAPI, BeautifulSoup, SQLAlchemy |
| Daniel | Frontend | Telas de consulta + portal do dev | Next.js, Axios, Swagger UI |
| Arthur | Infra de jobs | Celery/Redis, cache, rate limit | Celery, Redis, slowapi |
| Gabriel | Banco/Deploy / Product Owner | Modelagem, Docker, deploy, release notes; priorização de backlog e critérios de aceitação | PostgreSQL, SQLAlchemy, Alembic, Docker, Railway |
| João Paulo | QA/Integração | Investigação de fontes, testes de contrato, observabilidade, CI | DevTools, Postman, Pytest, schemathesis, UptimeRobot |

## 7. Requisito → responsável

| Pessoa | Requisitos |
|---|---|
| Vitor | RF01-05, RF17, RF18, RF13 (SDK) |
| Ítalo | RF06-09, RF19, RF13 (CLI) |
| Daniel | RF10, RF11, RF14 |
| Arthur | RF15, RF16, RNF01, RNF02 |
| Gabriel | RF12, RNF06, modelagem, release notes |
| João Paulo | RNF03, RNF04, RNF05, RNF07, RNF08, RNF09 |

## 8. Releases

Estrutura alinhada ao board da disciplina (Projeto 14 - Infraestrutura de Dados).

### Release 1

Dois ou três domínios de dados com scraping agendado e OpenAPI documentada.

- **Vitor**: scraper de Disciplinas (Playwright/SIGAA), associações Disciplina↔Professor↔Sala (RF01-05)
- **Ítalo**: scraper de Cardápio do RU (RF06-07)
- **Daniel**: telas de consulta consumindo os primeiros domínios, protótipos revisados antes da implementação
- **Arthur**: Celery + Redis, agendamento automático dos scrapers, logs de execução (RF15-16)
- **Gabriel**: schema inicial, Docker Compose, rotas já sob `/v1/` (RF12), documentação OpenAPI automática (RF11), release note da R1
- **João Paulo**: investigação das fontes de dado, relatório de risco, pipeline de CI configurado desde já (RNF08), primeiros testes de contrato

### Release 2

Versionamento, cache, rate limit e SDK/CLI - com portal do desenvolvedor.

- **Vitor**: completa os domínios restantes (Professores, Salas), features derivadas RF17 (salas vazias) e RF18 (agenda do professor), SDK Python (RF13)
- **Ítalo**: scrapers de Eventos e Editais (RF08-09), feature derivada RF19 (cardápio semanal), CLI (RF13)
- **Daniel**: portal do desenvolvedor (RF14), telas finais das features derivadas
- **Arthur**: cache (RNF02) e rate limit (RNF01)
- **Gabriel**: deploy em produção, ambiente e variáveis de produção (RNF06), release note da R2
- **João Paulo**: testes de contrato completos (RNF04), observabilidade (RNF03), cobertura de testes 90% (RNF09), checklist final board vs. entrega

## 9. Riscos técnicos

| Risco | Impacto |
|---|---|
| SIGAA em JSF | Exige Playwright, não scraping simples |
| Sem fonte pública de Salas | Resolvido por derivação, sem cadastro próprio |
| Sites mudam sem aviso | Manutenção contínua (RNF05) |
| Todas as unidades da UnB | Throttling e agendamento fora de pico; falha isolada não trava o resto |
