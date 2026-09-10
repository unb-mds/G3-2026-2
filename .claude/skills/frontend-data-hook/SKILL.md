---
name: frontend-data-hook
description: Add or change how the Next.js frontend (frontend/) calls Cerradinho's API. Use for anything under frontend/hooks, or when a component needs new data from the backend.
---

# Frontend data hook

**Source:** adapted from
[`hieutrtr/ai1-skills/react-frontend-expert`](https://skills.sh/hieutrtr/ai1-skills/react-frontend-expert)
("data fetching logic... shared through custom hooks", TanStack Query for query-key
management) — see also
[`jezweb/claude-skills/tanstack-query`](https://skills.sh/jezweb/claude-skills/tanstack-query)
for the `useQuery`/`useMutation` patterns if the team adopts TanStack Query for caching;
until then, hooks can wrap plain `fetch`/`axios` as long as the isolation rule below
holds.

The Next.js frontend consumes the `/v1/` API for query screens and the developer portal
(Daniel's area, `docs/REQUISITOS.md` §6). Structure per `docs/ARQUITETURA.md`:

```
frontend/
├── app/           # pages
├── components/    # visual components
└── hooks/         # API-calling logic, isolated from components
```

## Rules

- **API calls live in `frontend/hooks/`, never inline inside a component.** A component
  calls a hook (`useDisciplinas()`, `useCardapioSemana()`, etc.) and renders what it
  gets back — it does not construct the fetch/axios call itself. This is the explicit
  rule in "Separação de responsabilidades" in `docs/ARQUITETURA.md`.
- Name hooks after the domain/query they perform (`useSalasVazias`, not
  `useApi`/`useFetch` as a generic catch-all) — same "Nomenclatura" rule as the backend.
- **Prototype before implementing a new screen.** Per `docs/PROCESSO.md` §5, low/high-fi
  mockups must be produced and reviewed with the team *before* the frontend builds a new
  screen, not after. If no prototype/link exists for the screen you're about to build,
  flag it rather than building ahead of the review.
- The frontend reads from `/v1/` like any other consumer — it has no special/private API
  surface, and it never talks to the DB or scrapers directly.
