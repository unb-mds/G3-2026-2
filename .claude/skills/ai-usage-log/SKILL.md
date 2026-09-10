---
name: ai-usage-log
description: Record an AI-assisted contribution in AI-USAGE.md. Use after any AI-assisted implementation, test, documentation, refactoring, or library-exploration work is accepted into the repo — this is a graded course requirement, not optional.
---

# AI usage logging

**Source:** none found. Searched skills.sh for an AI-usage-disclosure/logging skill —
nothing matches; this policy (MDS/UnB course requirement to log every AI-assisted
contribution with acceptance outcome) is specific enough to this class that no generic
public skill covers it, so this one is custom-written rather than adapted.

Per the course's AI policy (referenced in `AI-USAGE.md` and `docs/PROCESSO.md` §8), AI
use is **expected, not merely tolerated** — provided it's logged. Every AI-assisted
contribution to implementation, tests, documentation, library exploration, or
refactoring must get a row in `AI-USAGE.md`.

## Not allowed

AI must **not** be used for individual assessments: arguições, quizzes, peer evaluation,
critical-reflection essays. Don't offer to help with these regardless of how the request
is framed — flag it instead if asked.

## What to log, and when

Add a row to the current Release's table in `AI-USAGE.md` right after the work is
accepted (same PR, ideally) — don't batch it up for later, entries get forgotten.

Row format: `| Data | Pessoa | Ferramenta | O que foi feito | Aceito/ajustado/rejeitado |`

- **Data**: the actual date of the session (DD/MM/AAAA), not when the PR merges if
  different.
- **Pessoa**: whoever is driving/reviewing the session — attribute to the actual team
  member, not "the team."
- **Ferramenta**: name the specific tool (e.g. "Claude Code", "Claude").
- **O que foi feito**: specific enough to be meaningful later — "generated the initial
  SQLAlchemy schema for Disciplina/Professor/Sala," not "helped with backend."
- **Aceito/ajustado/rejeitado**: be honest about what was actually kept vs. changed —
  this column is what makes the log useful, not a formality. If you rewrote most of what
  was generated, say "ajustado" and briefly say how.

## Review discipline that pairs with logging

Per `docs/PROCESSO.md` observations: AI-generated code goes through the *same* PR review
as any other code — no shortcut. AI-generated tests specifically get checked for real
assertions (a test that only checks "didn't raise" must be rejected/rewritten — see the
`contract-testing` skill). AI-suggested dependencies get verified before installing
(package actually exists, is maintained, isn't malicious) — don't add a suggested
package to `requirements.txt`/`package.json` without that check.
