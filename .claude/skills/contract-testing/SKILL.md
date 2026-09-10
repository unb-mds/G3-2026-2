---
name: contract-testing
description: Write or run tests for the backend — pytest unit tests for parsers/domain logic, or schemathesis contract tests against the FastAPI OpenAPI schema. Use for RNF04 and RNF09 work, or whenever adding a test alongside a feature.
---

# Contract & unit testing

**Source:** adapted from
[`secondsky/claude-skills/api-testing`](https://www.skills.sh/secondsky/claude-skills/api-testing)
(FastAPI testing with pytest + `TestClient`) and
[`manutej/luxor-claude-marketplace/pytest-patterns`](https://skills.sh/manutej/luxor-claude-marketplace/pytest-patterns)
(fixtures, parametrization, mocking, coverage). No dedicated `schemathesis` skill exists
on skills.sh at the time of writing — that tool choice is project-specific (RNF04, see
`docs/estudos/estudo-schemathesis.md`), layered on top of the generic API-testing
pattern rather than replacing it.

Backend tests live in `backend/tests/`, run with `pytest` from the project venv
(`backend/venv`). See `docs/estudos/estudo-pytest-mocking.md` and
`docs/estudos/estudo-schemathesis.md` for the team's own research notes on these tools.

## Unit tests (parsers, domain logic)

- Mirror the source tree: `backend/tests/scrapers/test_disciplinas_parser.py` tests
  `backend/app/scrapers/disciplinas/parser.py`.
- Use on-disk HTML/JSON fixtures (`backend/tests/scrapers/fixtures/`) — never hit a live
  external source from a test.
- **Assert on actual extracted values**, not just "no exception was raised." Per
  `AI-USAGE.md`'s own review note: an AI-generated test that only checks "didn't throw"
  must be rejected/rewritten before merge, whether AI-authored or not.
- Coverage target for the domain module is ≥70% (RNF09) — when adding domain logic
  (salas vazias, professor-name normalization, etc.), add the test in the same PR, not
  as follow-up debt.

## Contract tests (schemathesis, RNF04)

- Once routers exist under `/v1/`, `schemathesis` generates tests directly from the
  FastAPI OpenAPI schema — don't hand-write schema-shape assertions that duplicate what
  schemathesis already covers for free (see "Preferir bibliotecas prontas" in
  `docs/ARQUITETURA.md`).
- The point of RNF04 is that the API **cannot silently break its documented contract**.
  A route change that alters response shape needs the contract test suite re-run before
  merge, and any intentional break needs a version discussion (RF12), not a quiet edit.

## Mutation & sabotage testing (RNF09)

- Critical modules (scrapers/parsers feeding the DB, domain logic like salas vazias)
  need mutation-score ≥50% and 100% sabotage-test coverage. When a module qualifies as
  "critical," don't just add a happy-path test — add a test that would fail if the logic
  were subtly wrong (off-by-one, wrong comparison operator, swapped field), not just one
  that would fail if the function crashed outright.

## Running tests

```bash
cd backend && source venv/bin/activate && pytest
```
