from pathlib import Path

from app.scrapers.disciplinas.parser import parse_turmas

FIXTURE = Path(__file__).parent / "fixtures" / "turmas_fcte_gama_2026_2.html"


def test_parse_turmas_extrai_disciplinas_e_turmas():
    html = FIXTURE.read_text(encoding="utf-8")

    turmas = parse_turmas(html)

    assert len(turmas) > 0

    primeira = turmas[0]
    assert primeira.disciplina_codigo
    assert primeira.disciplina_nome
    assert primeira.numero
    assert primeira.professores, "toda turma deveria ter ao menos um professor"
    assert primeira.sala.descricao


def test_parse_turmas_agrupa_turmas_sob_a_disciplina_correta():
    html = FIXTURE.read_text(encoding="utf-8")

    turmas = parse_turmas(html)

    algoritmos_em_grafos = [t for t in turmas if t.disciplina_nome == "ALGORITMOS EM GRAFOS"]
    assert len(algoritmos_em_grafos) >= 1
    assert algoritmos_em_grafos[0].disciplina_codigo == "FCTE0005"
