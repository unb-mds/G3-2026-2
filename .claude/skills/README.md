# Cerradinho — project skills

Skills used by Claude Code agents working in this repo. Per team decision, each skill is
**adapted from an existing public skill** (mainly from [skills.sh](https://www.skills.sh/))
rather than invented from scratch, scoped down to Cerradinho's actual stack and the
conventions in `docs/REQUISITOS.md`, `docs/ARQUITETURA.md`, and `docs/PROCESSO.md`. Each
`SKILL.md` opens with a **Source** line naming what it's adapted from. Only one skill
(`ai-usage-log`) is fully custom — no public skill covers this course's specific AI
disclosure policy. This file is plain documentation, not a skill itself.

## Backend — data pipeline

| Skill | Source | Covers |
|---|---|---|
| [web-scraper](web-scraper/SKILL.md) | [openai/skills/playwright](https://www.skills.sh/openai/skills/playwright), [mindrally/skills/web-scraping](https://www.skills.sh/mindrally/skills/web-scraping) | Scraper/parser split for any public source (SIGAA, RU, agenda, editais, CKAN) |
| [data-contract](data-contract/SKILL.md) | [mindrally/skills/fastapi-python](https://www.skills.sh/mindrally/skills/fastapi-python) | Pydantic schemas in `app/schemas/` — scraper-output and API contracts |
| [db-model](db-model/SKILL.md) | [sickn33/antigravity-awesome-skills/database-architect](https://skills.sh/sickn33/antigravity-awesome-skills/database-architect) | SQLAlchemy models + Alembic migrations |
| [scheduled-task](scheduled-task/SKILL.md) | [sickn33/antigravity-awesome-skills/fastapi-pro](https://skills.sh/sickn33/antigravity-awesome-skills/fastapi-pro) | Celery/Redis jobs, RF15-16 (scheduling + run logging) |

## Backend — API & clients

| Skill | Source | Covers |
|---|---|---|
| [fastapi-endpoint](fastapi-endpoint/SKILL.md) | [wshobson/agents/fastapi-templates](https://skills.sh/wshobson/agents/fastapi-templates) | `/v1/` routers, versioning, OpenAPI docs |
| [sdk-cli](sdk-cli/SKILL.md) | [speakeasy-api/skills/start-new-sdk-project](https://skills.sh/speakeasy-api/skills/start-new-sdk-project), [sickn33/antigravity-awesome-skills/python-development-python-scaffold](https://skills.sh/sickn33/antigravity-awesome-skills/python-development-python-scaffold) | `sdk/` installable Python client/CLI (RF13) |
| [frontend-data-hook](frontend-data-hook/SKILL.md) | [hieutrtr/ai1-skills/react-frontend-expert](https://skills.sh/hieutrtr/ai1-skills/react-frontend-expert) | Next.js API-calling hooks (`frontend/hooks/`) |

## Quality

| Skill | Source | Covers |
|---|---|---|
| [contract-testing](contract-testing/SKILL.md) | [secondsky/claude-skills/api-testing](https://www.skills.sh/secondsky/claude-skills/api-testing), [manutej/luxor-claude-marketplace/pytest-patterns](https://skills.sh/manutej/luxor-claude-marketplace/pytest-patterns) | pytest unit tests + schemathesis contract tests (RNF04, RNF09) |

## Process & governance

| Skill | Source | Covers |
|---|---|---|
| [git-workflow](git-workflow/SKILL.md) | [github/awesome-copilot/git-commit](https://www.skills.sh/github/awesome-copilot/git-commit), [gentleman-programming/gentleman-skills/github-pr](https://skills.sh/gentleman-programming/gentleman-skills/github-pr) | Branching, Conventional Commits, issue/PR policy |
| [adr-writing](adr-writing/SKILL.md) | [wshobson/agents/architecture-decision-records](https://skills.sh/wshobson/agents/architecture-decision-records) | Architecture Decision Records under `docs/adr/` |
| [ai-usage-log](ai-usage-log/SKILL.md) | *(none — custom)* | Logging AI-assisted contributions in `AI-USAGE.md` (course requirement) |

## Not yet a skill (add when the work starts)

Rate limiting (`slowapi`, RNF01), Redis caching (RNF02), and observability/uptime
monitoring (RNF03) don't have dedicated modules yet. When that work starts, check
skills.sh first (a `slowapi`/rate-limiting or observability skill likely already exists)
before writing a project-specific one from scratch.
