# Estudo: Playwright

> Contexto: no Cerradinho, o Playwright é a ferramenta usada para o scraping de páginas institucionais da UnB (Disciplinas, Professores, Salas — RF01-05), possivelmente páginas que dependem de sessão/JavaScript (ex: SIGAA).

---

## 1. O que é e por que usar aqui

Playwright é uma biblioteca de automação de navegador (criada pela Microsoft) que permite controlar Chromium, Firefox e WebKit programaticamente. Diferente de um cliente HTTP simples, ele **renderiza a página de verdade**, incluindo JavaScript, o que é necessário quando:
- o conteúdo é carregado via requisições AJAX após o carregamento inicial;
- é preciso fazer login / manter sessão para acessar a página (comum em sistemas como o SIGAA);
- há interações necessárias (clicar em um menu, selecionar um filtro) antes do dado aparecer.

Comparado ao Selenium, o Playwright costuma ser mais rápido, tem uma API mais moderna (assíncrona nativa em Python) e mecanismos de espera mais inteligentes por padrão.

## 2. Instalação básica

```bash
pip install playwright
playwright install  # baixa os binários dos navegadores
```

## 3. API síncrona vs assíncrona

Como o resto do projeto usa FastAPI (assíncrono), faz sentido usar a **API assíncrona** do Playwright para integrar naturalmente com `async def`.

```python
import asyncio
from playwright.async_api import async_playwright

async def scrape_disciplinas():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://sigaa.unb.br/...")
        conteudo = await page.content()
        await browser.close()
        return conteudo

asyncio.run(scrape_disciplinas())
```

- `headless=True`: roda sem abrir janela visível — necessário em servidor/CI.
- Durante o desenvolvimento, use `headless=False` para **ver** o navegador agindo e depurar visualmente.

## 4. Navegação e espera (o ponto mais importante)

Playwright tem "auto-waiting" embutido: a maioria das ações espera automaticamente o elemento estar visível/interagível antes de agir. Ainda assim, para dados que carregam dinamicamente, controle a espera explicitamente:

```python
await page.goto("https://exemplo.unb.br/disciplinas")
await page.wait_for_selector("table.disciplinas")  # espera a tabela aparecer
await page.wait_for_load_state("networkidle")  # espera a rede "acalmar"
```

Evite `time.sleep()`/`asyncio.sleep()` fixo — é a causa mais comum de scrapers lentos ou instáveis (espera de mais ou de menos).

## 5. Seletores e extração de dados

Playwright suporta seletores CSS, texto, e seletores próprios (`get_by_role`, `get_by_text`), muito mais legíveis:

```python
# Por CSS
linhas = await page.query_selector_all("table.disciplinas tbody tr")
for linha in linhas:
    celulas = await linha.query_selector_all("td")
    codigo = await celulas[0].inner_text()
    nome = await celulas[1].inner_text()

# Por texto/role (mais legível e resiliente a mudanças de estilo)
await page.get_by_role("row", name="CIC0004").click()
```

Para extrair todo o HTML e processar depois com BeautifulSoup (combinação comum: Playwright renderiza, BeautifulSoup faz o parsing fino):
```python
html = await page.content()
```

## 6. Interações comuns em sistemas institucionais

```python
# Preencher formulário de login
await page.fill("#usuario", "meu_usuario")
await page.fill("#senha", "minha_senha")
await page.click("button[type=submit]")

# Selecionar em dropdown
await page.select_option("select#departamento", "CIC")

# Esperar navegação após clique
async with page.expect_navigation():
    await page.click("a.ver-mais")
```

## 7. Reaproveitando sessão/contexto (evitar logar toda vez)

```python
context = await browser.new_context(storage_state="auth.json")  # reusa cookies salvos
# ... depois de logar uma vez:
await context.storage_state(path="auth.json")
```
Útil se o scraping de Disciplinas/Professores/Salas depende de estar autenticado no sistema da UnB — evita repetir login a cada execução.

## 8. Paralelismo e performance

- Um único `browser` pode abrir múltiplos `context`s isolados (como abas/perfis diferentes), permitindo paralelizar o scraping de várias páginas.
- Cuidado com **rate limiting**: paralelizar demais pode sobrecarregar o servidor da UnB ou disparar bloqueios.

```python
async def scrape_pagina(browser, url):
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(url)
    dado = await page.inner_text("h1")
    await context.close()
    return dado

resultados = await asyncio.gather(*[scrape_pagina(browser, url) for url in urls])
```

## 9. Depuração

- `headless=False` + `slow_mo=500` (ms) para ver as ações acontecendo devagar.
- `await page.screenshot(path="debug.png")` para capturar o estado da página em caso de erro.
- Playwright Inspector: `PWDEBUG=1 python script.py` abre um inspetor interativo.
- Modo trace (`context.tracing`) grava toda a sessão para replay posterior — excelente para depurar falhas intermitentes em CI.

## 10. Boas práticas para o RF01-05

- Isolar a lógica de **navegação/coleta** (Playwright) da lógica de **parsing** (extrair campos) e da lógica de **associação/persistência** (SQLAlchemy) — facilita testar o parser com HTML salvo, sem depender do navegador.
- Salvar HTML de exemplo localmente durante o desenvolvimento para não bater na UnB a cada teste.
- Adicionar tratamento de timeout e retry (páginas institucionais podem ser lentas).
- Rodar em modo headless com `playwright install --with-deps chromium` em ambientes de CI/produção (mais leve que instalar os três navegadores).

## 11. Recursos oficiais

- Documentação: https://playwright.dev/python/
- Guia de seletores: https://playwright.dev/python/docs/selectors
- API assíncrona: https://playwright.dev/python/docs/api/class-playwright
