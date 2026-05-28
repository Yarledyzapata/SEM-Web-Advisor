from database.conexion import coleccion
import json


def generar_reporte(
        
        url,
        estado,
        prioridad):

    reporte = {

        "@context":
        "http://schema.org/",

        "@type":
        "AuditReport",

        "site":
        url,

        "result": {

    "status":
    estado,

    "priority":
    prioridad,

    "recommendations":
    obtener_recomendaciones(
        estado
    )
}
    }

    return reporte


# =====================================
# GUARDAR JSON
# =====================================

def guardar_reporte(
        reporte):

    with open(
        "reporte.json",
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            reporte,
            archivo,
            indent=4,
            ensure_ascii=False
        )

    print(
        "\nReporte guardado correctamente"
    )

    # =====================================
# GUARDAR EN MONGODB
# =====================================

def guardar_mongodb(reporte):

    coleccion.insert_one(reporte)

    print(
        "Reporte guardado en MongoDB"
    )


# =====================================
# RECOMENDACIONES SEMÁNTICAS
# =====================================

def obtener_recomendaciones(estado):

    if estado == "Crítico":

        return [
            "Corrección inmediata requerida",
            "Optimizar accesibilidad urgentemente",
            "Reducir errores críticos"
        ]

    elif estado == "Regular":

        return [
            "Mejorar imágenes sin ALT",
            "Optimizar tiempos de carga",
            "Revisión preventiva recomendada"
        ]

    else:

        return [
            "Sitio estable",
            "Mantenimiento preventivo periódico"
        ]