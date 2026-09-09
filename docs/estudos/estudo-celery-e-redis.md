# Estudo: Celery e Redis

> Contexto: Celery e Redis serão usados no Cerradinho como a infra de jobs assíncronos — agendamento automático de scraping (RF15) e log de sucesso/falha de execução (RF16) — além de servirem de base para cache (RNF02) e rate limiting (RNF01), que reaproveitam a mesma instância de Redis.

---

## 1. O que é e por que usar

Celery é uma fila de tasks distribuída para Python: permite rodar trabalho pesado (scraping, envio de dados, etc.) em segundo plano, fora do ciclo de request/response da API. Redis entra como **broker** — a fila de mensagens que guarda as tasks pendentes — e opcionalmente como **result backend**, guardando o status/resultado de cada execução.

Vantagens relevantes para o projeto:
- **Desacopla scraping da API:** um request em `/disciplinas` não fica esperando o scraper do SIGAA terminar — a API só dispara a task e responde na hora.
- **Agendamento nativo (`celery beat`):** resolve o RF15 sem precisar de cron externo ou scheduler separado.
- **Resiliência:** retries automáticos absorvem falhas temporárias de fontes externas (RNF05), como o SIGAA ficando fora do ar.
- **Reaproveitamento de infra:** o mesmo Redis usado como broker também serve de backend de cache (RNF02) e de storage do `slowapi` (RNF01) — uma peça de infra, três usos.

## 2. Conceitos fundamentais

### 2.1 Broker, worker, task e result backend
- **Broker:** onde as tasks esperam para ser executadas (Redis).
- **Worker:** processo que consome a fila e roda a task.
- **Task:** função Python decorada com `@app.task`.
- **Result backend:** onde fica o status/resultado de cada execução (pode ser o mesmo Redis, em outro índice de banco).

```python
from celery import Celery

celery_app = Celery(
    "cerradinho",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

@celery_app.task
def scrape_disciplinas(unidade: str):
    # lógica de scraping aqui
    return {"status": "ok", "unidade": unidade}
```

### 2.2 Disparando uma task
```python
resultado = scrape_disciplinas.delay("FCTE")
print(resultado.id)  # task_id, útil pra devolver num 202 Accepted
```

### 2.3 Consultando status e resultado
```python
from celery.result import AsyncResult

r = AsyncResult(task_id, app=celery_app)
r.status  # PENDING, STARTED, SUCCESS, FAILURE
r.result  # retorno da task, quando já concluída
```

### 2.4 `celery beat` — agendamento periódico (RF15)
```python
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    "scrape-disciplinas-diario": {
        "task": "tasks.scrape_disciplinas",
        "schedule": crontab(hour=3, minute=0),
        "args": ("FCTE",),
    },
}
```
Precisa de dois processos separados rodando:
```bash
celery -A cerradinho worker --loglevel=info
celery -A cerradinho beat --loglevel=info
```

### 2.5 Capturando sucesso e falha (RF16)
Retry manual dentro da task:
```python
@celery_app.task(bind=True, max_retries=3)
def scrape_disciplinas(self, unidade: str):
    try:
        ...
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
```

Signals globais — melhor lugar para centralizar o log de execução do RF16, sem repetir código em cada task:
```python
from celery.signals import task_success, task_failure

@task_success.connect
def log_success(sender=None, result=None, **kwargs):
    ...  # grava no banco: status=sucesso, task=sender.name

@task_failure.connect
def log_failure(sender=None, task_id=None, exception=None, **kwargs):
    ...  # grava no banco: status=falha, erro=str(exception)
```

## 3. Aplicação prática no Cerradinho

| Requisito | Como Celery/Redis ajuda |
|---|---|
| RF01-09 (scraping de todos os domínios) | Cada scraper (Disciplinas, RU, Eventos, Editais) roda como uma task, desacoplada da API |
| RF15 (agendamento automático) | `celery beat` agenda a execução periódica de cada scraper |
| RF16 (log de sucesso/falha) | Signals `task_success`/`task_failure` centralizam o registro de cada execução |
| RNF01 (rate limiting) | O mesmo Redis serve de storage distribuído para o `slowapi` |
| RNF02 (cache) | O mesmo Redis guarda o cache dos endpoints, em um banco lógico separado do broker |
| RNF05 (resiliência) | Retry com backoff nas tasks absorve instabilidade de fontes externas (ex: SIGAA fora do ar) |

## 4. Boas práticas para trabalhar em equipe

- **Separar tasks por domínio:** `tasks/disciplinas.py`, `tasks/ru.py`, `tasks/eventos.py` — espelhando a separação em `routers/` que o Vitor já adotou.
- **Bancos Redis diferentes por função:** um índice para broker, outro para result backend, outro para cache — evita misturar dados de fila com dados de cache.
- **Retry com backoff exponencial**, não tentativa imediata — evita martelar uma fonte externa já instável.
- **Configuração via `pydantic-settings`:** `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, sem hardcode — mesmo padrão que o Vitor usou pra URL do banco.

## 5. Recursos oficiais

- Documentação oficial do Celery: https://docs.celeryq.dev/
- Documentação oficial do Redis: https://redis.io/docs/
- Seção "First steps with Celery" da doc oficial
- Guia "Celery and FastAPI" (integração prática entre os dois)