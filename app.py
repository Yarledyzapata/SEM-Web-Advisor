from flask import Flask
from flask import render_template
from flask import request

from agents.analista import analizar_sitio
from agents.experto import evaluar_sitio
from database.conexion import coleccion

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.graphics.shapes import Drawing, String

from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

import json

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import letter

from reportlab.lib import colors

from datetime import datetime

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

    print("\n===== DATOS DEL ANALISTA =====")
    print(datos)

    resultado = evaluar_sitio(
        datos["tiempo"],
        datos["porcentaje_error"]
    )

    print("\n===== RESULTADO DEL EXPERTO =====")
    print(resultado)

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

    # ==============================================================
    # PALETA DE COLORES CENTRALIZADOS
    # ==============================================================

    AZUL_OSCURO  = colors.HexColor("#1e3a8a")
    AZUL_MEDIO   = colors.HexColor("#2563eb")
    GRIS_FONDO   = colors.HexColor("#f8fafc")
    GRIS_BORDE   = colors.HexColor("#cbd5e1")
    GRIS_CLARO   = colors.HexColor("#f1f5f9")
    AMARILLO_BG  = colors.HexColor("#fefce8")
    AMARILLO_BR  = colors.HexColor("#ca8a04")
    ROJO         = colors.HexColor("#dc2626")
    VERDE        = colors.HexColor("#16a34a")
    AMARILLO     = colors.HexColor("#eab308")
    PURPURA      = colors.HexColor("#9333ea")
    BLANCO       = colors.white
    TEXTO_GRIS   = colors.HexColor("#475569")


    # ==============================================================
    # HELPER: color según estado
    # ==============================================================

    def _color_estado(estado: str) -> colors.HexColor:
        mapa = {
            "Crítico": ROJO,
            "Regular": AMARILLO,
        }
        return mapa.get(estado, VERDE)


    # ==============================================================
    # HEADER / FOOTER (se aplica a cada página)
    # ==============================================================

    def _build_header_footer(fecha: str, url: str):
        """Devuelve una función compatible con onFirstPage/onLaterPages."""

        PAGE_W, PAGE_H = letter

        def _draw(canvas, doc):
            canvas.saveState()

            # ── Header ──────────────────────────────────────────────
            canvas.setFillColor(AZUL_OSCURO)
            canvas.rect(0, PAGE_H - 2 * cm, PAGE_W, 2 * cm, fill=1, stroke=0)

            canvas.setFillColor(BLANCO)
            canvas.setFont("Helvetica-Bold", 15)
            canvas.drawString(1.2 * cm, PAGE_H - 1.25 * cm, "SEM-Web-Advisor")

            canvas.setFont("Helvetica", 8)
            canvas.drawRightString(
                PAGE_W - 1.2 * cm,
                PAGE_H - 0.9 * cm,
                f"Auditoría: {url[:60]}{'…' if len(url) > 60 else ''}",
            )
            canvas.drawRightString(
                PAGE_W - 1.2 * cm,
                PAGE_H - 1.5 * cm,
                fecha,
            )

            # ── Footer ──────────────────────────────────────────────
            canvas.setFillColor(GRIS_CLARO)
            canvas.rect(0, 0, PAGE_W, 1.2 * cm, fill=1, stroke=0)

            canvas.setFillColor(TEXTO_GRIS)
            canvas.setFont("Helvetica", 8)
            canvas.drawString(
                1.2 * cm,
                0.45 * cm,
                "Generado automáticamente por SEM-Web-Advisor",
            )
            canvas.drawRightString(
                PAGE_W - 1.2 * cm,
                0.45 * cm,
                f"Página {doc.page}",
            )

            canvas.restoreState()

        return _draw


    # ==============================================================
    # ESTILOS PERSONALIZADOS
    # ==============================================================

    def _build_styles():
        base = getSampleStyleSheet()

        estilos = {}

        estilos["subtitulo"] = ParagraphStyle(
            "subtitulo",
            parent=base["BodyText"],
            fontSize=11,
            textColor=TEXTO_GRIS,
            alignment=TA_CENTER,
            spaceAfter=4,
        )

        estilos["meta"] = ParagraphStyle(
            "meta",
            parent=base["BodyText"],
            fontSize=10,
            textColor=TEXTO_GRIS,
            spaceAfter=3,
        )

        estilos["score"] = ParagraphStyle(
            "score",
            parent=base["BodyText"],
            fontSize=48,
            textColor=AZUL_OSCURO,
            alignment=TA_CENTER,
            leading=56,
            spaceAfter=0,
        )

        estilos["score_label"] = ParagraphStyle(
            "score_label",
            parent=base["BodyText"],
            fontSize=11,
            textColor=TEXTO_GRIS,
            alignment=TA_CENTER,
            spaceAfter=12,
        )

        estilos["heading"] = ParagraphStyle(
            "heading",
            parent=base["Heading2"],
            fontSize=13,
            textColor=AZUL_OSCURO,
            spaceBefore=14,
            spaceAfter=8,
            borderPadding=(0, 0, 4, 0),
        )

        estilos["recomendacion"] = ParagraphStyle(
            "recomendacion",
            parent=base["BodyText"],
            fontSize=10,
            backColor=AMARILLO_BG,
            borderColor=AMARILLO_BR,
            borderWidth=1,
            borderPadding=8,
            leftIndent=8,
            spaceAfter=6,
        )

        estilos["conclusion"] = ParagraphStyle(
            "conclusion",
            parent=base["BodyText"],
            fontSize=10,
            textColor=TEXTO_GRIS,
            leading=16,
            spaceAfter=6,
        )

        estilos["footer_text"] = ParagraphStyle(
            "footer_text",
            parent=base["Italic"],
            fontSize=9,
            textColor=TEXTO_GRIS,
            alignment=TA_CENTER,
        )

        return estilos


    # ==============================================================
    # SECCIÓN: badge de estado
    # ==============================================================

    def _badge_estado(estado: str, estilos: dict) -> Table:
        """Tabla de 1 celda que actúa como badge con color de fondo."""
        color = _color_estado(estado)

        estilo_badge = ParagraphStyle(
            "badge",
            fontSize=13,
            textColor=BLANCO,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
        )

        t = Table(
            [[Paragraph(f"Estado: {estado}", estilo_badge)]],
            colWidths=[8 * cm],
        )
        t.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), color),
                ("TOPPADDING",    (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING",   (0, 0), (-1, -1), 20),
                ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
                ("ALIGN",  (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROUNDEDCORNERS", [6, 6, 6, 6]),
            ])
        )

        # Centrar la tabla envolviéndola en otra tabla
        wrapper = Table([[t]], colWidths=[letter[0] - 3 * cm])
        wrapper.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
        return wrapper


    # ==============================================================
    # SECCIÓN: tabla de métricas
    # ==============================================================

    def _tabla_metricas(resultado: dict, datos: dict) -> Table:
        filas = [
            ["Campo", "Valor"],
            ["Estado",        resultado["estado"]],
            ["Nivel Difuso",  str(resultado["nivel"])],
            ["Errores ALT",   str(datos["errores"])],
            ["Tiempo de carga", f'{datos["tiempo"]} s'],
            ["Total imágenes", str(datos["imagenes"])],
            ["Etiquetas H1",  str(datos["h1"])],
            ["Open Graph",    datos["open_graph"]],
            ["Robots.txt",    datos["robots"]],
            ["Sitemap.xml",   datos["sitemap"]],
        ]

        col_widths = [6 * cm, 9 * cm]
        tabla = Table(filas, colWidths=col_widths, repeatRows=1)

        # Zebra striping
        row_styles = []
        for i in range(1, len(filas)):
            bg = BLANCO if i % 2 == 0 else GRIS_FONDO
            row_styles.append(("BACKGROUND", (0, i), (-1, i), bg))

        tabla.setStyle(
            TableStyle([
                # Encabezado
                ("BACKGROUND",    (0, 0), (-1, 0), AZUL_OSCURO),
                ("TEXTCOLOR",     (0, 0), (-1, 0), BLANCO),
                ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE",      (0, 0), (-1, 0), 11),
                ("TOPPADDING",    (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                # Cuerpo
                ("FONTNAME",  (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE",  (0, 1), (-1, -1), 10),
                ("FONTNAME",  (0, 1), (0, -1), "Helvetica-Bold"),
                ("TEXTCOLOR", (0, 1), (0, -1), AZUL_OSCURO),
                # Grid
                ("GRID",       (0, 0), (-1, -1), 0.5, GRIS_BORDE),
                ("ROWBORDERS", (0, 0), (-1, -1), 0.5, GRIS_BORDE),
                # Padding
                ("LEFTPADDING",  (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING",   (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING",(0, 1), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                *row_styles,
            ])
        )

        return tabla


    # ==============================================================
    # SECCIÓN: gráfica de barras
    # ==============================================================

    def _grafica_barras(datos: dict) -> Drawing:
        con_alt  = datos["imagenes"] - datos["errores"]
        sin_alt  = datos["errores"]
        imagenes = datos["imagenes"]
        h1       = datos["h1"]

        drawing = Drawing(440, 240)

        # Título de la gráfica
        titulo = String(
            220, 228,
            "Resumen Visual de Métricas",
            fontName="Helvetica-Bold",
            fontSize=10,
            fillColor=AZUL_OSCURO,
            textAnchor="middle",
        )
        drawing.add(titulo)

        grafica = VerticalBarChart()
        grafica.x = 55
        grafica.y = 30
        grafica.width  = 330
        grafica.height = 160

        # Una serie por categoría (permite colores distintos)
        grafica.data = [
            [imagenes],
            [con_alt],
            [sin_alt],
            [h1],
        ]

        grafica.categoryAxis.categoryNames = [""]

        # Eje Y
        max_val = max(imagenes, con_alt, sin_alt, h1, 1)
        grafica.valueAxis.valueMin  = 0
        grafica.valueAxis.valueMax  = max_val + max(1, int(max_val * 0.15))
        grafica.valueAxis.valueStep = max(1, int(max_val / 5))
        grafica.valueAxis.labelTextFormat = "%d"
        grafica.valueAxis.labels.fontName = "Helvetica"
        grafica.valueAxis.labels.fontSize = 9

        # Colores por serie
        palette = [AZUL_MEDIO, VERDE, ROJO, PURPURA]
        for i, col in enumerate(palette):
            grafica.bars[i].fillColor   = col
            grafica.bars[i].strokeColor = BLANCO
            grafica.bars[i].strokeWidth = 0.5

        # Etiquetas de valor sobre cada barra
        grafica.barLabelFormat = "%d"
        grafica.barLabels.nudge    = 8
        grafica.barLabels.fontName = "Helvetica-Bold"
        grafica.barLabels.fontSize = 9
        grafica.barLabels.fillColor = TEXTO_GRIS

        grafica.groupSpacing = 2

        drawing.add(grafica)

        # Leyenda manual
        leyendas = [
            ("Total Imágenes", AZUL_MEDIO),
            ("Con ALT",        VERDE),
            ("Sin ALT",        ROJO),
            ("H1",             PURPURA),
        ]
        x_ley = 55
        for texto, col in leyendas:
            from reportlab.graphics.shapes import Rect
            drawing.add(Rect(x_ley, 8, 10, 10, fillColor=col, strokeColor=BLANCO, strokeWidth=0.5))
            drawing.add(String(x_ley + 13, 9, texto, fontName="Helvetica", fontSize=8, fillColor=TEXTO_GRIS))
            x_ley += 90

        return drawing


    # ==============================================================
    # FUNCIÓN PRINCIPAL
    # ==============================================================

    def generar_pdf(
        url: str,
        resultado: dict,
        datos: dict,
        recomendaciones: list[str],
        output_dir: str = "static/reports",
    ) -> str:
        """
        Genera el PDF de auditoría SEO y devuelve la ruta del archivo.

        Parámetros
        ----------
        url            : URL analizada.
        resultado      : dict con claves 'estado' y 'nivel'.
        datos          : dict con claves 'errores', 'tiempo', 'imagenes',
                        'h1', 'open_graph', 'robots', 'sitemap'.
        recomendaciones: lista de strings con las recomendaciones.
        output_dir     : carpeta de destino.
        """
        os.makedirs(output_dir, exist_ok=True)

        fecha    = datetime.now().strftime("%d/%m/%Y %H:%M")
        pdf_path = os.path.join(output_dir, f"reporte_{resultado['estado']}.pdf")

        # ── Documento ───────────────────────────────────────────────
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=3 * cm,       # deja espacio al header
            bottomMargin=2 * cm,    # deja espacio al footer
            title=f"Reporte SEO — {url}",
            author="SEM-Web-Advisor",
            subject="Auditoría SEO y Accesibilidad",
            creator="SEM-Web-Advisor v2.0",
        )

        estilos    = _build_styles()
        header_fn  = _build_header_footer(fecha, url)
        contenido  = []

        # ── Encabezado ──────────────────────────────────────────────
        contenido.append(
            Paragraph("Reporte Inteligente de Auditoría SEO y Accesibilidad", estilos["subtitulo"])
        )
        contenido.append(Spacer(1, 6))
        contenido.append(HRFlowable(width="100%", thickness=1, color=GRIS_BORDE))
        contenido.append(Spacer(1, 10))

        contenido.append(Paragraph(f"<b>Sitio analizado:</b> {url}", estilos["meta"]))
        contenido.append(Paragraph(f"<b>Fecha del análisis:</b> {fecha}", estilos["meta"]))
        contenido.append(Spacer(1, 20))

        # ── Score + badge ────────────────────────────────────────────
        contenido.append(Paragraph(f"<b>{resultado['nivel']}</b>", estilos["score"]))
        contenido.append(Paragraph("Nivel Difuso", estilos["score_label"]))
        contenido.append(_badge_estado(resultado["estado"], estilos))
        contenido.append(Spacer(1, 24))

        # ── Tabla de métricas ───────────────────────────────────────
        contenido.append(HRFlowable(width="100%", thickness=0.5, color=GRIS_BORDE))
        contenido.append(Paragraph("Resumen Técnico", estilos["heading"]))
        contenido.append(_tabla_metricas(resultado, datos))
        contenido.append(Spacer(1, 20))

        # ── Gráfica ─────────────────────────────────────────────────
        contenido.append(HRFlowable(width="100%", thickness=0.5, color=GRIS_BORDE))
        contenido.append(Paragraph("Resumen Visual del Sitio", estilos["heading"]))
        contenido.append(_grafica_barras(datos))
        contenido.append(Spacer(1, 20))

        # ── Recomendaciones ─────────────────────────────────────────
        contenido.append(HRFlowable(width="100%", thickness=0.5, color=GRIS_BORDE))
        contenido.append(Paragraph("Recomendaciones", estilos["heading"]))

        if recomendaciones:
            for r in recomendaciones:
                contenido.append(Paragraph(f"⚠ {r}", estilos["recomendacion"]))
        else:
            contenido.append(
                Paragraph("No se encontraron recomendaciones adicionales.", estilos["conclusion"])
            )

        contenido.append(Spacer(1, 20))

        # ── Conclusión ──────────────────────────────────────────────
        contenido.append(HRFlowable(width="100%", thickness=0.5, color=GRIS_BORDE))
        contenido.append(Paragraph("Conclusión Ejecutiva", estilos["heading"]))
        contenido.append(
            Paragraph(
                f"El sitio analizado obtuvo una puntuación de <b>{resultado['nivel']}</b> "
                f"y fue clasificado como <b>{resultado['estado']}</b>. "
                f"Se detectaron <b>{datos['errores']}</b> errores de accesibilidad relacionados "
                f"con imágenes sin atributo ALT. Se recomienda aplicar las acciones sugeridas "
                f"para mejorar la experiencia del usuario, el posicionamiento SEO y el "
                f"rendimiento general del sitio web.",
                estilos["conclusion"],
            )
        )

        contenido.append(Spacer(1, 30))

        # ── Construir ────────────────────────────────────────────────
        doc.build(
            contenido,
            onFirstPage=header_fn,
            onLaterPages=header_fn,
        )

        return pdf_path


    # ==============================================================
    # EJEMPLO DE USO
    # ==============================================================

    if __name__ == "__main__":
        url_prueba = "https://mi-sitio-ejemplo.com"

        resultado_prueba = {
            "estado": "Regular",
            "nivel":  0.62,
        }

        datos_prueba = {
            "errores":    8,
            "tiempo":     2.4,
            "imagenes":  25,
            "h1":         2,
            "open_graph": "Sí",
            "robots":     "Sí",
            "sitemap":    "No",
        }

        recomendaciones_prueba = [
            "Añadir atributo ALT a las 8 imágenes que carecen de él.",
            "Revisar el tiempo de carga: 2.4 s supera el umbral recomendado de 2 s.",
            "Solo se detectó 1 etiqueta H1; asegúrate de que sea única y descriptiva.",
            "El sitemap.xml no fue encontrado. Publícalo en /sitemap.xml.",
            "Incluir metaetiquetas Open Graph para mejorar la vista en redes sociales.",
        ]

        ruta = generar_pdf(
            url_prueba,
            resultado_prueba,
            datos_prueba,
            recomendaciones_prueba,
            output_dir=".",
        )
        print(f"PDF generado en: {ruta}")

    # =========================
    # HTML
    # =========================

    ruta_pdf = generar_pdf(
        url,
        resultado,
        datos,
        recomendaciones
    )

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

        pdf=f"reports/reporte_{resultado['estado']}.pdf"


    )

    

# =====================================

if __name__ == '__main__':

    app.run(debug=True)