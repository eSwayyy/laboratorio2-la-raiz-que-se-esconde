import numpy as np

import funciones as f
from metodos import (biseccion, falsa_posicion, punto_fijo,
                     secante, newton, newton_mejorado)

TOL = 1e-6
MAX_ITER = 100

DATA = "src/data/"

casos = [
    ("polinomica", f.polinomica, f.d_polinomica, f.dd_polinomica, f.g_polinomica, 1, 2, 1.5, 1.5213797068),
    ("raiz_doble", f.raiz_doble, f.d_raiz_doble, f.dd_raiz_doble, f.g_raiz_doble, 1, 3, 1.2, 2.0),
    ("logaritmica", f.logaritmica, f.d_logaritmica, f.dd_logaritmica, f.g_logaritmica, 2, 3, 2.5, 2.9262710624),
    ("exponencial", f.exponencial, f.d_exponencial, f.dd_exponencial, f.g_exponencial, 0, 1, 0.5, 0.5671432904),
    ("trigonometrica", f.trigonometrica, f.d_trigonometrica, f.dd_trigonometrica, f.g_trigonometrica, 0, 1, 0.5, 0.7390851332),
    ("mixta", f.mixta, f.d_mixta, f.dd_mixta, f.g_mixta, 0.1, 1, 0.5, 0.6417143709),
]

resumen = open(DATA + "resumen_convergencia.csv", "w")
resumen.write("funcion,metodo,iteraciones,raiz,error,estado\n")
historial = open(DATA + "historial_iteraciones.csv", "w")
historial.write("funcion,metodo,iteracion,x,error\n")

for nombre, fx, dfx, ddfx, gx, a, b, x0, raiz_real in casos:

    x = np.linspace(a, b, 200)
    np.savetxt(DATA + nombre + ".csv", np.column_stack((x, fx(x))),
               delimiter=",", header="x,f(x)", comments="")

    print(nombre, "-> f(a)*f(b) =", fx(a) * fx(b))

    metodos = {
        "biseccion": lambda: biseccion(fx, a, b, TOL, MAX_ITER),
        "falsa_posicion": lambda: falsa_posicion(fx, a, b, TOL, MAX_ITER),
        "punto_fijo": lambda: punto_fijo(fx, gx, x0, TOL, MAX_ITER),
        "secante": lambda: secante(fx, x0, x0 + 0.1, TOL, MAX_ITER),
        "newton": lambda: newton(fx, dfx, x0, TOL, MAX_ITER),
        "newton_mejorado": lambda: newton_mejorado(fx, dfx, ddfx, x0, TOL, MAX_ITER),
    }

    for metodo, correr in metodos.items():
        try:
            raiz, hist = correr()
        except ValueError:
            print("  ", metodo, "no aplica (sin cambio de signo)")
            resumen.write(f"{nombre},{metodo},,,,no aplica\n")
            continue

        error = abs(raiz - raiz_real)
        if len(hist) < MAX_ITER:
            estado = "converge"
        else:
            estado = "no converge"

        print("  ", metodo, len(hist), "iteraciones, raiz =", raiz, estado)
        resumen.write(f"{nombre},{metodo},{len(hist)},{raiz},{error},{estado}\n")

        for i in range(len(hist)):
            historial.write(f"{nombre},{metodo},{i + 1},{hist[i]},{abs(hist[i] - raiz_real)}\n")

resumen.close()
historial.close()