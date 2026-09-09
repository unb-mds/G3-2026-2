# Guia de Estudo: Pytest e Mocking

## 1. O que é o Pytest

Pytest é o framework de testes mais usado no ecossistema Python. Ele permite escrever testes de forma simples, usando apenas funções com `assert`, sem precisar de classes ou boilerplate como em outros frameworks (ex: `unittest`).

### Por que usar pytest no Cerradinho

- É a base sobre a qual o schemathesis roda (testes de contrato)
- Permite organizar testes unitários, de integração e de contrato num único formato consistente
- Tem suporte nativo a fixtures, parametrização e plugins de cobertura

---

## 2. Estrutura Básica de um Projeto Pytest

Convenção padrão de nomes de arquivos e funções:

```
projeto/
├── src/
│   └── app.py
└── tests/
    ├── conftest.py
    ├── test_app.py
    └── test_scraper.py
```

- Arquivos de teste começam com `test_` ou terminam com `_test.py`
- Funções de teste começam com `test_`
- O pytest descobre e roda esses testes automaticamente, sem precisar registrar cada um manualmente

### Exemplo mínimo

```python
def soma(a, b):
    return a + b

def test_soma():
    assert soma(2, 3) == 5
```

Rodar com:
```bash
pytest
```

---

## 3. Fixtures

Fixtures são funções que preparam algo necessário para os testes (dados, conexões, objetos), evitando repetição de código de setup em cada teste.

```python
import pytest

@pytest.fixture
def cliente_api():
    # simula um cliente configurado, reaproveitado em vários testes
    return {"base_url": "http://localhost:8000"}

def test_endpoint_disciplinas(cliente_api):
    assert cliente_api["base_url"] == "http://localhost:8000"
```

### conftest.py

Fixtures que precisam ser compartilhadas entre **vários arquivos de teste** ficam num arquivo especial chamado `conftest.py`, que o pytest carrega automaticamente sem precisar de import explícito.

---

## 4. Parametrize

Permite rodar o mesmo teste várias vezes, com entradas diferentes, sem duplicar código:

```python
import pytest

@pytest.mark.parametrize("entrada,esperado", [
    (2, 4),
    (3, 6),
    (0, 0),
])
def test_dobro(entrada, esperado):
    assert entrada * 2 == esperado
```

Isso gera 3 testes distintos a partir de uma única função, útil por exemplo para testar vários formatos de resposta de uma mesma fonte de dados.

---

## 5. Mocking

Mocking é a técnica de **substituir uma dependência real** (chamada de rede, banco de dados, arquivo) por um objeto simulado, controlado pelo próprio teste. Isso permite testar código que depende de fontes externas (como o SIGAA ou o RU) sem realmente fazer a requisição de verdade.

### Por que isso é essencial no Cerradinho

- Testar o comportamento do scraper sem depender do SIGAA estar disponível/estável no momento do teste
- Evitar sobrecarregar servidores externos com testes automatizados repetidos
- Simular respostas de erro (500, timeout) que seriam difíceis de reproduzir de propósito na fonte real

### Exemplo com `unittest.mock`

```python
from unittest.mock import patch

def buscar_cardapio_ru():
    import requests
    resposta = requests.get("https://ru.unb.br/cardapio")
    return resposta.json()

@patch("requests.get")
def test_buscar_cardapio_ru(mock_get):
    mock_get.return_value.json.return_value = {"prato": "arroz e feijão"}
    resultado = buscar_cardapio_ru()
    assert resultado["prato"] == "arroz e feijão"
```

Aqui, `requests.get` nunca é chamado de verdade — o mock intercepta a chamada e devolve uma resposta fabricada, controlada pelo teste.

### pytest-mock (alternativa mais integrada ao pytest)

```python
def test_buscar_cardapio_ru(mocker):
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.json.return_value = {"prato": "arroz e feijão"}
    resultado = buscar_cardapio_ru()
    assert resultado["prato"] == "arroz e feijão"
```

A fixture `mocker` (do plugin `pytest-mock`) evita precisar do decorator `@patch`, deixando a sintaxe mais próxima do estilo do pytest.

---

## 6. Cobertura de Testes com pytest-cov

Mede quanto do código-fonte é efetivamente executado pelos testes:

```bash
pip install pytest-cov
pytest --cov=src
```

Isso gera um relatório mostrando quais linhas/arquivos não têm nenhum teste passando por elas — útil para identificar áreas do projeto ainda não cobertas (ex: um endpoint novo sem teste correspondente).

---

## 7. Aplicação Prática no Cerradinho

- **Testes de scraper**: usar mocks para simular respostas do SIGAA/RU/CKAN, sem depender de disponibilidade real durante o CI
- **Testes de contrato (schemathesis)**: rodam dentro da mesma suíte pytest, junto dos testes unitários
- **Fixtures compartilhadas**: um `conftest.py` no projeto pode centralizar clientes de teste (ex: `TestClient` do FastAPI) reaproveitados por vários arquivos de teste
- **Cobertura**: pode ser configurada para rodar automaticamente a cada PR via GitHub Actions, dando visibilidade de quanto do código está testado

---

## 8. Resumo Rápido

| Conceito | O que é |
|---|---|
| Fixture | Função de setup reaproveitável entre testes |
| conftest.py | Arquivo especial com fixtures compartilhadas entre múltiplos arquivos |
| Parametrize | Roda o mesmo teste com várias entradas diferentes |
| Mock | Substitui uma dependência real por uma simulada, controlada pelo teste |
| `unittest.mock.patch` | Forma nativa do Python de fazer mocking |
| `pytest-mock` | Plugin que integra mocking ao estilo de fixtures do pytest |
| `pytest-cov` | Mede cobertura de testes sobre o código-fonte |

---

## 9. Dicas Finais

- Sempre mockar chamadas de rede em testes automatizados — nunca depender da fonte real estar no ar para o CI passar.
- Nomear fixtures de forma clara (`cliente_api`, `mock_sigaa_response`) para facilitar entendimento de quem revisar o PR.
- Rodar `pytest --cov` regularmente para identificar partes do código sem cobertura, especialmente nas áreas de scraping (mais propensas a bugs silenciosos).
- Testes de contrato (schemathesis) e testes unitários com mock são complementares — um não substitui o outro.