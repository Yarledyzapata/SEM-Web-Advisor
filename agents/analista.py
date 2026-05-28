
import requests
from bs4 import BeautifulSoup
import time


def analizar_sitio(url):

    inicio = time.time()

    respuesta = requests.get(url)

    fin = time.time()

    tiempo_respuesta = fin - inicio

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
    # PORCENTAJE DE ERROR
    # =====================================

    porcentaje_error = 0

    if total_imagenes > 0:

        porcentaje_error = (

            imagenes_sin_alt /

            total_imagenes

        ) * 100

    # =====================================
    # TITLE SEO
    # =====================================

    titulo = "No encontrado"

    if soup.title:

        titulo = soup.title.string

    # =====================================
    # META DESCRIPTION
    # =====================================

    descripcion = "No encontrada"

    meta = soup.find(
        "meta",
        attrs={
            "name": "description"
        }
    )

    if meta and meta.get("content"):

        descripcion = meta.get("content")

    # =====================================
    # H1
    # =====================================

    h1 = soup.find_all("h1")

    total_h1 = len(h1)

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

    # =====================================
    # OPEN GRAPH
    # =====================================

    og = soup.find(
        "meta",
        attrs={
            "property": "og:title"
        }
    )

    open_graph = "Sí" if og else "No"

    # =====================================
    # ROBOTS
    # =====================================

    robots_url = url.rstrip("/") + "/robots.txt"

    try:

        robots = requests.get(robots_url)

        robots_txt = "Sí" if robots.status_code == 200 else "No"

    except:

        robots_txt = "No"

    # =====================================
    # SITEMAP
    # =====================================

    sitemap_url = url.rstrip("/") + "/sitemap.xml"

    try:

        sitemap = requests.get(sitemap_url)

        sitemap_xml = "Sí" if sitemap.status_code == 200 else "No"

    except:

        sitemap_xml = "No"

    # =====================================
    # RESULTADO
    # =====================================

    return {

        "url": url,

        "tiempo": round(
            tiempo_respuesta,
            2
        ),

        "errores": imagenes_sin_alt,

        "porcentaje_error": round(
            porcentaje_error,
            2
        ),

        "imagenes": total_imagenes,

        "titulo": titulo,

        "descripcion": descripcion,

        "h1": total_h1,

        "links": total_links,

        "scripts": total_scripts,

        "open_graph": open_graph,

        "robots": robots_txt,

        "sitemap": sitemap_xml
    }
