import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# =========================
# VARIABLES DE ENTRADA
# =========================

# Tiempo de carga (0 a 10 segundos)
tiempo = ctrl.Antecedent(np.arange(0, 11, 1), 'tiempo')

# Errores de sintaxis (0 a 50)
errores = ctrl.Antecedent(np.arange(0, 51, 1), 'errores')

# =========================
# VARIABLE DE SALIDA
# =========================

# Nivel de mantenimiento
mantenimiento = ctrl.Consequent(np.arange(0, 11, 1), 'mantenimiento')

# =========================
# CONJUNTOS DIFUSOS
# =========================

# Tiempo
tiempo['rapido'] = fuzz.trimf(tiempo.universe, [0, 0, 5])
tiempo['moderado'] = fuzz.trimf(tiempo.universe, [2, 5, 8])
tiempo['lento'] = fuzz.trimf(tiempo.universe, [5, 10, 10])

# Errores
errores['pocos'] = fuzz.trimf(errores.universe, [0, 0, 25])
errores['muchos'] = fuzz.trimf(errores.universe, [15, 50, 50])

# Mantenimiento
mantenimiento['al_dia'] = fuzz.trimf(mantenimiento.universe, [0, 0, 4])
mantenimiento['preventivo'] = fuzz.trimf(mantenimiento.universe, [3, 5, 7])
mantenimiento['urgente'] = fuzz.trimf(mantenimiento.universe, [6, 10, 10])

# =========================
# REGLAS DIFUSAS
# =========================

regla1 = ctrl.Rule(tiempo['lento'] & errores['muchos'],
                   mantenimiento['urgente'])

regla2 = ctrl.Rule(tiempo['moderado'] & errores['pocos'],
                   mantenimiento['preventivo'])

regla3 = ctrl.Rule(tiempo['rapido'] & errores['pocos'],
                   mantenimiento['al_dia'])

# =========================
# SISTEMA DE CONTROL
# =========================

sistema_control = ctrl.ControlSystem([
    regla1,
    regla2,
    regla3
])

simulador = ctrl.ControlSystemSimulation(sistema_control)

# =========================
# DATOS DE PRUEBA
# =========================

simulador.input['tiempo'] = 8
simulador.input['errores'] = 40

# Ejecutar simulación
simulador.compute()

# Resultado numérico
resultado = simulador.output['mantenimiento']

print("Nivel numérico:", resultado)

# Interpretación
if resultado >= 6:
    print("Estado: Mantenimiento Urgente")

elif resultado >= 3:
    print("Estado: Mantenimiento Preventivo")

else:
    print("Estado: Sitio al día")

# Mostrar gráficas
tiempo.view()
errores.view()
mantenimiento.view()