# Estudo: Web Scraping

> Material de estudo focado no contexto do projeto **Cerradinho** (API aberta da UnB), onde a responsabilidade é o scraping de **Disciplinas, Professores e Salas** (RF01-05) para alimentar o back-end.

---

## 1. O que é Web Scraping

Web scraping é o processo de extrair dados de páginas web de forma automatizada, transformando conteúdo não estruturado (HTML) em dados estruturados (JSON, tabelas de banco de dados, etc.).

No caso do Cerradinho, o objetivo é ler páginas institucionais da UnB (ex: SIGAA, páginas de departamentos) e transformar essas informações em registros de `Disciplina`, `Professor` e `Sala` no banco de dados.

## 2. Duas abordagens principais

### 2.1 Scraping estático (HTTP + parsing de HTML)
- A página é baixada com uma requisição HTTP simples (ex: `requests`, `httpx`) e o HTML é parseado (ex: `BeautifulSoup`, `lxml`, `selectolax`).
- **Vantagem:** rápido, leve, baixo consumo de recursos.
- **Quando usar:** quando o conteúdo já vem pronto no HTML retornado pelo servidor (não depende de JavaScript para renderizar).

### 2.2 Scraping dinâmico (browser automation)
- Um navegador real (ou headless) é controlado programaticamente para carregar a página, executar JavaScript e só então extrair os dados.
- Ferramentas: **Playwright**, Selenium, Puppeteer.
- **Vantagem:** funciona em páginas que dependem de JS (SPAs, conteúdo carregado via AJAX, formulários dinâmicos).
- **Desvantagem:** mais lento e mais pesado computacionalmente.
- **Por que o Cerradinho usa Playwright:** páginas institucionais como o SIGAA costumam ter navegação por sessão, formulários e conteúdo carregado dinamicamente — cenário típico onde scraping estático não é suficiente.

## 3. Etapas de um pipeline de scraping

1. **Identificação da fonte:** mapear quais páginas/endpoints contêm os dados de Disciplinas, Professores e Salas.
2. **Inspeção da estrutura:** usar DevTools do navegador para entender o HTML, IDs, classes e possíveis APIs internas (Network tab) que a página consome.
3. **Coleta (fetch/navigate):** baixar o HTML ou navegar até a página com o browser automatizado.
4. **Extração (parsing):** localizar os elementos relevantes via seletores (CSS selectors, XPath) e extrair o texto/atributos.
5. **Limpeza e normalização:** remover espaços, converter tipos, padronizar nomes (ex: nome do professor sempre em um mesmo formato).
6. **Associação de dados:** relacionar Disciplina ↔ Professor ↔ Sala (o "core" do RF01-05).
7. **Persistência:** salvar no banco via ORM (SQLAlchemy).
8. **Agendamento/atualização:** decidir com que frequência repetir o processo (dados mudam por semestre).

## 4. Boas práticas técnicas

- **Seletores resilientes:** prefira seletores baseados em atributos semânticos (`data-*`, `id`) a seletores frágeis baseados em posição (`div:nth-child(3)`), que quebram com qualquer mudança de layout.
- **Esperas explícitas, não `sleep` fixo:** em scraping dinâmico, espere por um elemento/estado específico aparecer, em vez de usar `time.sleep(5)` fixo (mais lento e menos confiável).
- **Tratamento de erros e retries:** páginas institucionais podem cair ou responder devagar; implemente retentativas com backoff.
- **Idempotência:** rodar o scraper duas vezes não deve duplicar dados — use upsert (inserir ou atualizar) baseado em uma chave natural (ex: código da disciplina).
- **Rate limiting:** não sobrecarregue o servidor de origem; espace as requisições.
- **Cache local durante desenvolvimento:** salve o HTML baixado localmente enquanto desenvolve o parser, para não ficar refazendo requisições à UnB a cada teste.
- **Separação de responsabilidades:** separe claramente as camadas de:
  - **coleta** (baixar a página),
  - **extração** (parsear o HTML em dados brutos),
  - **transformação/associação** (regras de negócio: ligar disciplina a professor e sala),
  - **persistência** (salvar no banco).

  Isso facilita testes unitários (você pode testar o parser com um HTML salvo, sem precisar acessar a internet).

## 5. Ética e aspectos legais

- **`robots.txt`:** verificar se o domínio define regras de crawling (ainda que não seja juridicamente vinculante em todos os países, é uma boa prática respeitá-lo).
- **Termos de uso:** dados institucionais da própria universidade tendem a ser de uso mais tranquilo em contexto acadêmico, mas vale documentar a origem dos dados.
- **Carga no servidor:** evitar scraping agressivo que possa ser confundido com um ataque (DoS acidental) — importante especialmente em servidores institucionais compartilhados.
- **Dados pessoais:** nomes de professores são dados públicos institucionais, mas evite coletar informações pessoais sensíveis não necessárias ao projeto.

## 6. Testando scrapers

- **Fixtures de HTML:** salve exemplos reais de páginas (anonimizados se necessário) como fixtures para os testes automatizados, evitando dependência de rede nos testes.
- **Testes de regressão de layout:** como sites mudam de estrutura, é útil ter um teste que alerte quando o parser não encontra mais os elementos esperados (falha "ruidosa" em vez de retornar dados vazios silenciosamente).
- **Logs estruturados:** registrar quantos registros foram coletados, quantos falharam, e por quê — essencial para depurar scraping em produção.

## 7. Checklist prático para o RF01-05 (Disciplinas/Professores/Salas)

- [ ] Mapear todas as páginas/fontes de onde vêm Disciplinas, Professores e Salas
- [ ] Definir o modelo de dados (o que é obrigatório, o que é opcional)
- [ ] Escrever o parser de cada entidade isoladamente
- [ ] Definir a lógica de associação (uma disciplina pode ter mais de um professor/turma? mais de uma sala?)
- [ ] Implementar upsert idempotente
- [ ] Adicionar tratamento de erros e logging
- [ ] Escrever testes com HTML de exemplo salvo localmente
- [ ] Documentar a fonte e a frequência de atualização dos dados

## 8. Recursos para aprofundar

- Documentação do Playwright (ver arquivo específico `estudo-playwright.md`)
- MDN Web Docs — seletores CSS
- Artigos sobre "ethical web scraping"
- Documentação do `robots.txt` (Google Search Central)
