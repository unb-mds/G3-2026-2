# Guia de Estudo: Testes de Contrato com Schemathesis

## 1. O que é um Teste de Contrato

Um teste de contrato verifica se a **implementação real** de uma API respeita a **especificação documentada** dela. No caso do Cerradinho, a especificação é o schema OpenAPI, gerado automaticamente pelo FastAPI a partir do código dos endpoints.

### Diferença entre teste unitário e teste de contrato

| Teste unitário | Teste de contrato |
|---|---|
| Verifica se uma função retorna o valor esperado para uma entrada específica | Verifica se a API, como um todo, cumpre o que promete na documentação |
| Escrito manualmente, caso a caso | Gerado automaticamente a partir do schema |
| Não detecta divergência entre código e documentação | Existe justamente para detectar essa divergência |

### Por que isso importa no Cerradinho

Como o Cerradinho expõe uma API pública consumida por terceiros (via SDK/CLI), qualquer mudança que quebre o contrato documentado (ex: um campo que muda de tipo, um campo que some da resposta, um status code que muda) pode quebrar sistemas de quem consome a API sem aviso. O teste de contrato existe pra pegar isso **antes** de ir pra produção.

---

## 2. OpenAPI / Swagger

OpenAPI é um formato padronizado (JSON ou YAML) para descrever uma API REST: quais endpoints existem, quais parâmetros aceitam, quais respostas retornam, com quais tipos de dado.

### Geração automática no FastAPI

O FastAPI gera o schema OpenAPI automaticamente, sem esforço extra, a partir das assinaturas de função e dos tipos declarados (via Pydantic). Duas rotas ficam disponíveis por padrão:

- `/docs` — interface visual interativa (Swagger UI)
- `/openapi.json` — o schema bruto, em JSON

Isso significa que, se o código do endpoint mudar (ex: um campo deixa de ser obrigatório), o schema muda junto automaticamente — o que é ótimo para manter documentação atualizada, mas também significa que **erros de código viram erros de documentação automaticamente**, sem ninguém perceber. É exatamente esse tipo de erro silencioso que o schemathesis é feito para capturar.

---

## 3. O que é o Schemathesis

Schemathesis é uma ferramenta de testes que lê um schema OpenAPI e **gera testes automaticamente** a partir dele, sem que seja necessário escrever caso por caso manualmente.

Ela aplica o conceito de **property-based testing**: em vez de testar com um único exemplo fixo de entrada, ela gera muitas variações de entrada (dados válidos, extremos, ausentes, malformados) e verifica se a API se comporta de forma consistente com o que o schema promete em todos os casos.

### O que ela verifica automaticamente

- Se a resposta bate com o schema declarado (tipos, campos obrigatórios)
- Se os status codes retornados são os documentados
- Se a API não quebra (erro 500) com entradas inesperadas mas válidas segundo o schema
- Se respostas de erro (4xx) seguem o formato esperado

---

## 4. Uso Básico

### Instalação

```bash
pip install schemathesis
```

### Uso via linha de comando (contra uma API rodando)

```bash
schemathesis run http://localhost:8000/openapi.json
```

Isso já roda uma bateria de testes automáticos contra a API local, sem precisar escrever nenhum teste manualmente.

### Integração com pytest

Schemathesis também pode ser usado dentro de uma suíte pytest, o que é mais interessante para o Cerradinho, já que os outros testes do projeto também usam pytest:

```python
import schemathesis

schema = schemathesis.from_uri("http://localhost:8000/openapi.json")

@schema.parametrize()
def test_api_contract(case):
    case.call_and_validate()
```

Esse pequeno trecho já gera automaticamente múltiplos casos de teste para **todos** os endpoints declarados no schema, sem precisar escrever um teste por rota manualmente.

---

## 5. Rodando contra o schema local (sem servidor rodando)

Também é possível carregar o schema diretamente do código, sem precisar subir o servidor:

```python
from fastapi.testclient import TestClient
from myapp.main import app

schema = schemathesis.from_asgi("/openapi.json", app)
```

Isso é útil para rodar os testes de contrato dentro do pipeline de CI, sem depender de subir a aplicação inteira em um servidor real.

---

## 6. Aplicação Prática no Cerradinho

- Cada endpoint publicado pela API (ex: `/v1/disciplinas`, `/v1/ru/cardapio`) deve ter um teste de contrato rodando via schemathesis.
- Esses testes podem ser executados automaticamente em cada Pull Request, via GitHub Actions, garantindo que nenhuma mudança quebre o contrato documentado sem que o time perceba (RNF04).
- Isso complementa, mas não substitui, os testes unitários e de integração escritos manualmente — o schemathesis cobre casos que seriam difíceis de prever e escrever à mão.

---

## 7. Resumo Rápido

| Conceito | O que é |
|---|---|
| Teste de contrato | Verifica se a API real cumpre o que a documentação promete |
| OpenAPI | Formato padronizado de especificação de API REST |
| `/openapi.json` | Schema gerado automaticamente pelo FastAPI |
| Property-based testing | Geração automática de múltiplas variações de entrada para teste |
| `schemathesis.from_uri` | Carrega o schema a partir de uma API rodando |
| `schemathesis.from_asgi` | Carrega o schema direto do código, sem precisar de servidor rodando |
| `case.call_and_validate()` | Executa e valida um caso de teste gerado automaticamente |

---

## 8. Dicas Finais

- Rodar schemathesis desde cedo, mesmo com poucos endpoints prontos, evita acumular dívida técnica de contrato quebrado.
- Preferir `from_asgi` no ambiente de CI, evitando a necessidade de subir um servidor real só para rodar os testes.
- Usar esses testes como complemento, não substituto, dos testes unitários — eles cobrem ângulos diferentes.