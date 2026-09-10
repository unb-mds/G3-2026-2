---
name: scheduled-task
description: Add or change a Celery task in backend/app/tasks/ that schedules a scraper run. Use for RF15 (automatic scheduling) and RF16 (success/failure logging) work.
---

# Scheduled task (Celery + Redis)

**Source:** adapted from the task-queue guidance in
[`sickn33/antigravity-awesome-skills/fastapi-pro`](https://skills.sh/sickn33/antigravity-awesome-skills/fastapi-pro)
("Task queues with Celery or Dramatiq" as part of production-ready async FastAPI
services), narrowed to Celery+Redis specifically since that's the choice already made in
`docs/ARQUITETURA.md` (and a candidate for its own ADR — see the `adr-writing` skill).

`backend/app/tasks/` wires scrapers into Celery jobs, scheduled via Redis (RF15). This
is the *only* place a scraper's success/failure is logged (RF16) — logging is a task
concern, not a scraper concern (see the `web-scraper` skill's resilience rule).

## Rules

- **A task calls a scraper + parser, persists the result, and logs the outcome.** It does
  not contain scraping or parsing logic itself — that stays in
  `app/scrapers/<dominio>/`.
- **Every task run logs success or failure (RF16)**, including *which* unit/source
  failed when scraping multiple units (e.g. one FCTE-Gama failure shouldn't blank out
  the log entry for a run that succeeded on other units). A failed unit should not raise
  and kill the whole task run — see "falha isolada não trava o resto" in "Riscos
  técnicos", `docs/REQUISITOS.md` §9.
- **Schedule outside peak hours** and keep throttling between requests inside the
  scraper (already true of `buscar_html_varias_unidades`) — the task's job is *when*,
  the scraper's job is *how gently*.
- Tasks are idempotent where possible: re-running a task for the same period should
  update existing rows, not duplicate them — this matters for RF07 (cardápio history)
  where old data must be preserved, not overwritten by a naive upsert.
- Retries belong in the task layer (Celery's own retry mechanism), not hand-rolled
  inside the scraper — the scraper's own retry loop (see `_sessao_expirada` handling in
  `DisciplinaScraper.buscar_html`) is for a *specific* transient failure mode
  (SIGAA session expiry) it can detect and recover from directly; broader "the whole run
  failed, try again later" retries are a Celery concern.
