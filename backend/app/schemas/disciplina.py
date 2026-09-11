"""Contrato de dados para Disciplina/Turma/Professor/Sala (RF01-05).

Representa o formato validado que sai do scraper de Disciplinas antes de
seguir para o banco. Isso é intencionalmente "burro": normalização mais
profunda (ex: casar o mesmo professor com nomes grafados diferente entre
turmas, separar "FCTE - I9/I10" em prédio+sala) é responsabilidade da
camada de domínio (app/domain/), não deste contrato — evita duplicar essa
lógica entre o scraper e os endpoints, como o ARQUITETURA.md pede.
"""

from pydantic import BaseModel


class Professor(BaseModel):
    nome: str


class Sala(BaseModel):
    descricao: str  # ex: "FCTE - I9/I10" (parsing em prédio/sala: ver app/domain/)


class Horario(BaseModel):
    codigo: str  # ex: "6T2345"
    descricao: str  # ex: "Sexta-feira 14:00 às 17:50"


class Turma(BaseModel):
    disciplina_codigo: str
    disciplina_nome: str
    numero: str
    ano_periodo: str
    professores: list[Professor]
    horarios: list[Horario]
    sala: Sala
    vagas_ofertadas: int
    vagas_ocupadas: int
