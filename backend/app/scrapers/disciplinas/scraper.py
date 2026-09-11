"""
NOTA (causa raiz de um bug sutil, documentada para quem mexer aqui depois):
o SIGAA usa um contador de "views" por sessão, visível no campo oculto
javax.faces.ViewState (j_id1, j_id6...). Uma sessão que nasce direto na
página de busca começa "fria demais" e o Buscar falha com "sessão não
está mais ativa". Por isso `buscar` sempre visita a home antes de ir para
a busca — isso "aquece" a sessão. Também usamos `domcontentloaded` em vez
de `networkidle`: o Google Analytics da página nunca deixa a rede ficar
de fato ociosa, o que travava o scraper indefinidamente.
"""

from __future__ import annotations
import asyncio
from playwright.async_api import Page, async_playwright

URL_HOME = "https://sigaa.unb.br/sigaa/public/"
URL_BUSCA_TURMAS = "https://sigaa.unb.br/sigaa/public/turmas/listar.jsf?aba=p-ensino"

_SELETOR_NIVEL = '[name="formTurma:inputNivel"]'
_SELETOR_UNIDADE = '[name="formTurma:inputDepto"]'
_SELETOR_ANO = '[name="formTurma:inputAno"]'
_SELETOR_PERIODO = '[name="formTurma:inputPeriodo"]'
_SELETOR_BOTAO_BUSCAR = 'input[type="submit"][value="Buscar"]'


def _sessao_expirada(html: str) -> bool:
    """SIGAA grava a mensagem de erro com escape unicode (n\\u00e3o em vez
    de "ã"), então comparamos por "mais ativa" (sem acentuação) — senão a
    comparação nunca dá match."""
    html_lower = html.lower()
    return "mais ativa" in html_lower or "viewexpired" in html_lower


class DisciplinaScraper:
    """Captura HTML da consulta pública de turmas do SIGAA.

    nivel: "G" (graduação), "F", "L", "R", "S", "E" (mestrado) ou "D" (doutorado).
    unidade: código numérico do departamento (ex: "673" = CAMPUS UNB GAMA: FCTE).
    """

    def __init__(self, headless: bool = True) -> None:
        self._headless = headless

    async def _preencher_e_buscar(self, page: Page, nivel: str, unidade: str, ano: str, periodo: str) -> None:
        await page.locator(_SELETOR_NIVEL).select_option(nivel)
        await page.locator(_SELETOR_UNIDADE).select_option(unidade)
        await page.locator(_SELETOR_ANO).fill(ano)
        await page.locator(_SELETOR_PERIODO).select_option(periodo)
        await page.locator(_SELETOR_BOTAO_BUSCAR).click()
        await page.wait_for_load_state("domcontentloaded")

    async def obter_html_formulario(self) -> str:
        """HTML da própria página de busca, sem preencher nada — útil para
        descobrir as opções disponíveis (ex: lista de unidades) via
        parser.listar_unidades, sem precisar fazer uma busca completa."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self._headless)
            page = await browser.new_page()
            await page.goto(URL_HOME, wait_until="domcontentloaded")
            await page.goto(URL_BUSCA_TURMAS, wait_until="domcontentloaded")
            html = await page.content()
            await browser.close()
            return html

    async def buscar_html(self, nivel: str, unidade: str, ano: str, periodo: str, tentativas: int = 3) -> str:
        """Busca uma unidade e devolve o HTML bruto do resultado."""
        for tentativa in range(1, tentativas + 1):
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self._headless)
                page = await browser.new_page()

                await page.goto(URL_HOME, wait_until="domcontentloaded")
                await page.goto(URL_BUSCA_TURMAS, wait_until="domcontentloaded")
                await self._preencher_e_buscar(page, nivel, unidade, ano, periodo)

                html = await page.content()
                await browser.close()

            if not _sessao_expirada(html):
                return html

            print(f"Sessão expirou na tentativa {tentativa}/{tentativas} (unidade {unidade}), tentando de novo...")

        raise RuntimeError(
            f"SIGAA continuou respondendo 'sessão não está mais ativa' para a unidade {unidade} "
            f"após {tentativas} tentativas."
        )

    async def buscar_html_varias_unidades(
        self,
        nivel: str,
        ano: str,
        periodo: str,
        unidades: list[str],
        atraso_segundos: float = 2.0,
    ) -> dict[str, str]:
        """Busca várias unidades reaproveitando a mesma sessão (mais rápido
        que abrir um navegador novo por unidade, e evita repetir o
        "aquecimento" da sessão a cada uma). Devolve {codigo_unidade: html};
        unidades que falharem após as tentativas ficam de fora do dict."""
        resultados: dict[str, str] = {}

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self._headless)
            page = await browser.new_page()
            await page.goto(URL_HOME, wait_until="domcontentloaded")

            for codigo_unidade in unidades:
                html = None
                for tentativa in range(1, 4):
                    await page.goto(URL_BUSCA_TURMAS, wait_until="domcontentloaded")
                    await self._preencher_e_buscar(page, nivel, codigo_unidade, ano, periodo)
                    html = await page.content()
                    if not _sessao_expirada(html):
                        break
                    print(f"  unidade {codigo_unidade}: sessão expirou, tentativa {tentativa}/3")
                    html = None

                if html is None:
                    print(f"unidade {codigo_unidade}: falhou após 3 tentativas, pulando.")
                    continue

                resultados[codigo_unidade] = html
                await asyncio.sleep(atraso_segundos)  # etiqueta com o servidor da UnB

            await browser.close()

        return resultados
