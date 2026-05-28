import requests

from bs4 import BeautifulSoup

import time

# =====================================
# ANALIZAR SITIO
# =====================================

def analizar_sitio(url):

    inicio = time.time()

    respuesta = requests.get(url)

    fin = time.time()

    tiempo_respuesta = round(
        fin - inicio,
        2
    )

    soup = BeautifulSoup(
        respuesta.text,
        'html.parser'
    )

    # =====================================
    # IMÁGENES
    # =====================================

    imagenes = soup.find_all('img')

    total_imagenes = len(imagenes)

    imagenes_sin_alt = 0

    for img in imagenes:

        if not img.get('alt'):

            imagenes_sin_alt += 1

    # =====================================
    # TÍTULO SEO
    # =====================================

    titulo = soup.title.string.strip() \
        if soup.title else \
        "No encontrado"

    # =====================================
    # META DESCRIPTION
    # =====================================

    meta_description = soup.find(
        "meta",
        attrs={
            "name": "description"
        }
    )

    descripcion = (
        meta_description.get("content")
        if meta_description
        else "No encontrada"
    )

    # =====================================
    # H1
    # =====================================

    h1_tags = soup.find_all("h1")

    total_h1 = len(h1_tags)

    # =====================================
    # LINKS
    # =====================================

    links = soup.find_all("a")

    total_links = len(links)

    # =====================================
    # SCRIPTS
    # =====================================

    scripts = soup.find_all("script")

    total_scripts = len(scripts)


    porcentaje_error = 0

    if total_imagenes > 0:

        porcentaje_error = (
            imagenes_sin_alt
            /
            total_imagenes
        ) * 100

    # =====================================
    # RESULTADOS
    # =====================================


    return {

        "url": url,

        "tiempo":
        tiempo_respuesta,

        "errores":
        imagenes_sin_alt,

        "imagenes":
        total_imagenes,

        "porcentaje_error":
        round(porcentaje_error, 2),

        "titulo":
        titulo,

        "descripcion":
        descripcion,

        "h1":
        total_h1,

        "links":
        total_links,

        "scripts":
        total_scripts
    }