"""Descarga Chrome for Testing y Brave oficiales dentro del entorno virtual."""
import io
import json
import stat
import sys
import urllib.request
import zipfile
from pathlib import Path

DESTINO = Path(sys.prefix) / 'navegadores'

def descargar(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'ep02-browser-check'})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()

def extraer(url, carpeta):
    print(f'Descargando {carpeta.name}...', flush=True)
    carpeta.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(descargar(url))) as archivo:
        archivo.extractall(carpeta)
        for info in archivo.infolist():
            permisos = info.external_attr >> 16
            if permisos & stat.S_IXUSR:
                (carpeta / info.filename).chmod(permisos & 0o777)

chrome = json.loads(descargar('https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'))['channels']['Stable']
url = next(item['url'] for item in chrome['downloads']['chrome'] if item['platform'] == 'linux64')
extraer(url, DESTINO / 'chrome')
brave = json.loads(descargar('https://api.github.com/repos/brave/brave-browser/releases/latest'))
url = next(item['browser_download_url'] for item in brave['assets'] if item['name'].endswith('-linux-amd64.zip'))
extraer(url, DESTINO / 'brave')
print('Chrome:', chrome['version'])
print('Brave:', brave['tag_name'])
