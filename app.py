from flask import Flask
from flask import render_template
from flask import request

from agents.analista import analizar_sitio
from agents.experto import evaluar_sitio
from database.conexion import coleccion

import json

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import letter

app = Flask(__name__)

# =====================================
# INICIO
# =====================================

@app.route('/')

def inicio():

    return render_template(
        'index.html'
    )

# =====================================
# ANALIZAR
# =====================================

@app.route('/analizar',
           methods=['POST'])
def analizar():

    url = request.form['url']

    # =========================
    # AGENTE ANALISTA
    # =========================

    datos = analizar_sitio(url)

    # =========================
    # AGENTE EXPERTO
    # =========================

    resultado = evaluar_sitio(

        datos["tiempo"],

        datos["porcentaje_error"]
    )

    # =========================
    # DOCUMENTO MONGODB
    # =========================

    documento = {

        "@context": "http://schema.org/",

        "@type": "AuditReport",

        "site": url,

        "result": {

            "status": resultado["estado"],

            "priority": resultado["prioridad"],

            "nivel": resultado["nivel"],

            "errores": datos["errores"],

            "tiempo": datos["tiempo"],

            "tags": [

                "SEO",

                "Accesibilidad",

                "Rendimiento"
            ]
        }
    }

    coleccion.insert_one(documento)

    # =========================
    # RECOMENDACIONES
    # =========================

    from agents.notificador import (
        obtener_recomendaciones
    )

    recomendaciones = obtener_recomendaciones(
        resultado["estado"]
    )

    # =========================
    # HISTORIAL
    # =========================

    historial = list(

        coleccion.find().sort(
            "_id",
            -1
        ).limit(5)

    )

    # =========================
    # JSON BONITO
    # =========================

    json_bonito = json.dumps(

        historial[0],

        indent=4,

        default=str,

        ensure_ascii=False
    )

    # =========================
    # PDF
    # =========================

    pdf_path = "static/reports/reporte.pdf"

    doc = SimpleDocTemplate(

        pdf_path,

        pagesize=letter
    )

    styles = getSampleStyleSheet()

    contenido = []

    contenido.append(

        Paragraph(
            "SEM-Web-Advisor",
            styles['Title']
        )
    )

    contenido.append(
        Spacer(1, 20)
    )

    contenido.append(

        Paragraph(
            f"<b>URL:</b> {url}",
            styles['BodyText']
        )
    )

    contenido.append(

        Paragraph(
            f"<b>Estado:</b> {resultado['estado']}",
            styles['BodyText']
        )
    )

    contenido.append(

        Paragraph(
            f"<b>Nivel Difuso:</b> {resultado['nivel']}",
            styles['BodyText']
        )
    )

    contenido.append(

        Paragraph(
            f"<b>Errores:</b> {datos['errores']}",
            styles['BodyText']
        )
    )

    contenido.append(

        Paragraph(
            f"<b>Tiempo:</b> {datos['tiempo']} segundos",
            styles['BodyText']
        )
    )

    contenido.append(
        Spacer(1, 20)
    )

    contenido.append(

        Paragraph(
            "<b>Información SEO</b>",
            styles['Heading2']
        )
    )

    contenido.append(

        Paragraph(
            f"Título: {datos['titulo']}",
            styles['BodyText']
        )
    )

    contenido.append(

        Paragraph(
            f"Meta descripción: {datos['descripcion']}",
            styles['BodyText']
        )
    )

    contenido.append(

        Paragraph(
            f"Imágenes: {datos['imagenes']}",
            styles['BodyText']
        )
    )

    contenido.append(
        Spacer(1, 20)
    )

    contenido.append(

        Paragraph(
            "<b>Recomendaciones</b>",
            styles['Heading2']
        )
    )

    for r in recomendaciones:

        contenido.append(

            Paragraph(
                f"• {r}",
                styles['BodyText']
            )
        )

    doc.build(contenido)

    # =========================
    # HTML
    # =========================

    return render_template(

        'index.html',

        url=url,

        tiempo=datos["tiempo"],

        errores=datos["errores"],

        titulo=datos["titulo"],

        descripcion=datos["descripcion"],

        h1=datos["h1"],

        links=datos["links"],

        scripts=datos["scripts"],

        imagenes=datos["imagenes"],

        estado=resultado["estado"],

        nivel=resultado["nivel"],

        prioridad=resultado["prioridad"],

        recomendaciones=recomendaciones,

        historial=historial,

        json_bonito=json_bonito,

        pdf="reports/reporte.pdf"
    )

# =====================================

if __name__ == '__main__':

    app.run(debug=True)