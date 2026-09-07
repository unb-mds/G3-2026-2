# Sprint Planning — Cerradinho (API Aberta da UnB)
**Disciplina:** MDS — UnB FCTE
**Scrum Master:** Vitor | **Product Owner:** Gabriel

---

## 1. Premissas do planejamento

- Cadência de sprint: **1 semana**.
- Cerimônias fixas do time: **segunda-feira** (após a aula) e **quinta-feira, 19h**, além de reuniões emergenciais e resoluções pontuais por mensagem quando necessário.
  - Toda **segunda-feira**: Daily de alinhamento. No início de cada sprint, também serve de **Sprint Planning** do ciclo; no fim de cada sprint, também serve de **Sprint Review** (demo rápida do incremento) + **Retrospectiva** curta.
  - Toda **quinta-feira (19h)**: Daily técnica — bloqueios e dependências entre backend, infra, banco e QA.
- Release 1 = **Sprints 1 a 6** (6 semanas). Release 2 = **Sprints 7 a 12** (6 semanas). Total: 12 semanas.
- Definition of Done (DoD) do time, válida para toda tarefa de código:
  1. Código revisado (PR aprovado por pelo menos 1 outro membro)
  2. Testes unitários (e de integração quando aplicável) passando
  3. Lint sem erros (CI verde)
  4. Documentação/OpenAPI atualizada quando a tarefa expõe/altera endpoint
  5. Sem lógica de negócio duplicada entre scraper/router (ver `ARQUITETURA.md`)

---

## 2. Visão macro: Release 1 x Release 2

| | Release 1 (Sprints 1-6) | Release 2 (Sprints 7-12) |
|---|---|---|
| **Escopo de dados** | Disciplinas + RU (2 domínios) | + Professores, Salas, Eventos, Editais (5 domínios completos) |
| **Infra** | Celery+Redis, scheduling, logs (RF15-16), Docker Compose, CI (RNF08) | Cache (RNF02), Rate limit (RNF01), deploy produção (RNF06) |
| **API** | `/v1/`, OpenAPI automática (RF11-12) | Portal do dev (RF14), SDK Python + CLI (RF13) |
| **Features derivadas** | — | Salas vazias (RF17), Agenda do professor (RF18), Cardápio semanal (RF19) |
| **Qualidade** | CI configurado, 1ºs testes de contrato | Contrato completo (RNF04), observabilidade (RNF03), cobertura 90% (RNF09) |
| **Entrega** | Release note R1 | Release note R2, checklist board vs. entrega |

---

## 3. RELEASE 1 (Sprints 1–6)

### Sprint 1 — Investigação e estrutura base

**Objetivo:** repositório e ambiente organizados, fontes de dado mapeadas, primeiro rascunho de schema.

| Pessoa | Tarefas |
|---|---|
| **Vitor** | Investigar estrutura do SIGAA público (`sigaa.unb.br/sigaa/public/turmas`) — mapear ViewState/postback do JSF; rascunho do contrato de dados de Disciplina/Professor/Sala |
| **Ítalo** | Investigar `ru.unb.br/cardapio` (estrutura HTML, frequência de atualização) |
| **Daniel** | Setup do projeto Next.js (estrutura de pastas, roteamento, Axios configurado) |
| **Arthur** | Setup Celery + Redis localmente via docker; validar comunicação básica entre eles |
| **Gabriel** | Diagrama ER inicial (Disciplina, Professor, Sala, Cardápio); `docker-compose.yml` inicial (Postgres); estrutura do monorepo conforme `ARQUITETURA.md` |
| **João Paulo** | Levantamento de risco das fontes (mudanças possíveis, rate limit, robots.txt); esqueleto do pipeline de CI (lint + testes) no repositório |

**Dependência-chave:** Gabriel entrega a estrutura do monorepo cedo para os demais já codarem no padrão certo.

---

### Sprint 2 — Provas de conceito

**Objetivo:** primeira prova de que dá pra extrair dado real de cada fonte, ambiente de infra rodando.

| Pessoa | Tarefas |
|---|---|
| **Vitor** | PoC de scraping com Playwright para 1 unidade do SIGAA (navegação + extração básica) |
| **Ítalo** | PoC de scraping com BeautifulSoup para 1 dia de cardápio do RU |
| **Daniel** | Wireframes/protótipos das telas de consulta, revisados com o time antes de implementar |
| **Arthur** | PoC de uma task Celery agendada simples (sem lógica de scraping real ainda) |
| **Gabriel** | Revisar schema inicial com Vitor e Ítalo à luz do que as PoCs encontraram |
| **João Paulo** | CI rodando de fato (lint + testes) a cada push; relatório de risco atualizado com achados das PoCs |

---

