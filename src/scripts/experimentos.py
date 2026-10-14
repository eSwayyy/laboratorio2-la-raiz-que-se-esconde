import numpy as np

import funciones as f
from metodos import (biseccion, falsa_posicion, punto_fijo,
                     secante, newton, newton_mejorado)

TOL = 1e-6
MAX_ITER = 100

lineas = []


def mostrar(texto=""):
    print(texto)
    lineas.append(texto)


def contar(fx, correr):
    """Devuelve las iteraciones como texto, o por qué falló."""
    try:
        raiz, hist = correr()
    except ValueError:
        return "no aplica"
    if len(hist) >= MAX_ITER or not np.isfinite(raiz) or abs(fx(raiz)) > 1e-3:
        return "no converge"
    return str(len(hist))


mostrar("A. INTERVALO INICIAL (iteraciones)")
mostrar("funcion, intervalo, biseccion, falsa_posicion")
pruebas = [
    ("polinomica", f.polinomica, [(1, 2), (1.4, 1.6), (0, 5), (-10, 10), (1, 100)]),
    ("exponencial", f.exponencial, [(0, 1), (0.5, 0.6), (-5, 5), (0, 100)]),
]
for nombre, fx, intervalos in pruebas:
    for a, b in intervalos:
        bis = contar(fx, lambda: biseccion(fx, a, b, TOL, MAX_ITER))
        fal = contar(fx, lambda: falsa_posicion(fx, a, b, TOL, MAX_ITER))
        mostrar(f"{nombre}, [{a}; {b}], {bis}, {fal}")


mostrar("")
mostrar("B. ESTIMACION INICIAL x0 (iteraciones)")
mostrar("funcion, x0, punto_fijo, secante, newton, newton_mejorado")
pruebas = [
    ("polinomica", f.polinomica, f.d_polinomica, f.dd_polinomica, f.g_polinomica, [1.5, 1, 3, 10, 0.5, 0]),
    ("trigonometrica", f.trigonometrica, f.d_trigonometrica, f.dd_trigonometrica, f.g_trigonometrica, [0.5, 2, 3, 4, 10, -3]),
    ("mixta", f.mixta, f.d_mixta, f.dd_mixta, f.g_mixta, [0.5, 0.1, 0.01, 2, 5]),
    ("raiz_doble", f.raiz_doble, f.d_raiz_doble, f.dd_raiz_doble, f.g_raiz_doble, [1.2, 0, 3, 10]),
]
for nombre, fx, dfx, ddfx, gx, valores in pruebas:
    for x0 in valores:
        pf = contar(fx, lambda: punto_fijo(fx, gx, x0, TOL, MAX_ITER))
        sec = contar(fx, lambda: secante(fx, x0, x0 + 0.1, TOL, MAX_ITER))
        new = contar(fx, lambda: newton(fx, dfx, x0, TOL, MAX_ITER))
        mej = contar(fx, lambda: newton_mejorado(fx, dfx, ddfx, x0, TOL, MAX_ITER))
        mostrar(f"{nombre}, {x0}, {pf}, {sec}, {new}, {mej}")


mostrar("")
mostrar("C. ORDEN DE CONVERGENCIA ESTIMADO (tol = 1e-13)")
mostrar("funcion, metodo, iteraciones, orden_estimado, razon_final")
pruebas = [
    ("polinomica", f.polinomica, f.d_polinomica, f.dd_polinomica, f.g_polinomica, 1, 2, 1.5),
    ("exponencial", f.exponencial, f.d_exponencial, f.dd_exponencial, f.g_exponencial, 0, 1, 0.5),
    ("trigonometrica", f.trigonometrica, f.d_trigonometrica, f.dd_trigonometrica, f.g_trigonometrica, 0, 1, 0.5),
    ("logaritmica", f.logaritmica, f.d_logaritmica, f.dd_logaritmica, f.g_logaritmica, 2, 3, 2.5),
]
T = 1e-13
for nombre, fx, dfx, ddfx, gx, a, b, x0 in pruebas:
    raiz_real, _ = newton(fx, dfx, x0, 1e-15, 200)
    metodos = {
        "biseccion": lambda: biseccion(fx, a, b, T, 200),
        "falsa_posicion": lambda: falsa_posicion(fx, a, b, T, 200),
        "punto_fijo": lambda: punto_fijo(fx, gx, x0, T, 200),
        "secante": lambda: secante(fx, x0, x0 + 0.1, T, 200),
        "newton": lambda: newton(fx, dfx, x0, T, 200),
        "newton_mejorado": lambda: newton_mejorado(fx, dfx, ddfx, x0, T, 200),
    }
    for metodo, correr in metodos.items():
        raiz, hist = correr()
        e = np.abs(hist - raiz_real)
        e = e[e > 1e-15]                  # quitar errores que llegaron al límite de la máquina
        if len(e) < 3:
            mostrar(f"{nombre}, {metodo}, {len(hist)}, -, -")
            continue
        p = [np.log(e[k + 1] / e[k]) / np.log(e[k] / e[k - 1]) for k in range(1, len(e) - 1)]
        razon = e[-1] / e[-2]
        mostrar(f"{nombre}, {metodo}, {len(hist)}, {np.median(p):.2f}, {razon:.3f}")

archivo = open("src/data/experimentos.txt", "w", encoding="utf-8")
archivo.write("\n".join(lineas))
archivo.close()