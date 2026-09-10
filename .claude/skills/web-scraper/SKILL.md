---
name: web-scraper
description: Build or modify a scraper for one of Cerradinho's public data sources (SIGAA turmas/cursos, RU cardapio, noticias.unb.br agenda, editais, CKAN). Use when the task involves fetching or parsing HTML/JSON from any source listed in docs/REQUISITOS.md section 2.
---

# Web scraper

**Source:** adapted from [`openai/skills/playwright`](https://www.skills.sh/openai/skills/playwright)
(driving a real browser for JS-rendered sources) and
[`mindrally/skills/web-scraping`](https://www.skills.sh/mindrally/skills/web-scraping)
(static vs. dynamic site decision — `requests`+`BeautifulSoup`+`lxml` for static HTML,
Playwright/Selenium for JS-rendered pages), narrowed to Cerradinho's actual sources and
existing module (`backend/app/scrapers/disciplinas/`).

Cerradinho scrapes public, no-login UnB sources (see `docs/REQUISITOS.md` §2) and stores
normalized data in Postgres; the API never scrapes on request (see "Decisões de
arquitetura" in `docs/ARQUITETURA.md`). Every scraper module lives under
`backend/app/scrapers/<dominio>/` and is split into exactly two files:

- `scraper.py` — talks to the network only. Knows how to navigate/fetch and returns
  **raw HTML/JSON**. Never interprets content.
- `parser.py` — takes raw HTML/JSON in, returns validated Pydantic models (from
  `app/schemas/`) out. Never touches the network.

This mirrors the existing `backend/app/scrapers/disciplinas/` module — use it as the
reference implementation.

## When to use Playwright vs. plain HTTP

This is the static-vs-dynamic decision from the `web-scraping` skill above, applied to
our specific sources:

- SIGAA (`sigaa.unb.br`) is JSF (ViewState/postback-based) — it **requires Playwright**,
  a plain `requests.get` will not work. See RF01 and the "Riscos técnicos" table in
  `docs/REQUISITOS.md`.
- RU cardápio, notícias/agenda, and CKAN are plain HTML/JSON — prefer `httpx`/`requests` +
  `BeautifulSoup`, no browser needed. Only reach for Playwright when the source is
  JS-rendered.

## Rules

- **Scraper never imports parser logic and vice versa's network calls.** If you catch
  yourself parsing inside the scraper class or fetching inside the parser function,
  split it back out.
- **Resilience (RNF05)**: a scraper must fail gracefully if the source changes shape —
  return an empty list / raise a specific, catchable exception, never let an unhandled
  `AttributeError` from a missing selector propagate raw. Log enough to diagnose (see
  RF16 — every run needs a success/failure log, wired through the Celery task in
  `app/tasks/`, not inside the scraper itself).
- **Throttling**: any loop over multiple units/pages must sleep between requests (see
  `atraso_segundos` in `DisciplinaScraper.buscar_html_varias_unidades`) — UnB's servers
  are a shared resource, all units get scraped, so this isn't optional.
- **Document non-obvious source quirks in a module docstring**, the way
  `scrapers/disciplinas/scraper.py` documents the SIGAA ViewState session-warm-up bug and
  the `domcontentloaded` vs `networkidle` choice. Future maintainers need the *why*, not
  just the workaround.
- **Output must be a schema, not a dict.** The parser returns instances of models from
  `app/schemas/` (see the `data-contract` skill) — never raw dicts crossing the module
  boundary into `app/domain/` or the DB layer.
- Scraper classes/functions are named after the domain, not `utils.py`/`scraper_helpers.py`
  (see "Nomenclatura" in `docs/ARQUITETURA.md`).

## Testing

- Parser tests use HTML fixtures under `backend/tests/scrapers/fixtures/`, loaded from
  disk — never hit the live site in a unit test. See
  `backend/tests/scrapers/test_disciplinas_parser.py` as the pattern: assert on real
  extracted fields (codes, names, grouping), not just "didn't crash."
- Scraper (network) code is harder to unit test — keep it thin enough that most logic
  and edge cases live in the parser, which is fully testable offline.
