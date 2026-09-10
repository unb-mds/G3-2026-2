---
name: db-model
description: Add or change a SQLAlchemy model in backend/app/models/ or an Alembic migration. Use when persisting a new domain (disciplina, professor, sala, cardapio, evento, edital) or altering an existing table.
---

# Database model & migration

**Source:** adapted from
[`sickn33/antigravity-awesome-skills/database-architect`](https://skills.sh/sickn33/antigravity-awesome-skills/database-architect)
(ORM selection — SQLAlchemy vs. Django ORM vs. Prisma — schema design, migration tools
including Alembic, connection management), narrowed to the SQLAlchemy+Alembic+Postgres
stack this project already committed to in `docs/ARQUITETURA.md`.

`backend/app/models/` holds SQLAlchemy models — the persisted, normalized shape of each
domain from `docs/REQUISITOS.md` §2–3. Migrations live in `backend/alembic/`.

## Rules

- **Models are not schemas.** `app/schemas/` (Pydantic) is what a scraper produces or an
  API request/response carries; `app/models/` (SQLAlchemy) is what's actually stored.
  They diverge on purpose — e.g. a schema's free-text `Sala.descricao` string may become
  a normalized `predio` + `sala` pair of columns once it passes through `app/domain/`
  normalization. Don't collapse the two layers to save a file.
- **Every schema change needs an Alembic migration in the same PR** — never hand-edit
  the DB shape without a migration, and never let the model drift from what's actually
  migrated.
- **Queries don't live loose in routers or scrapers.** Reads/writes go through the model
  layer (a repository function or the model class itself), so routers stay thin (see the
  `fastapi-endpoint` skill) and scrapers stay network-only (see the `web-scraper`
  skill).
- Salas/Prédios (RF05) have **no scraper of their own** — they're derived as a
  by-product of the Disciplinas scraper. Model this as a relationship/foreign key from
  Turma, not a separately-scraped, separately-synced table.
- Name models after the domain entity (`Disciplina`, `Turma`, `Professor`, `Sala`), not
  generic names — consistent with "Nomenclatura" in `docs/ARQUITETURA.md`.

## Before writing a migration

Check `docs/REQUISITOS.md` for the RF that motivates the field, and check whether the
same normalization already needs to happen elsewhere (e.g. professor name reconciliation
across turmas) — that logic should exist once, in `app/domain/`, not be duplicated
between the migration's constraints and a scraper/parser.
