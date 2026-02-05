"""
Servicio de scraping para el Poder Judicial de Chile.
Extrae causas y sus detalles completos de la Oficina Judicial Virtual.
"""

import asyncio
import json
import re
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class Actuacion:
    """Representa una actuación/trámite en una causa."""
    folio: str
    etapa: str
    tramite: str
    descripcion: str
    fecha: str
    foja: str = ""
    tiene_documento: bool = False


@dataclass
class Causa:
    """Representa una causa judicial con todos sus detalles."""
    # Datos básicos
    rit: str
    ruc: str
    tribunal: str
    caratulado: str
    fecha_ingreso: str
    estado: str
    tipo: str  # Civil, Penal, Laboral, Familia, etc.

    # Datos adicionales del detalle
    procedimiento: str = ""
    etapa: str = ""
    ubicacion: str = ""
    estado_admin: str = ""

    # Historial de actuaciones
    actuaciones: List[Actuacion] = field(default_factory=list)

    # Última actuación
    ultima_actuacion: Optional[str] = None
    fecha_ultima_actuacion: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['actuaciones'] = [asdict(a) for a in self.actuaciones]
        return data


class PJUDScraper:
    """
    Scraper para la Oficina Judicial Virtual del Poder Judicial de Chile.

    Extrae causas y sus detalles completos incluyendo historial de actuaciones.
    """

    OJV_URL = "https://oficinajudicialvirtual.pjud.cl/home/index.php"

    # Tipos de causas disponibles
    TIPOS_CAUSA = ['Civil', 'Penal', 'Laboral', 'Familia', 'Cobranza', 'Corte Suprema', 'Corte Apelaciones', 'Disciplinario']

    # Modo demo para desarrollo
    DEMO_MODE = True

    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        self._authenticated = False

    async def init_browser(self, headless: bool = True):
        """Inicializa el navegador Playwright."""
        try:
            from playwright.async_api import async_playwright

            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=headless,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 900},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            self.page = await self.context.new_page()
            logger.info(f"Browser inicializado (headless={headless})")
            return True
        except Exception as e:
            logger.error(f"Error inicializando browser: {e}")
            return False

    async def close(self):
        """Cierra el navegador."""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            logger.error(f"Error cerrando browser: {e}")

    async def login(self, rut: str, password: str) -> bool:
        """
        Realiza login con ClaveÚnica.

        Args:
            rut: RUT sin puntos ni guión (ej: 209769441)
            password: Contraseña de ClaveÚnica

        Returns:
            True si el login fue exitoso
        """
        try:
            logger.info("Navegando a OJV...")
            await self.page.goto(self.OJV_URL, timeout=30000)
            await asyncio.sleep(3)

            # Abrir menú y seleccionar Clave Única
            logger.info("Seleccionando Clave Única...")
            await self.page.click('text=Todos los servicios')
            await asyncio.sleep(1)
            await self.page.locator('#myDropdown').get_by_role('link', name='Clave Única').click()
            await asyncio.sleep(5)

            # Ingresar credenciales (escribiendo, no pegando)
            logger.info("Ingresando credenciales...")
            await self.page.get_by_role('textbox', name='Ingresa tu RUN').type(rut, delay=100)
            await self.page.get_by_role('textbox', name='Ingresa tu ClaveÚnica').type(password, delay=100)

            # Presionar Enter para enviar (evita problema con botón deshabilitado)
            await self.page.keyboard.press('Enter')

            # Esperar redirección exitosa
            logger.info("Esperando autenticación...")
            for _ in range(60):
                if 'oficinajudicialvirtual.pjud.cl' in self.page.url and 'claveunica' not in self.page.url:
                    self._authenticated = True
                    logger.info("Login exitoso!")

                    # Cerrar modal informativo si aparece
                    await self._cerrar_modal()
                    return True
                await asyncio.sleep(1)

            logger.error("Timeout esperando login")
            return False

        except Exception as e:
            logger.error(f"Error en login: {e}")
            return False

    async def _cerrar_modal(self):
        """Cierra modales informativos si existen."""
        try:
            await asyncio.sleep(2)
            cerrar = await self.page.query_selector('button:has-text("Cerrar")')
            if cerrar and await cerrar.is_visible():
                await cerrar.click()
                await asyncio.sleep(1)
        except:
            pass

    async def get_causas(self) -> List[Causa]:
        """
        Obtiene todas las causas del usuario.

        Returns:
            Lista de causas con datos básicos
        """
        if not self._authenticated:
            logger.error("Usuario no autenticado")
            return []

        causas = []

        try:
            # Navegar a Mis Causas
            logger.info("Navegando a Mis Causas...")
            await self.page.click('text=Mis Causas')
            await asyncio.sleep(3)
            await self._cerrar_modal()
            await asyncio.sleep(2)

            # Recorrer cada tipo de causa
            for tipo in self.TIPOS_CAUSA:
                try:
                    logger.info(f"Revisando causas de tipo: {tipo}")
                    tab = await self.page.query_selector(f'a:has-text("{tipo}")')
                    if tab:
                        await tab.click()
                        await asyncio.sleep(2)

                        # Extraer headers de la tabla
                        headers = []
                        header_cells = await self.page.query_selector_all('table:visible thead th')
                        for th in header_cells:
                            text = await th.text_content()
                            headers.append(text.strip() if text else '')
                        logger.debug(f"Headers para {tipo}: {headers}")

                        # Extraer causas de la tabla visible
                        rows = await self.page.query_selector_all('table:visible tbody tr')
                        for row in rows:
                            causa = await self._extraer_causa_de_fila(row, tipo, headers)
                            if causa:
                                causas.append(causa)
                                logger.info(f"  Causa encontrada: {causa.rit} - {causa.estado}")
                except Exception as e:
                    logger.debug(f"Error en tipo {tipo}: {e}")
                    continue

            logger.info(f"Total causas encontradas: {len(causas)}")
            return causas

        except Exception as e:
            logger.error(f"Error obteniendo causas: {e}")
            return []

    async def _extraer_causa_de_fila(self, row, tipo: str, headers: List[str]) -> Optional[Causa]:
        """Extrae datos de una causa desde una fila de tabla usando los headers para mapear."""
        try:
            cells = await row.query_selector_all('td')
            if len(cells) < 4:
                return None

            # Extraer texto de cada celda
            datos = []
            for cell in cells:
                text = await cell.text_content()
                datos.append(text.strip() if text else '')

            # Crear diccionario mapeando header -> valor
            # El primer elemento suele ser la lupa (sin header o header vacío)
            data_map = {}
            for i, header in enumerate(headers):
                if i < len(datos):
                    header_clean = header.lower().strip()
                    data_map[header_clean] = datos[i]

            # Buscar RIT en diferentes posibles nombres de columna
            rit = data_map.get('rit', '') or data_map.get('rol', '') or data_map.get('causa', '')
            if not rit and len(datos) > 1:
                rit = datos[1]  # Fallback al segundo elemento

            if not rit:
                return None

            # Buscar otros campos con diferentes nombres posibles
            ruc = data_map.get('ruc', '') or data_map.get('ruc causa', '')

            tribunal = (data_map.get('tribunal', '') or
                       data_map.get('corte', '') or
                       data_map.get('juzgado', ''))

            caratulado = (data_map.get('caratulado', '') or
                         data_map.get('carátula', '') or
                         data_map.get('caratula', '') or
                         data_map.get('partes', ''))

            fecha = (data_map.get('fecha ingreso', '') or
                    data_map.get('fecha', '') or
                    data_map.get('f. ingreso', '') or
                    data_map.get('ingreso', ''))

            estado = (data_map.get('estado', '') or
                     data_map.get('estado causa', '') or
                     data_map.get('estado actual', ''))

            # Log para debug
            logger.debug(f"Headers: {headers}")
            logger.debug(f"Datos: {datos}")
            logger.debug(f"Mapeado - RIT: {rit}, Tribunal: {tribunal}, Estado: {estado}")

            # Crear causa con datos básicos
            causa = Causa(
                tipo=tipo,
                rit=rit,
                ruc=ruc,
                tribunal=tribunal,
                caratulado=caratulado,
                fecha_ingreso=fecha,
                estado=estado
            )

            return causa
        except Exception as e:
            logger.debug(f"Error extrayendo fila: {e}")
            return None

    async def get_detalle_causa(self, causa: Causa) -> Causa:
        """
        Obtiene el detalle completo de una causa incluyendo actuaciones.

        Args:
            causa: Causa con datos básicos

        Returns:
            Causa con todos los detalles y actuaciones
        """
        try:
            logger.info(f"Obteniendo detalle de {causa.rit} ({causa.tipo})...")

            # Primero cerrar cualquier modal abierto
            await self._cerrar_todos_modales()
            await asyncio.sleep(1)

            # Navegar a la pestaña correcta del tipo de causa
            tab_found = False
            tab_selectors = [
                f'a.nav-link:has-text("{causa.tipo}")',
                f'a:has-text("{causa.tipo}")',
                f'li:has-text("{causa.tipo}") a',
                f'[role="tab"]:has-text("{causa.tipo}")'
            ]

            for selector in tab_selectors:
                try:
                    tab = await self.page.query_selector(selector)
                    if tab:
                        await tab.click()
                        await asyncio.sleep(2)
                        tab_found = True
                        logger.debug(f"Tab {causa.tipo} encontrada con selector: {selector}")
                        break
                except:
                    continue

            if not tab_found:
                logger.warning(f"No se pudo navegar a la pestaña {causa.tipo}")

            # Buscar la fila de esta causa y hacer clic en la lupa
            causa_encontrada = False
            rows = await self.page.query_selector_all('table:visible tbody tr')

            for row in rows:
                cells = await row.query_selector_all('td')
                if len(cells) > 1:
                    # Buscar el RIT en todas las celdas
                    for cell in cells:
                        cell_text = await cell.text_content()
                        if cell_text and causa.rit in cell_text:
                            # Hacer clic en la primera celda (lupa) o en un botón de ver detalle
                            first_cell = await row.query_selector('td:first-child')
                            detail_btn = await row.query_selector('button, a.btn, [data-toggle="modal"]')

                            if detail_btn:
                                await detail_btn.click()
                            elif first_cell:
                                await first_cell.click()

                            await asyncio.sleep(3)
                            causa_encontrada = True
                            break
                    if causa_encontrada:
                        break

            if not causa_encontrada:
                logger.warning(f"No se encontró la fila para {causa.rit}")
                return causa

            # Extraer datos del modal de detalle
            await self._extraer_detalle_modal(causa)

            # Cerrar modal
            await self._cerrar_todos_modales()
            await asyncio.sleep(1)

            return causa

        except Exception as e:
            logger.error(f"Error obteniendo detalle de {causa.rit}: {e}")
            # Intentar cerrar modal en caso de error
            await self._cerrar_todos_modales()
            return causa

    async def _cerrar_todos_modales(self):
        """Cierra todos los modales abiertos."""
        try:
            await asyncio.sleep(1)
            # Buscar botones de cerrar en modales visibles
            close_buttons = await self.page.query_selector_all('.modal.show button.close, .modal.in button.close, .modal.show .btn-close, [data-dismiss="modal"]')
            for btn in close_buttons:
                try:
                    if await btn.is_visible():
                        await btn.click()
                        await asyncio.sleep(0.5)
                except:
                    pass

            # También presionar Escape por si acaso
            await self.page.keyboard.press('Escape')
            await asyncio.sleep(0.5)
        except:
            pass

    async def _extraer_detalle_modal(self, causa: Causa):
        """Extrae información del modal de detalle de causa."""
        try:
            # Esperar que el modal cargue
            await asyncio.sleep(2)

            # Extraer datos del encabezado
            content = await self.page.content()

            # Procedimiento
            proc_match = re.search(r'Proc\.?:?\s*</?\w*>?\s*([^<]+)', content)
            if proc_match:
                causa.procedimiento = proc_match.group(1).strip()

            # Etapa
            etapa_match = re.search(r'Etapa:?\s*</?\w*>?\s*([^<]+)', content)
            if etapa_match:
                causa.etapa = etapa_match.group(1).strip()

            # Estado administrativo
            est_match = re.search(r'Est\.\s*Adm\.?:?\s*</?\w*>?\s*([^<]+)', content)
            if est_match:
                causa.estado_admin = est_match.group(1).strip()

            # Extraer actuaciones de la tabla de Historia
            await self._extraer_actuaciones(causa)

        except Exception as e:
            logger.debug(f"Error extrayendo detalle: {e}")

    async def _extraer_actuaciones(self, causa: Causa):
        """Extrae el historial de actuaciones de una causa."""
        try:
            # Esperar a que el modal cargue completamente
            await asyncio.sleep(2)

            # Intentar varios selectores para encontrar la tabla de actuaciones
            selectors = [
                '.modal.show table tbody tr',
                '.modal:visible table tbody tr',
                '.modal table tbody tr',
                '#modalDetalle table tbody tr',
                '[role="dialog"] table tbody tr'
            ]

            rows = []
            for selector in selectors:
                rows = await self.page.query_selector_all(selector)
                if len(rows) > 0:
                    logger.debug(f"Encontradas {len(rows)} filas con selector: {selector}")
                    break

            if not rows:
                logger.warning(f"No se encontraron actuaciones para {causa.rit}")
                return

            for row in rows:
                cells = await row.query_selector_all('td')
                if len(cells) >= 5:
                    datos = []
                    for cell in cells:
                        text = await cell.text_content()
                        datos.append(text.strip() if text else '')

                    # Verificar si tiene documento PDF
                    tiene_doc = await row.query_selector('a[href*=".pdf"], .fa-file-pdf, img[src*="pdf"]')

                    # Los índices pueden variar, intentamos extraer lo más importante
                    actuacion = Actuacion(
                        folio=datos[0] if datos[0] else '',
                        etapa=datos[3] if len(datos) > 3 else '',
                        tramite=datos[4] if len(datos) > 4 else '',
                        descripcion=datos[5] if len(datos) > 5 else datos[4] if len(datos) > 4 else '',
                        fecha=datos[6] if len(datos) > 6 else datos[5] if len(datos) > 5 else '',
                        foja=datos[7] if len(datos) > 7 else '',
                        tiene_documento=tiene_doc is not None
                    )

                    if actuacion.folio or actuacion.descripcion:
                        causa.actuaciones.append(actuacion)

            # Establecer última actuación
            if causa.actuaciones:
                ultima = causa.actuaciones[0]  # La primera es la más reciente
                causa.ultima_actuacion = ultima.descripcion
                causa.fecha_ultima_actuacion = ultima.fecha

            logger.info(f"  {len(causa.actuaciones)} actuaciones encontradas para {causa.rit}")

        except Exception as e:
            logger.error(f"Error extrayendo actuaciones de {causa.rit}: {e}")

    async def sync_causas_completas(self, rut: str, password: str) -> Dict[str, Any]:
        """
        Proceso completo: login, obtener causas y sus detalles.

        Args:
            rut: RUT sin puntos ni guión
            password: Contraseña ClaveÚnica

        Returns:
            Dict con causas completas o error
        """
        # Modo demo
        if self.DEMO_MODE:
            logger.info("Modo DEMO - retornando datos de ejemplo")
            return self._get_demo_data()

        try:
            # Inicializar browser (headless=True para producción)
            if not await self.init_browser(headless=True):
                return {'success': False, 'error': 'No se pudo inicializar el navegador'}

            # Login
            if not await self.login(rut, password):
                return {'success': False, 'error': 'Error en autenticación'}

            # Obtener lista de causas
            causas = await self.get_causas()

            # Obtener detalle de cada causa
            for causa in causas:
                await self.get_detalle_causa(causa)

            return {
                'success': True,
                'causas': [c.to_dict() for c in causas],
                'total': len(causas),
                'sync_date': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error en sincronización: {e}")
            return {'success': False, 'error': str(e)}
        finally:
            await self.close()

    def _get_demo_data(self) -> Dict[str, Any]:
        """Retorna datos de demostración."""
        demo_causas = [
            {
                'tipo': 'Civil',
                'rit': 'C-5521-2024',
                'ruc': '',
                'tribunal': '4º Juzgado Civil de San Miguel',
                'caratulado': 'CHANDÍA/CHANDÍA',
                'fecha_ingreso': '20/11/2024',
                'estado': 'Concluido',
                'procedimiento': 'Designación Árbitro',
                'etapa': '5 Terminada',
                'ubicacion': 'Digital',
                'estado_admin': 'Sin archivar',
                'ultima_actuacion': 'Acepta cargo',
                'fecha_ultima_actuacion': '15/01/2026',
                'actuaciones': [
                    {'folio': '53', 'etapa': 'Impugnación', 'tramite': '', 'descripcion': 'Acepta cargo', 'fecha': '15/01/2026', 'foja': '46', 'tiene_documento': True},
                    {'folio': '52', 'etapa': 'Impugnación', 'tramite': '(CER)Certificacion', 'descripcion': 'Certifica sent. definitiva ejecutoriada', 'fecha': '12/01/2026', 'foja': '45', 'tiene_documento': True},
                    {'folio': '51', 'etapa': 'Impugnación', 'tramite': 'Resolución', 'descripcion': 'Certifíquese ejecutoria de sentencia', 'fecha': '09/01/2026', 'foja': '44', 'tiene_documento': True},
                ]
            },
            {
                'tipo': 'Penal',
                'rit': 'Ordinaria-318-2021',
                'ruc': '2100189812-1',
                'tribunal': 'Juzgado de Letras y Garantía de Pichilemu',
                'caratulado': 'MP C/ ESTEBAN ALONSO FIGUEROA FUENTES',
                'fecha_ingreso': '27/02/2021',
                'estado': 'Fallada o Concluida',
                'procedimiento': 'Ordinario',
                'etapa': 'Terminada',
                'ubicacion': '',
                'estado_admin': '',
                'ultima_actuacion': 'Sentencia definitiva',
                'fecha_ultima_actuacion': '15/06/2021',
                'actuaciones': []
            }
        ]

        return {
            'success': True,
            'causas': demo_causas,
            'total': len(demo_causas),
            'sync_date': datetime.now().isoformat(),
            'demo_mode': True
        }


# Función auxiliar para uso síncrono
def sync_causas(rut: str, password: str) -> Dict[str, Any]:
    """
    Versión síncrona para sincronizar causas.
    """
    scraper = PJUDScraper()
    return asyncio.run(scraper.sync_causas_completas(rut, password))


# Para pruebas
if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 3:
        rut = sys.argv[1]
        password = sys.argv[2]
    else:
        print("Uso: python pjud_scraper.py <rut> <password>")
        print("Ejemplo: python pjud_scraper.py 209769441 'MiClave123'")
        sys.exit(1)

    print("Iniciando sincronización con Poder Judicial...")
    result = sync_causas(rut, password)
    print(json.dumps(result, indent=2, ensure_ascii=False))
