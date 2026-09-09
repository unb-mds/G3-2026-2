# Guia Completo de Git e GitHub

## 1. Conceitos Fundamentais

### O que é Git?
Git é um **sistema de controle de versão distribuído**. Ele registra o histórico de mudanças em um projeto, permitindo que várias pessoas trabalhem no mesmo código sem sobrescrever o trabalho umas das outras, e permitindo voltar a qualquer ponto do histórico.

### O que é GitHub?
GitHub é uma **plataforma online** que hospeda repositórios Git na nuvem e adiciona ferramentas de colaboração em cima do Git puro: interface visual, Issues, Pull Requests, Actions (CI/CD), Projects (kanban), Wiki, etc. Git é a ferramenta; GitHub é o serviço que hospeda e potencializa o uso dela.

### Repositório (repo)
É a "pasta" do projeto rastreada pelo Git. Pode existir só localmente (`git init`) ou ser espelhada em um servidor remoto (GitHub, GitLab, etc.).

### Os três "estados" de um arquivo no Git
1. **Working Directory** — os arquivos como estão no seu computador agora.
2. **Staging Area (Index)** — arquivos marcados (`git add`) para entrar no próximo commit.
3. **Repository (histórico)** — arquivos já "gravados" definitivamente por um commit.

```
Working Directory --(git add)--> Staging Area --(git commit)--> Repositório
```

---

## 2. Configuração Inicial

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seuemail@exemplo.com"
git config --global init.defaultBranch main
```

Isso identifica quem fez cada commit e define `main` como nome padrão da branch principal (evitando o antigo `master`).

---

## 3. Criando e Clonando Repositórios

```bash
git init                          # cria um repositório novo do zero, na pasta atual
git clone <url-do-repo>           # copia um repositório existente do GitHub para sua máquina
```

Depois de um `clone`, seu repositório local já vem conectado ao remoto (chamado por padrão de `origin`).

---

## 4. Fluxo Básico do Dia a Dia

```bash
git status                # mostra o que mudou (modificado, novo, staged, etc.)
git add arquivo.py        # adiciona um arquivo específico à staging area
git add .                 # adiciona TODAS as mudanças da pasta atual
git commit -m "mensagem"  # grava as mudanças no histórico com uma mensagem
git push                  # envia os commits locais para o repositório remoto (GitHub)
git pull                  # traz e mescla as mudanças do remoto para o seu local
git log                   # mostra o histórico de commits
git log --oneline --graph # histórico resumido e visual (ótimo pra ver branches)
```

### Boas mensagens de commit
- Use o presente/imperativo: "corrige bug de login" em vez de "corrigido bug de login".
- Seja específico: `git commit -m "corrige cálculo de nota final no relatório"` é melhor que `git commit -m "fix"`.
- Um padrão popular é o **Conventional Commits**: `feat: adiciona tela de login`, `fix: corrige erro 404 na API`, `docs: atualiza README`, `refactor:`, `test:`, `chore:`.

---

## 5. Branches (Ramificações)

### O que é uma branch?
Uma branch é uma **linha independente de desenvolvimento**. Ela permite que você trabalhe em uma funcionalidade nova, correção de bug, ou experimento, sem afetar o código que já está funcionando na branch principal (geralmente `main`).

Pense nela como uma "cópia paralela" do projeto onde você pode mexer livremente; quando terminar, você mescla (`merge`) essas mudanças de volta.

### Por que usar branches?
- Isola trabalho em progresso do código estável.
- Permite que várias pessoas (ou você mesmo, em várias tarefas) trabalhem em paralelo.
- Facilita revisão de código antes de aceitar as mudanças (via Pull Request).
- Se algo der errado, basta descartar a branch — o `main` nunca foi afetado.

### Comandos essenciais

```bash
git branch                     # lista as branches locais
git branch -a                  # lista branches locais e remotas
git branch nome-da-branch      # cria uma nova branch (mas não muda pra ela)
git checkout nome-da-branch    # muda para essa branch
git checkout -b nome-da-branch # cria E já muda para a nova branch (atalho)
git switch nome-da-branch      # forma mais moderna de trocar de branch
git switch -c nome-da-branch   # forma moderna de criar + trocar

