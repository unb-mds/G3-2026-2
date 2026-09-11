from bs4 import BeautifulSoup
from app.schemas.disciplina import Horario, Professor, Sala, Turma

def listar_unidades(html_pagina_busca: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html_pagina_busca, "html.parser")
    select = soup.select_one('select[name="formTurma:inputDepto"]')
    if select is None:
        return []

    unidades = []
    for opcao in select.find_all("option"):
        valor = (opcao.get("value") or "").strip()
        nome = opcao.get_text(strip=True)
        if valor and valor != "0":  # "0" é o placeholder "-- SELECIONE --"
            unidades.append((valor, nome))
    return unidades


def parse_turmas(html: str) -> list[Turma]:
    soup = BeautifulSoup(html, "html.parser")
    tabela = soup.select_one("#turmasAbertas table.listagem")
    if tabela is None or tabela.find("tbody") is None:
        return []

    turmas: list[Turma] = []
    disciplina_codigo = disciplina_nome = ""

    for row in tabela.find("tbody").find_all("tr", recursive=False):
        if "agrupador" in row.get("class", []):
            titulo = row.find("span", class_="tituloDisciplina")
            if titulo:
                codigo, _, nome = titulo.get_text(strip=True).partition(" - ")
                disciplina_codigo, disciplina_nome = codigo.strip(), nome.strip()
            continue

        celulas = row.find_all("td")
        if len(celulas) < 8 or not disciplina_codigo:
            continue

        professores = [
            Professor(nome=t.strip())
            for t in celulas[2].stripped_strings
            if t.strip()
        ]

        # Horário ocupa 2 colunas; a segunda vem vazia se só há um horário.
        horarios: list[Horario] = []
        for cel in (celulas[3], celulas[4]):
            textos = list(cel.stripped_strings)
            if not textos:
                continue
            popup = cel.find("div", class_="popUp")
            horarios.append(Horario(
                codigo=textos[0],
                descricao=popup.get_text(" ", strip=True) if popup else "",
            ))

        turmas.append(Turma(
            disciplina_codigo=disciplina_codigo,
            disciplina_nome=disciplina_nome,
            numero=celulas[0].get_text(strip=True),
            ano_periodo=celulas[1].get_text(strip=True),
            professores=professores,
            horarios=horarios,
            sala=Sala(descricao=celulas[7].get_text(strip=True)),
            vagas_ofertadas=celulas[5].get_text(strip=True),
            vagas_ocupadas=celulas[6].get_text(strip=True),
        ))

    return turmas
