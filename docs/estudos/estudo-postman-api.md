# Guia de Estudo: Postman e Testes de API

## 1. Conceitos Fundamentais

### O que é uma API?
API (Application Programming Interface) é uma interface que permite que sistemas diferentes conversem entre si. No contexto do Cerradinho, os scrapers vão consumir dados de fontes externas (SIGAA, RU, CKAN, Notícias) e nossa própria aplicação vai expor uma API REST em FastAPI para que outros sistemas consumam esses dados.

### O que é uma requisição HTTP?
Toda comunicação com uma API acontece via **HTTP**: o cliente (navegador, Postman, outro sistema) envia uma requisição, e o servidor devolve uma resposta.

Uma requisição HTTP tem:
- **Método**: a ação que se quer fazer (GET, POST, PUT, DELETE...)
- **URL**: o endereço do recurso (ex: `https://ru.unb.br/cardapio`)
- **Headers**: metadados (autenticação, tipo de conteúdo, etc.)
- **Body**: dados enviados junto (usado em POST/PUT, geralmente ausente em GET)

Uma resposta HTTP tem:
- **Status code**: um número que indica o resultado (200 = sucesso, 404 = não encontrado, 500 = erro no servidor)
- **Headers**: metadados da resposta
- **Body**: o conteúdo retornado (JSON, HTML, etc.)

### Métodos HTTP mais usados

| Método | Uso |
|---|---|
| `GET` | Buscar um dado, sem alterar nada no servidor |
| `POST` | Criar um novo recurso / enviar dados |
| `PUT` | Atualizar um recurso por completo |
| `PATCH` | Atualizar um recurso parcialmente |
| `DELETE` | Remover um recurso |

### Status codes mais comuns

| Faixa | Significado |
|---|---|
| `2xx` | Sucesso (200 OK, 201 Created, 204 No Content) |
| `3xx` | Redirecionamento |
| `4xx` | Erro do cliente (400 Bad Request, 401 Unauthorized, 404 Not Found) |
| `5xx` | Erro do servidor (500 Internal Server Error, 503 Service Unavailable) |

---

## 2. O que é o Postman

O Postman é uma ferramenta que permite montar, enviar e inspecionar requisições HTTP sem precisar escrever código. É útil tanto para **consumir** APIs já existentes quanto para **testar** APIs que estamos construindo.

No Cerradinho, o Postman serve para dois propósitos principais:
1. **Investigar** como as fontes externas (SIGAA, RU, CKAN, Notícias) respondem, antes de escrever qualquer scraper.
2. **Testar** os endpoints da nossa própria API FastAPI conforme vão sendo criados.

### Componentes principais

- **Request**: uma requisição individual configurada (método, URL, headers, body).
- **Collection**: uma pasta que agrupa várias requests relacionadas. Facilita organizar e reutilizar.
- **Environment**: um conjunto de variáveis (ex: `{{base_url}}`) que muda conforme o ambiente (local, produção), evitando reescrever URLs fixas toda hora.

---

## 3. Montando uma Request no Postman

Passo a passo básico:

1. Escolher o **método** (GET, POST, etc.) no menu suspenso.
2. Digitar a **URL** do recurso.
3. Se necessário, adicionar **Params** (parâmetros de busca, ex: `?data=2026-09-08`).
4. Se necessário, adicionar **Headers** (ex: `Content-Type: application/json`).
5. Se for POST/PUT, preencher o **Body** com os dados a enviar.
6. Clicar em **Send**.
7. Analisar a resposta: status code, tempo de resposta, corpo (JSON/HTML/texto).

### Exemplo prático (investigação de fonte)

Para investigar o RU:
```
Método: GET
URL: https://ru.unb.br/cardapio
```
Ao mandar essa request, observamos:
- Se retorna HTML puro (precisará de parsing/scraping) ou JSON (já estruturado)
- Se exige autenticação/sessão ou é público
- Qual o tempo de resposta e a estabilidade

---

## 4. Organizando com Collections

Em vez de testar requests soltas e perder o histórico, agrupamos em uma Collection, por exemplo:

```
Cerradinho - Investigação de Fontes
├── RU - Cardápio (GET)
├── CKAN - Datasets (GET)
├── SIGAA - Turmas (GET/POST)
├── SIGAA - Editais (GET)
└── Notícias - Agenda (GET)
```

