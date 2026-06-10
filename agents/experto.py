import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def evaluar_sitio(
        tiempo_respuesta,
        porcentaje_error
):

    # =========================
    # VARIABLES DIFUSAS
    # =========================

    tiempo = ctrl.Antecedent(
        np.arange(0, 11, 1),
        'tiempo'
    )

    errores_var = ctrl.Antecedent(
        np.arange(0, 101, 1),
        'errores'
    )

    mantenimiento = ctrl.Consequent(
        np.arange(0, 11, 1),
        'mantenimiento'
    )

    # =========================
    # TIEMPO
    # =========================

    tiempo['rapido'] = fuzz.trimf(
        tiempo.universe,
        [0, 0, 2]
    )

    tiempo['moderado'] = fuzz.trimf(
        tiempo.universe,
        [1, 3, 5]
    )

    tiempo['lento'] = fuzz.trimf(
        tiempo.universe,
        [4, 10, 10]
    )

    # =========================
    # ERRORES
    # =========================

    errores_var['pocos'] = fuzz.trimf(
        errores_var.universe,
        [0, 0, 20]
    )

    errores_var['moderados'] = fuzz.trimf(
        errores_var.universe,
        [10, 40, 70]
    )

    errores_var['muchos'] = fuzz.trimf(
        errores_var.universe,
        [60, 100, 100]
    )

    # =========================
    # MANTENIMIENTO
    # =========================

    mantenimiento['al_dia'] = fuzz.trimf(
        mantenimiento.universe,
        [0, 0, 3]
    )

    mantenimiento['preventivo'] = fuzz.trimf(
        mantenimiento.universe,
        [2, 5, 7]
    )

    mantenimiento['urgente'] = fuzz.trimf(
        mantenimiento.universe,
        [6, 10, 10]
    )

    # =========================
    # REGLAS
    # =========================

    regla1 = ctrl.Rule(
        tiempo['lento'] &
        errores_var['muchos'],
        mantenimiento['urgente']
    )

    regla2 = ctrl.Rule(
        tiempo['moderado'] |
        errores_var['moderados'],
        mantenimiento['preventivo']
    )

    regla3 = ctrl.Rule(
        tiempo['rapido'] &
        errores_var['pocos'],
        mantenimiento['al_dia']
    )

    # =========================
    # SISTEMA
    # =========================

    sistema = ctrl.ControlSystem([

        regla1,

        regla2,

        regla3
    ])

    simulador = ctrl.ControlSystemSimulation(
        sistema
    )

    # =========================
    # ENTRADAS
    # =========================

    simulador.input['tiempo'] = min(
        tiempo_respuesta,
        10
    )

    simulador.input['errores'] = min(
        porcentaje_error,
        100
    )

    simulador.compute()

    print("SALIDAS DIFUSAS:")
    print(simulador.output)

    resultado = simulador.output.get(
        'mantenimiento',
        0
    )

    # =========================
    # INTERPRETACIÓN
    # =========================

    if resultado >= 6:

        estado = "Crítico"
        prioridad = "Urgente"

    elif resultado >= 4:

        estado = "Regular"
        prioridad = "Media"

    else:

        estado = "Al día"
        prioridad = "Baja"

    return {

        "nivel": round(
            resultado,
            2
        ),

        "estado": estado,

        "prioridad": prioridad
    }
