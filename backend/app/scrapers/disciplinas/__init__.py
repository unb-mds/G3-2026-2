"""Ponto de entrada público do scraper de Disciplinas (RF01-05).

Orquestra scraper.py (captura via Playwright) + parser.py (validação via
BeautifulSoup + Pydantic), expondo só o resultado já validado. Quem chama
isso daqui (uma task do Celery, por exemplo) não precisa saber que por
baixo tem Playwright/BeautifulSoup — só recebe list[Turma].
"""

from app.schemas.disciplina import Turma

from .parser import listar_unidades, parse_turmas
from .scraper import DisciplinaScraper

__all__ = ["DisciplinaScraper", "raspar_disciplinas", "raspar_disciplinas_varias_unidades"]


async def raspar_disciplinas(nivel: str, unidade: str, ano: str, periodo: str) -> list[Turma]:
    """Captura e valida as turmas de uma unidade. Este é o contrato
    público do módulo: entrada = filtros de busca, saída = list[Turma]."""
    scraper = DisciplinaScraper()
    html = await scraper.buscar_html(nivel, unidade, ano, periodo)
    return parse_turmas(html)


async def raspar_disciplinas_varias_unidades(
    nivel: str,
    ano: str,
    periodo: str,
    unidades: list[str] | None = None,
) -> list[Turma]:
    """Mesma coisa, para várias unidades de uma vez. Se `unidades` for
    None, varre todas as unidades listadas no formulário do SIGAA."""
    scraper = DisciplinaScraper()

    if unidades is None:
        html_formulario = await scraper.obter_html_formulario()
        unidades = [codigo for codigo, _ in listar_unidades(html_formulario)]

    html_por_unidade = await scraper.buscar_html_varias_unidades(nivel, ano, periodo, unidades)

    turmas: list[Turma] = []
    for html in html_por_unidade.values():
        turmas.extend(parse_turmas(html))
    return turmas