Cada request salva mantém o histórico do que foi enviado e recebido, o que facilita comparar respostas ao longo do tempo (importante para detectar mudanças nas fontes — ligado ao RNF05, resiliência).

---

## 5. Environments e Variáveis

Ao invés de escrever a URL completa em cada request, usamos variáveis:

```
{{base_url}}/api/v1/disciplinas
```

E depois definimos `base_url` diferente por ambiente:
- **Local**: `http://localhost:8000`
- **Produção**: `https://api.cerradinho.unb.br`

Isso evita ter que editar dezenas de requests manualmente quando o endereço muda.

---

## 6. DevTools do Navegador (complemento ao Postman)

Antes de replicar uma requisição no Postman, é útil primeiro observar como o navegador se comunica com o site, usando a aba **Network** do DevTools (F12):

1. Abrir o site da fonte (ex: SIGAA, RU).
2. Abrir o DevTools → aba **Network**.
3. Recarregar a página ou interagir com ela.
4. Observar as requisições que aparecem: URL, método, headers, resposta.
5. Replicar essa mesma requisição no Postman para testar isoladamente.

### Cuidado com fontes que usam sessão/estado (ex: SIGAA)
O SIGAA usa JSF (JavaServer Faces), que depende de um mecanismo chamado **ViewState** — um token que muda a cada sessão/postback. Isso significa que uma requisição simples de GET não é suficiente: é necessário capturar o ViewState atual e reenviá-lo na requisição seguinte (POST), o que torna essa fonte mais instável e mais arriscada de scraping (relevante para o relatório de risco do RNF05).

---

## 7. Testes de Contrato (aplicação futura)

Mais adiante no projeto, quando a API do Cerradinho já tiver endpoints publicados, entra o conceito de **teste de contrato**: verificar se a resposta real da API bate com o que está documentado na especificação OpenAPI (gerada automaticamente pelo FastAPI em `/openapi.json`).

Isso é diferente de um teste unitário: o teste de contrato garante que a API não "quebrou a promessa" feita na documentação — por exemplo, um campo que deixou de ser retornado ou mudou de tipo sem aviso. Essa etapa é feita com a ferramenta `schemathesis`, que lê o schema OpenAPI e gera testes automaticamente a partir dele.

---

## 8. Comandos e Conceitos — Resumo Rápido

| Conceito | O que é |
|---|---|
| Request | Uma requisição HTTP configurada (método + URL + headers + body) |
| Collection | Conjunto de requests organizadas em pastas |
| Environment | Conjunto de variáveis que mudam por ambiente (local/produção) |
| GET | Busca dado sem alterar nada |
| POST | Envia/cria dado |
| Status code 2xx | Sucesso |
| Status code 4xx | Erro do cliente (ex: 404 não encontrado) |
| Status code 5xx | Erro do servidor |
| DevTools Network tab | Inspeciona requisições feitas pelo navegador |
| ViewState (JSF/SIGAA) | Token de sessão que muda a cada requisição, dificultando scraping simples |
| Teste de contrato | Verifica se a API real bate com a documentação OpenAPI |
| schemathesis | Ferramenta que gera testes de contrato a partir do schema OpenAPI |

---

## 9. Aplicação Prática no Cerradinho

- **Ciclo 1**: usar Postman + DevTools para investigar as 5 fontes públicas (RU, CKAN, SIGAA-disciplinas, SIGAA-editais, Notícias) e documentar o risco de cada uma (RNF05).
- **Ciclo 2 em diante**: usar Postman para testar manualmente os endpoints da API FastAPI conforme são publicados, complementando os testes automatizados de contrato feitos com `schemathesis` (RNF04).

## 10. Dicas Finais

- Sempre salvar as requests em uma Collection, mesmo em fase de investigação — evita perder o que já foi descoberto.
- Documentar a resposta real (exemplo de JSON/HTML) de cada fonte no relatório de risco, não só descrever de memória.
- Preferir investigar primeiro as fontes mais simples (RU, CKAN) antes de partir para o SIGAA, que exige lidar com sessão/ViewState.
- Usar variáveis de Environment desde o início evita retrabalho quando o projeto migrar de ambiente local para produção.