git branch -d nome-da-branch   # deleta uma branch já mesclada (local)
git branch -D nome-da-branch   # força a deleção mesmo sem merge
git push origin --delete nome-da-branch  # deleta a branch no remoto (GitHub)
```

### Convenções de nomes de branch (comuns no mercado)
- `feature/nome-da-funcionalidade` ou `feat/login-usuario`
- `fix/nome-do-bug` ou `bugfix/erro-cadastro`
- `hotfix/correcao-urgente-producao`
- `docs/atualiza-readme`
- `chore/configura-lint`

### Merge (mesclar branches)

```bash
git checkout main          # vá para a branch que vai RECEBER as mudanças
git merge feature/login    # traz as mudanças da branch feature/login para dentro da main
```

Se as duas branches mudaram partes diferentes do código, o Git mescla automaticamente. Se mudaram a **mesma linha**, ocorre um **conflito de merge**, e você precisa resolver manualmente (o Git marca no arquivo com `<<<<<<<`, `=======`, `>>>>>>>` onde está o conflito).

### Rebase (alternativa ao merge)

```bash
git checkout feature/login
git rebase main
```

Reaplica os commits da sua branch em cima da versão mais atual da `main`, criando um histórico mais linear (sem "commit de merge"). É poderoso, mas **nunca faça rebase em branches compartilhadas com outras pessoas** sem alinhar antes, pois reescreve o histórico.

### Estratégia de branches mais comum (simplificada)
- `main` — sempre estável, é o que está (ou vai) para produção.
- `develop` (opcional, em times maiores) — integra funcionalidades antes de ir para `main`.
- Branches de `feature/`, `fix/` etc. — criadas a partir da `main` (ou `develop`), e mescladas de volta via Pull Request depois de revisadas.

---

## 6. Trabalhando com o Remoto (GitHub)

```bash
git remote -v                          # mostra os remotos configurados
git remote add origin <url>            # conecta o repo local a um remoto no GitHub
git push -u origin main                # primeiro push, já "linkando" a branch local com a remota
git push origin nome-da-branch         # envia uma branch específica
git fetch                              # baixa as mudanças do remoto SEM mesclar automaticamente
```

**Diferença entre `fetch` e `pull`:** `fetch` só atualiza sua referência do que existe no remoto (você ainda decide o que fazer); `pull` já faz `fetch` + `merge` (ou rebase, se configurado) de uma vez.

---

## 7. Pull Requests (PRs)

Um **Pull Request** é uma solicitação, feita no GitHub, para mesclar as mudanças de uma branch em outra (normalmente da sua branch de feature para a `main`). É o coração da colaboração no GitHub.

### Fluxo típico
1. Você cria uma branch (`git checkout -b feature/nova-tela`).
2. Faz commits com suas mudanças.
3. Dá `git push origin feature/nova-tela`.
4. No GitHub, clica em "Compare & pull request".
5. Escreve um título e uma descrição explicando **o que** mudou e **por quê**.
6. Outras pessoas do time revisam o código (comentam, pedem ajustes, aprovam).
7. Depois de aprovado (e passando nos testes automáticos, se houver), o PR é mesclado (`Merge`, `Squash and merge`, ou `Rebase and merge`) na branch principal.
8. A branch de feature geralmente é deletada depois do merge.

### Boas práticas em PRs
- PRs pequenos e focados são mais fáceis de revisar do que um PR gigante com 50 arquivos.
- Descreva o contexto: o que motivou a mudança, como testar, se resolve alguma issue.
- Vincule a issue relacionada escrevendo `Closes #12` ou `Fixes #12` na descrição — o GitHub fecha a issue automaticamente quando o PR é mesclado.
- Peça revisão de pelo menos uma outra pessoa antes de mesclar, quando possível.

---

## 8. Issues

Uma **Issue** é um item de rastreamento no GitHub: pode ser um bug, uma tarefa, uma ideia de melhoria, uma pergunta. É a forma organizada de dizer "isso precisa ser feito ou resolvido".

### Para que servem
- Reportar bugs.
- Planejar funcionalidades futuras.
- Dividir um projeto grande em tarefas menores.
- Discutir decisões técnicas antes de codar.
- Servir de "checklist" do projeto (muito usado em trabalhos em grupo/faculdade também).

