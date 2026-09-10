---
name: adr-writing
description: Write an Architecture Decision Record. Use whenever a non-trivial architectural choice is made or revisited — a new library, a structural pattern, a technology swap — not for routine implementation details.
---

# ADR (Architecture Decision Record)

**Source:** adapted from
[`wshobson/agents/architecture-decision-records`](https://skills.sh/wshobson/agents/architecture-decision-records)
("Document significant technical decisions with structured context, rationale, and
consequences" — that skill offers five template formats: standard MADR, lightweight,
Y-statement, deprecation, and RFC-style, plus lifecycle states proposed/accepted/
deprecated/superseded). Cerradinho standardizes on one lightweight-MADR-style template
already fixed by `docs/PROCESSO.md` §7 (below) instead of picking a format per decision —
consistency across `docs/adr/` matters more than per-ADR flexibility for a small team.

Per `docs/PROCESSO.md` §7, relevant architecture decisions get their own file under
`docs/adr/`, one file per decision.

## When an ADR is warranted

Examples the team itself flagged: choosing Playwright for the Disciplinas scraper,
the monorepo structure, choosing Celery/Redis for scheduling. As a rule of thumb: if
reversing the decision later would mean non-trivial rework (not just editing one
function), it's ADR-worthy. Routine implementation choices (naming a variable, which
loop construct to use) are not.

## Format (exact template from docs/PROCESSO.md — the project's fixed choice among the
source skill's template options)

```markdown
# ADR 00X — [decision title]

## Status
Aceito / Proposto / Substituído

## Contexto
[Why this decision needed to be made]

## Decisão
[What was decided]

## Alternativas descartadas
[What else was considered and why it wasn't chosen]

## Consequências
[What this decision implies — costs and trade-offs accepted]
```

- Keep the section headers in Portuguese exactly as above — that's the team's
  established format, don't translate them even though this SKILL.md is in English.
- Number ADRs sequentially (`0001-...`, `0002-...`); check `docs/adr/` for the next
  free number before creating one.
- Status starts as `Proposto` unless the decision is already settled and implemented,
  in which case `Aceito`. Use `Substituído` only when superseding an existing ADR — link
  back to the ADR it replaces.
- Write the "Alternativas descartadas" section honestly — it's what makes the ADR useful
  later, not a formality. Include the option actually tempting enough to consider, not a
  strawman.
