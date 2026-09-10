---
name: data-contract
description: Define or change a Pydantic schema in backend/app/schemas/ that represents validated data coming out of a scraper, or a request/response shape for the API. Use when adding a new domain (professores, salas, cardapio, eventos, editais) or field.
---

# Data contract (Pydantic schemas)

**Source:** adapted from the Pydantic v2 validation guidance in
[`mindrally/skills/fastapi-python`](https://www.skills.sh/mindrally/skills/fastapi-python)
("Pydantic v2 validation... for scalable backend development"), scoped down to how this
project actually uses schemas — as the scraper-output contract, not just API I/O.

`backend/app/schemas/` holds Pydantic `BaseModel` classes — the validated contract that
sits between scrapers and the rest of the system (DB layer, API). See the docstring at
the top of `backend/app/schemas/disciplina.py` for the canonical explanation of scope.

## Rules

- **Schemas are intentionally "dumb."** A schema validates shape and type — it does not
  normalize or reconcile data (e.g. matching the same professor spelled two different
  ways across turmas, splitting a free-text room string like "FCTE - I9/I10" into
  building+room). That normalization belongs in `app/domain/`, never in `app/schemas/`.
  Don't add methods or business logic to a schema class beyond validators for shape.
- **One file per domain entity**, named in the singular after the entity (`disciplina.py`,
  not `disciplinas.py`), even when it defines several related models (see `Professor`,
  `Sala`, `Horario`, `Turma` all living in `disciplina.py` because they all revolve
  around the Disciplina domain).
- **Comment the *meaning* of a field when it isn't obvious from the name alone** — e.g.
  `codigo: str  # ex: "6T2345"` — especially for raw strings copied verbatim from a
  scraped source that will need further parsing downstream.
- Field types should reflect what the parser can *actually* extract cleanly. If a field
  is scraped as text with mixed formatting (vagas, e.g.), keep it `str` at this layer
  and let `app/domain/` (or a dedicated normalization step) coerce it to `int` — don't
  bake type coercion that can silently fail into the schema unless you also handle the
  failure explicitly.
- These are the **scraper-output contracts**, distinct from the API request/response
  models that will live under the same `app/schemas/` tree once routers exist (RF10) —
  when both exist, keep scraper-output schemas and API I/O schemas in clearly separate
  modules (e.g. `schemas/disciplina.py` vs `schemas/api/disciplina.py`), don't reuse one
  for both purposes if their shapes diverge.

## When adding a new domain

1. Check `docs/REQUISITOS.md` §2–3 for the fields required by that domain's RF.
2. Model only what the scraper reliably provides; leave derived/cross-domain fields (RF17
   salas vazias, RF18 agenda do professor, RF19 cardápio semanal) out of the schema — those
   are computed in `app/domain/`, not stored as schema fields.
3. Pair the new schema with parser tests (see the `web-scraper` skill) that assert on
   real field values from a fixture.