### Elementos de uma boa issue
- **Título claro**: "Botão de login não funciona no Firefox" é melhor que "bug".
- **Descrição**: o que está acontecendo, o que era esperado, passos para reproduzir (no caso de bug).
- **Labels (etiquetas)**: `bug`, `enhancement`, `documentation`, `good first issue`, `help wanted`, etc. — ajudam a filtrar e priorizar.
- **Assignees**: quem é responsável por resolver.
- **Milestone**: agrupa issues relacionadas a uma entrega/versão específica.
- **Projects**: quadros estilo Kanban (To do / In progress / Done) que organizam issues e PRs visualmente.

### Vinculando issues a commits e PRs
Ao escrever numa mensagem de commit ou descrição de PR:
```
Fixes #23
Closes #45
Resolves #12
```
o GitHub cria um link automático e fecha a issue quando aquele commit/PR chega na branch principal.

---

## 9. Situações Comuns (e como resolver)

### "Fiz commit na branch errada"
```bash
git branch nome-nova-branch     # cria uma branch no ponto atual (com o commit)
git reset --hard HEAD~1         # volta a branch atual 1 commit, "descartando" o commit dela
git switch nome-nova-branch     # vá para a branch nova, que já tem o commit
```

### "Quero desfazer o último commit, mas manter as alterações"
```bash
git reset --soft HEAD~1
```

### "Quero descartar TODAS as mudanças não commitadas"
```bash
git checkout -- .
# ou, versão moderna:
git restore .
```

### "Preciso guardar mudanças temporariamente sem commitar"
```bash
git stash          # guarda as mudanças de lado e limpa o working directory
git stash pop       # traz de volta as últimas mudanças guardadas
git stash list      # lista tudo que está guardado
```

### Conflito de merge
1. O Git avisa quais arquivos têm conflito.
2. Abra o arquivo, procure os marcadores `<<<<<<<`, `=======`, `>>>>>>>`.
3. Edite manualmente para deixar o código como deveria ficar, removendo os marcadores.
4. `git add arquivo-resolvido`
5. `git commit` (finaliza o merge).

### `.gitignore`
Arquivo que diz ao Git quais arquivos/pastas **não** devem ser rastreados (ex: `node_modules/`, `.env`, `__pycache__/`, arquivos de build). Evita subir lixo ou dados sensíveis para o repositório.

---

## 10. Comandos Mais Usados — Resumo Rápido

| Comando | O que faz |
|---|---|
| `git init` | Cria um repositório novo |
| `git clone <url>` | Copia um repositório remoto |
| `git status` | Mostra o estado atual dos arquivos |
| `git add <arquivo>` / `git add .` | Adiciona mudanças à staging area |
| `git commit -m "msg"` | Grava as mudanças no histórico |
| `git push` | Envia commits locais para o remoto |
| `git pull` | Traz e mescla mudanças do remoto |
| `git branch` | Lista/gerencia branches |
| `git checkout -b <branch>` / `git switch -c <branch>` | Cria e muda de branch |
| `git merge <branch>` | Mescla uma branch na atual |
| `git log --oneline --graph` | Histórico visual |
| `git diff` | Mostra as diferenças ainda não commitadas |
| `git stash` | Guarda mudanças temporariamente |
| `git reset` | Desfaz commits (com cuidado) |
| `git revert <commit>` | Cria um novo commit que desfaz um commit anterior (seguro para histórico compartilhado) |

---

## 11. Fluxo Resumido de Trabalho em Time (o "combo" tudo junto)

```bash
git checkout main
git pull                              # garante que está atualizado
git checkout -b feature/minha-tarefa  # cria branch pra sua tarefa
# ... faz as alterações no código ...
git add .
git commit -m "feat: implementa X"
git push -u origin feature/minha-tarefa
# vai no GitHub, abre um Pull Request, vincula a issue relacionada (Closes #N)
# time revisa, aprova
# merge do PR
git checkout main
git pull                              # traz o merge pra sua main local
git branch -d feature/minha-tarefa    # limpa a branch local que já foi usada
```

---

## 12. Dicas Finais
- Commite com frequência e em pedaços pequenos e lógicos — facilita entender o histórico e reverter algo específico se precisar.
- Nunca dê `git push --force` numa branch compartilhada sem avisar o time (ele reescreve o histórico remoto e pode sumir com commits de outras pessoas).
- Use Issues desde o início do projeto para organizar tarefas, mesmo em projetos pequenos ou acadêmicos — ajuda demais a não perder o controle do que falta fazer.
- README.md bem escrito (o que é o projeto, como rodar, como contribuir) facilita muito a vida de quem chega depois.
