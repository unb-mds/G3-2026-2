# Estudo: FastAPI

> Contexto: FastAPI será usado no Cerradinho para expor os endpoints da API aberta da UnB (Disciplinas, Professores, Salas, salas vazias — RF17, agenda do professor — RF18) e como base para o SDK Python (RF13).

---

## 1. O que é e por que usar

FastAPI é um framework web Python moderno, focado em performance e produtividade, construído sobre **Starlette** (camada assíncrona) e **Pydantic** (validação de dados).

Vantagens relevantes para o projeto:
- **Tipagem nativa:** os tipos do Python (`str`, `int`, modelos Pydantic) viram validação automática de entrada e saída.
- **Documentação automática:** gera Swagger UI (`/docs`) e Redoc (`/redoc`) sem esforço extra — ótimo para um SDK/API pública que outras pessoas vão consumir.
- **Assíncrono nativo:** essencial para endpoints que dependem de I/O (banco de dados, scraping sob demanda).
- **Alta performance** comparado a frameworks WSGI tradicionais (Flask/Django) em cenários assíncronos.

## 2. Conceitos fundamentais

### 2.1 Aplicação e rotas básicas
```python
from fastapi import FastAPI

app = FastAPI(title="Cerradinho API")

@app.get("/disciplinas")
async def listar_disciplinas():
    return [{"codigo": "CIC0004", "nome": "Algoritmos e Programação de Computadores"}]
```

### 2.2 Path e Query parameters
```python
@app.get("/disciplinas/{codigo}")
async def obter_disciplina(codigo: str):
    ...

@app.get("/professores")
async def listar_professores(departamento: str | None = None, limit: int = 20):
    ...
```
- Parâmetros de **path** (`{codigo}`) identificam um recurso específico.
- Parâmetros de **query** (`?departamento=CIC`) filtram/paginam listagens — muito usado no RF17 (salas vazias) e RF18 (agenda do professor), por exemplo `?data=2026-09-07&horario=14h`.

### 2.3 Modelos com Pydantic (schemas)
```python
from pydantic import BaseModel

class Disciplina(BaseModel):
    codigo: str
    nome: str
    carga_horaria: int
    professor_id: int | None = None

@app.post("/disciplinas")
async def criar_disciplina(disciplina: Disciplina):
    ...
```
- O Pydantic valida automaticamente o corpo da requisição contra o schema.
- É comum separar schemas de **entrada** (o que a API recebe) dos de **saída** (o que a API retorna), e dos **modelos do banco** (SQLAlchemy) — evitando vazar detalhes internos do banco na API pública.

### 2.4 Dependency Injection (`Depends`)
```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/salas")
async def listar_salas(db: Session = Depends(get_db)):
    return db.query(Sala).all()
```
- `Depends` é o mecanismo central do FastAPI para injetar sessões de banco, autenticação, parâmetros compartilhados, etc.
- Fundamental para conectar os endpoints às sessões do SQLAlemy sem repetir código de abertura/fechamento de conexão.

### 2.5 Async vs sync
- Use `async def` quando a função faz operações de I/O que podem ser aguardadas (`await`) — chamadas assíncronas ao banco, requisições HTTP externas, Playwright assíncrono.
- Se uma função é síncrona (bibliotecas que não suportam `async`), o FastAPI ainda lida bem rodando-a em um threadpool — mas é bom saber a diferença para não bloquear o event loop acidentalmente.

### 2.6 Roteadores (`APIRouter`)
```python
from fastapi import APIRouter

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])

@router.get("/")
async def listar():
    ...

# em outro arquivo:
app.include_router(router)
```
- Essencial para organizar a API por domínio (`disciplinas.py`, `professores.py`, `salas.py`) em vez de um único arquivo gigante — importante num projeto em equipe como o Cerradinho.

### 2.7 Tratamento de erros
```python
from fastapi import HTTPException

@app.get("/disciplinas/{codigo}")
async def obter_disciplina(codigo: str, db: Session = Depends(get_db)):
    disciplina = db.query(Disciplina).filter_by(codigo=codigo).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina
```

## 3. Aplicação prática no Cerradinho

| Requisito | Como o FastAPI ajuda |
|---|---|
| RF01-05 (scraping e associação) | Endpoints internos/administrativos para disparar ou consultar o resultado do scraping |
| RF17 (salas vazias) | Endpoint com query params (data, horário) que consulta o banco e retorna salas sem aula |
| RF18 (agenda do professor) | Endpoint `/professores/{id}/agenda` retornando as aulas associadas |
| RF13 (SDK Python) | A documentação automática (OpenAPI/Swagger) gerada pelo FastAPI pode ser usada para **gerar o SDK automaticamente** (ex: com `openapi-python-client`) |

## 4. Boas práticas para trabalhar em equipe

- **Separar camadas:** `routers/` (endpoints), `schemas/` (Pydantic), `models/` (SQLAlchemy), `services/` (lógica de negócio/scraping) — evita conflitos de merge e deixa claro onde cada coisa vai.
- **Usar `response_model`** nos endpoints para garantir que a API sempre retorna o formato documentado, mesmo que o modelo do banco tenha mais campos.
- **Testes com `TestClient`** (do `starlette.testclient` ou `httpx`) para testar os endpoints sem subir um servidor real.
- **Variáveis de ambiente** (`pydantic-settings`) para configurar a URL do banco, chaves, etc., sem hardcode.

## 5. Recursos oficiais

- Documentação oficial: https://fastapi.tiangolo.com/
- Tutorial oficial (passo a passo, em português também disponível)
- Seção "SQL (Relational) Databases" da doc oficial — mostra a integração com SQLAlchemy