### Sprint 3 — Scraper de Disciplinas e de RU (dado real)

**Objetivo:** scraping real dos dois primeiros domínios, gravando no banco.

| Pessoa | Tarefas |
|---|---|
| **Vitor** | Scraper de Disciplinas com Playwright para todas as unidades (RF01), com throttling; persistência via SQLAlchemy |
| **Ítalo** | Scraper de Cardápio do RU completo (RF06); persistência via SQLAlchemy |
| **Daniel** | Isolar chamadas de API em hooks/serviços (`services/`), preparando consumo real |
| **Arthur** | Estrutura de log de execução (sucesso/falha) — base do RF16 |
| **Gabriel** | Migrations com Alembic para as tabelas de Disciplina/Professor/Sala/Cardápio |
| **João Paulo** | Primeiros testes de contrato (schemathesis) sobre o schema Pydantic dos dois domínios |

**Dependência-chave:** Vitor e Ítalo dependem do schema/migrations do Gabriel.

---

### Sprint 4 — Associações e agendamento

**Objetivo:** dados relacionados corretamente, scraping passa a rodar agendado (não manual).

| Pessoa | Tarefas |
|---|---|
| **Vitor** | Associar disciplina a professor (RF02) e a sala/prédio (RF03), extraídos no mesmo scraper |
| **Ítalo** | Modelagem e gravação de histórico de cardápio (RF07) |
| **Daniel** | Primeira tela de consulta (lista de disciplinas) consumindo endpoint local |
| **Arthur** | Task Celery real disparando o scraper de Disciplinas e o de RU em agendamento configurável (RF15) |
| **Gabriel** | Ajustes de schema conforme dado real capturado pelos scrapers |
| **João Paulo** | Expandir testes de contrato; validar que o agendamento do Arthur não quebra o schema esperado |

---

### Sprint 5 — API pública dos dois domínios

**Objetivo:** endpoints REST sob `/v1/` documentados via OpenAPI.

| Pessoa | Tarefas |
|---|---|
| **Vitor** | Endpoints REST de Disciplinas/Professores/Salas sob `/v1/` |
| **Ítalo** | Endpoint de Cardápio (`/v1/cardapio`) |
| **Daniel** | Telas de consulta consumindo os endpoints reais (Disciplinas + Cardápio) |
| **Arthur** | Log de sucesso/falha completo e consultável (RF16) |
| **Gabriel** | Garantir que todas as rotas nascem sob `/v1/` (RF12); habilitar geração automática de OpenAPI/Swagger (RF11) |
| **João Paulo** | Testes de contrato cobrindo os novos endpoints; checar viabilidade de observabilidade básica (UptimeRobot) |

---

### Sprint 6 — Fechamento da Release 1

**Objetivo:** consolidar, testar e publicar a primeira entrega.

| Pessoa | Tarefas |
|---|---|
| **Vitor** | Ajustes finos de associação Disciplina↔Professor↔Sala; revisão de código dos endpoints |
| **Ítalo** | Revisão final do domínio de Cardápio (RF06-07) |
| **Daniel** | Ajustes de UX pós-feedback do time nas telas de consulta |
| **Arthur** | Garantir que agendamento e logs rodam de forma estável (sem falhas silenciosas) |
| **Gabriel** | Escrever e publicar a **release note da R1** |
| **João Paulo** | Checklist de saída da R1; testes de contrato consolidados; observabilidade básica ligada |

**Marco:** ✅ Release 1 entregue — 2 domínios (Disciplinas, RU) com scraping agendado e OpenAPI documentada.

---

## 4. RELEASE 2 (Sprints 7–12)

### Sprint 7 — Início dos domínios restantes

**Objetivo:** começar Eventos/Editais e refinar Professores/Salas; planejar features derivadas.

| Pessoa | Tarefas |
|---|---|
| **Vitor** | Refino de RF04 (cadastro robusto de docentes) e RF05 (localização/identificação completa de salas/prédios) |
| **Ítalo** | Scraper de Eventos institucionais (RF08) |
| **Daniel** | Wireframe do portal do desenvolvedor (RF14) |
| **Arthur** | Design da camada de cache Redis (RNF02) — quais endpoints cachear e por quanto tempo |
| **Gabriel** | Preparar variáveis e secrets do ambiente de produção (Railway) |
| **João Paulo** | Expandir testes de contrato para os domínios que estão entrando; medir cobertura atual do backend |

---

### Sprint 8 — Editais e primeira feature derivada

**Objetivo:** scraper de Editais no ar; iniciar lógica de salas vazias e cache real.

