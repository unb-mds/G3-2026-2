# Processo — Cerradinho

Como o time trabalha: fluxo de Git, padrões de qualidade e governança do repositório. Requisitos do sistema estão em [`REQUISITOS.md`](REQUISITOS.md).

## 1. Repositório e fluxo de Git

Repositório: [github.com/unb-mds/G3-2026-2](https://github.com/unb-mds/G3-2026-2)

- Monorepo — um único repositório com pastas `/frontend` e `/backend`
- Branches: `main` (estável) → `dev` (integração) → `feature/nome-da-tarefa`
- Commits em Conventional Commits (`feat:`, `fix:`, `docs:`, etc.), com padrão documentado em `docs/padrao_commits.md`
- Organização de tarefas via Issues + board (Projects) do GitHub

## 2. Padrão de Issues e Pull Requests

- Toda issue deve ter critério de aceitação, label de tamanho (S/M/L/XL) e label de tipo (feature, fix, docs, devops)
- Templates em `.github/ISSUE_TEMPLATE/` e `.github/PULL_REQUEST_TEMPLATE.md`
- Todo PR precisa de revisão **formal e registrada** — comentário ou aprovação no próprio PR. Combinar revisão fora do GitHub (chat, verbal) não conta como evidência.

## 3. Ritmo individual esperado

- Atividade constante ao longo do projeto — recomendado pelo menos 3 commits/semana por pessoa — em vez de concentrar contribuição só no fim de cada release
- Presença em planning e retrospectiva de cada sprint, registrada com lista de presença
- Planning e retro devem ser documentados sprint a sprint, sem exceção — inclusive nas últimas sprints do projeto, quando o time costuma relaxar essa prática

## 4. Story Map

Montado diretamente no GitHub Projects, sem ferramenta externa:

1. Criar campos single select `Journey` (jornada do usuário: ex. Consultar Disciplinas, Consultar Cardápio, Consultar Eventos/Editais, Integrar via SDK) e `Step` (etapas dentro de cada jornada)
2. Preencher esses campos em cada issue
3. Usar Milestones como as releases (linhas do mapa)
4. Criar uma view em Board, com Column field = `Step` e Group by = `Milestone` — isso gera a grade do story map a partir das issues já existentes

## 5. Protótipos

Telas de baixa e alta fidelidade (Figma ou similar) devem ser produzidas e revisadas com o time **antes** de o frontend implementar cada tela, não depois. Link do protótipo registrado no README.

## 6. Padrões de projeto open source

- `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md` na raiz do repositório
- Cada Release fechada (Release 1, Release 2) deve ter uma Release Note publicada na aba Releases do GitHub, descrevendo o que foi entregue

## 7. ADR (Architecture Decision Record)

Decisões de arquitetura relevantes ficam registradas individualmente em `docs/adr/`, um arquivo por decisão, formato:

```markdown
# ADR 00X — [título da decisão]

## Status
Aceito / Proposto / Substituído

## Contexto
[Por que essa decisão precisou ser tomada]

## Decisão
[O que foi decidido]

## Alternativas descartadas
[O que também foi considerado e por que não foi escolhido]

## Consequências
[O que essa decisão implica, custos e trade-offs assumidos]
```

Exemplos de decisões que merecem ADR: escolha de Playwright para scraping de Disciplinas, estrutura de monorepo, escolha de Celery/Redis para agendamento.

## 8. Registro de uso de IA

Uso de IA no projeto é documentado em [`AI-USAGE.md`](../AI-USAGE.md), na raiz do repositório. Toda contribuição de IA em implementação, testes, documentação ou refatoração deve ser registrada ali. IA não pode ser usada em avaliações individuais (arguições, ensaio de reflexão crítica).
