from agents.analista import analizar_sitio

from agents.experto import evaluar_sitio

from agents.notificador import (
    generar_reporte,
    guardar_reporte,
    guardar_mongodb
)

# =====================================
# URL A ANALIZAR
# =====================================

url = "https://www.wikipedia.org"

# =====================================
# AGENTE ANALISTA
# =====================================

datos = analizar_sitio(url)

print("\n=== DATOS ANALISTA ===")

print(datos)

# =====================================
# AGENTE EXPERTO
# =====================================

resultado = evaluar_sitio(

    datos["tiempo"],

    datos["errores"]
)

print("\n=== RESULTADO EXPERTO ===")

print(resultado)

# =====================================
# PRIORIDAD
# =====================================

if resultado["estado"] == "Urgente":

    prioridad = "Alta"

elif resultado["estado"] == "Preventivo":

    prioridad = "Media"

else:

    prioridad = "Baja"

# =====================================
# AGENTE NOTIFICADOR
# =====================================

reporte = generar_reporte(

    url,

    resultado["estado"],

    prioridad
)

guardar_reporte(reporte)
guardar_mongodb(reporte)

print("\n=== REPORTE FINAL ===")

print(reporte)