| Pessoa | Tarefas |
|---|---|
| **Vitor** | Iniciar lógica de RF17 (salas vazias) na camada de domínio/serviço |
| **Ítalo** | Scraper de Editais (RF09) |
| **Daniel** | Integrar Swagger UI ao início do portal do desenvolvedor |
| **Arthur** | Implementação real do cache Redis (RNF02) para os endpoints mais consultados |
| **Gabriel** | Validar ambiente de produção com deploy de teste |
| **João Paulo** | Testes de contrato dos novos domínios (Eventos/Editais) |

---

### Sprint 9 — Features derivadas e início de SDK/CLI

**Objetivo:** salas vazias e agenda do professor prontos; SDK e CLI iniciados.

| Pessoa | Tarefas |
|---|---|
| **Vitor** | Finalizar RF17 (`GET /v1/salas/vazias`); finalizar RF18 (`GET /v1/professores/{nome}/agenda`) |
| **Ítalo** | Iniciar RF19 (`GET /v1/cardapio/semana`) |
| **Daniel** | Telas para as primeiras features derivadas (salas vazias, agenda do professor) |
| **Arthur** | Iniciar rate limit com slowapi (RNF01) |
| **Gabriel** | Deploy de uma versão candidata em produção |
| **João Paulo** | Observabilidade (RNF03) — configurar UptimeRobot em produção |

---

### Sprint 10 — SDK, CLI e cardápio semanal

**Objetivo:** RF19 pronto; SDK e CLI em estado utilizável; rate limit e cache finalizados.

| Pessoa | Tarefas |
|---|---|
| **Vitor** | Iniciar SDK Python (RF13) cobrindo Disciplinas/Professores/Salas |
| **Ítalo** | Finalizar RF19 (cardápio semanal); iniciar CLI (RF13, via Typer) |
| **Daniel** | Telas para cardápio semanal; continuar portal do desenvolvedor |
| **Arthur** | Finalizar rate limit (RNF01) e cache (RNF02) para os domínios completos |
| **Gabriel** | Ajustar variáveis de ambiente de produção conforme testes do Arthur/Gabriel |
| **João Paulo** | Cobertura de testes avançando em direção aos 90% (RNF09) |

**Dependência-chave:** rate limit/cache do Arthur não deve quebrar os testes de contrato do João Paulo — alinhar antes de mergear.

---

### Sprint 11 — Consolidação de SDK/CLI e portal do dev

**Objetivo:** SDK e CLI quase prontos, portal do desenvolvedor completo, testes sob carga.

| Pessoa | Tarefas |
|---|---|
| **Vitor** | Fechar e documentar o SDK Python (RF13) |
| **Ítalo** | Fechar a CLI (RF13) |
| **Daniel** | Finalizar o portal do desenvolvedor (RF14) |
| **Arthur** | Validação de rate limit e cache sob carga (teste simples de stress) |
| **Gabriel** | Ajustes finais antes do deploy definitivo |
| **João Paulo** | Testes de contrato quase completos (RNF04); cobertura próxima de 90% |

---

### Sprint 12 — Fechamento da Release 2

**Objetivo:** tudo em produção, documentação e qualidade fechadas.

| Pessoa | Tarefas |
|---|---|
| **Vitor** | Revisão final de RF01-05, RF17, RF18 |
| **Ítalo** | Revisão final de RF06-09, RF19 |
| **Daniel** | Polimento visual final das telas e do portal do desenvolvedor |
| **Arthur** | Confirmar estabilidade de cache e rate limit em produção |
| **Gabriel** | Deploy final em produção (RNF06); escrever e publicar a **release note da R2** |
| **João Paulo** | Testes de contrato completos (RNF04); confirmar cobertura mínima de 90% (RNF09); checklist final board vs. entrega |

**Marco:** ✅ Release 2 entregue — 5 domínios completos, features derivadas, versionamento, cache, rate limit, SDK/CLI, portal do desenvolvedor, produção estável.

---

## 5. Riscos a monitorar sprint a sprint

| Risco | Sprints mais críticos | Mitigação |
|---|---|---|
| SIGAA em JSF (ViewState/postback) pode mudar sem aviso | Sprints 1-3 | PoC cedo (Sprint 2) antes de comprometer prazo; scraper deve falhar de forma graciosa (RNF05) |
| Ausência de fonte própria para Salas | Sprint 3-4 | Já mitigado por design: dado derivado do scraper de Disciplinas |
| Acúmulo de dívida técnica em cobertura de teste | Sprints 7-12 | João Paulo mede cobertura desde o Sprint 7, não só no fechamento |
| Cache/rate limit introduzindo regressão na API | Sprints 8-10 | Rodar suíte de contrato do João Paulo antes de mergear mudanças do Arthur |

---

*Documento gerado a partir de `REQUISITOS.md` e `ARQUITETURA.md`. Ajustar datas exatas de cada sprint conforme o calendário oficial da disciplina assim que definido.*