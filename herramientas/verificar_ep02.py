"""Prueba los cinco ejercicios en Chrome y Brave, sin servidor externo."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

RAIZ = Path(__file__).resolve().parents[1]
BINARIOS = Path(sys.prefix) / 'navegadores'

def comprobar(browser):
    page = browser.new_page()
    errores = []
    page.on('pageerror', lambda error: errores.append(str(error)))
    def abrir(numero):
        page.goto((RAIZ / f'ej-ep02/ejercicio{numero}.html').as_uri())
        assert page.locator('img').evaluate_all('(imgs) => imgs.every(i => i.complete && i.naturalWidth > 0)'), 'Imagen sin cargar'

    abrir(1)
    page.locator('#modo').click()
    expect(page.locator('body')).to_have_class('oscuro')
    expect(page.locator('#modo')).to_have_text('Cambiar a modo claro')
    page.locator('#modo').click()
    expect(page.locator('body')).not_to_have_class('oscuro')
    print('  1: modo oscuro y claro OK')

    abrir(2)
    for longitud, rojo in [(265, False), (266, True), (280, True), (0, False)]:
        page.locator('#texto').fill('a' * longitud)
        expect(page.locator('#contador')).to_have_text(f'Quedan {280-longitud} caracteres.')
        assert ('error' in (page.locator('#contador').get_attribute('class') or '')) == rojo
    page.locator('#texto').fill(' ' * 280)
    page.locator('#texto').press('End')
    page.locator('#texto').press('a')
    assert len(page.locator('#texto').input_value()) == 280
    print('  2: contador, espacios y límite OK')

    abrir(3)
    expect(page.locator('#lista')).to_be_hidden()
    page.locator('#titulo').fill('Estudiar')
    page.get_by_role('button', name='Crear lista').click()
    expect(page.locator('#titulo-lista')).to_have_text('Estudiar')
    for i in range(10):
        page.locator('#tarea').fill(f'Tarea {i}')
        page.locator('#anadir').click()
    expect(page.locator('#tareas li')).to_have_count(10)
    expect(page.locator('#anadir')).to_be_disabled()
    expect(page.locator('#error')).not_to_be_empty()
    tarea = page.locator('#tareas li').first
    tarea.get_by_role('button', name='Completar', exact=True).click()
    expect(tarea.locator('span')).to_have_class('completada')
    tarea.get_by_role('button', name='Pendiente', exact=True).click()
    expect(tarea.locator('span')).not_to_have_class('completada')
    page.once('dialog', lambda dialog: dialog.dismiss())
    tarea.get_by_role('button', name='Eliminar').click()
    expect(page.locator('#tareas li')).to_have_count(10)
    page.once('dialog', lambda dialog: dialog.accept())
    tarea.get_by_role('button', name='Eliminar').click()
    expect(page.locator('#tareas li')).to_have_count(9)
    expect(page.locator('#anadir')).to_be_enabled()
    print('  3: creación, límite, completar y eliminar con confirmación OK')

    abrir(4)
    page.locator('#busqueda').fill('TECL')
    expect(page.locator('.producto:visible')).to_have_count(1)
    expect(page.locator('.producto:visible h2')).to_have_text('Teclado')
    page.locator('#busqueda').fill('inexistente')
    expect(page.locator('.producto:visible')).to_have_count(0)
    page.locator('#busqueda').fill('')
    expect(page.locator('.producto:visible')).to_have_count(3)
    print('  4: filtrado y restauración OK')

    abrir(5)
    page.get_by_role('button', name='Crear cuenta').click()
    expect(page.locator('#mensajes li')).to_have_count(4)
    expect(page.locator('#nombre')).to_be_focused()
    datos = {'nombre':'Alex', 'email':'alex@example.com', 'contrasena':'Abcdefg1', 'confirmacion':'otra'}
    for campo, valor in datos.items():
        page.locator('#'+campo).fill(valor)
    page.get_by_role('button', name='Crear cuenta').click()
    expect(page.locator('#mensajes li')).to_have_count(1)
    expect(page.locator('#confirmacion')).to_be_focused()
    for campo, invalido, valido in [('nombre','Ana','Alex'), ('email','correo','alex@example.com'), ('contrasena','abcdefgh','Abcdefg1')]:
        page.locator('#confirmacion').fill('Abcdefg1')
        page.locator('#'+campo).fill(invalido)
        page.get_by_role('button', name='Crear cuenta').click()
        expect(page.locator('#'+campo)).to_be_focused()
        page.locator('#'+campo).fill(valido)
    page.get_by_role('button', name='Crear cuenta').click()
    expect(page.locator('#mensajes')).to_have_text('Registro completado correctamente.')
    for campo in datos:
        expect(page.locator('#'+campo)).to_have_value('')
    page.locator('#nombre').fill('Alex')
    page.get_by_role('button', name='Limpiar').click()
    expect(page.locator('#nombre')).to_have_value('')
    expect(page.locator('#mensajes')).to_be_empty()
    assert not errores, errores
    print('  5: errores, foco, éxito y limpieza OK; sin errores JavaScript')
    page.close()

with sync_playwright() as playwright:
    for nombre, ruta in [('Chrome', BINARIOS/'chrome/chrome-linux64/chrome'), ('Brave', BINARIOS/'brave/brave')]:
        print(nombre, flush=True)
        browser = playwright.chromium.launch(executable_path=str(ruta), headless=True)
        print('  Versión:', browser.version)
        try:
            comprobar(browser)
        finally:
            browser.close()
