import numpy as np
import matplotlib.pyplot as plt

DATA = "src/data/"
ASSETS = "src/assets/"

# nombre -> (título, raíz real)
funciones = {
    "polinomica": ("f(x) = x³ − x − 2", 1.5213797068),
    "raiz_doble": ("f(x) = (x − 2)²  (raíz doble)", 2.0),
    "logaritmica": ("f(x) = ln(x) + x − 4", 2.9262710624),
    "exponencial": ("f(x) = e^(−x) − x", 0.5671432904),
    "trigonometrica": ("f(x) = cos(x) − x", 0.7390851332),
    "mixta": ("f(x) = √x − cos(x)", 0.6417143709),
}

metodos = ["biseccion", "falsa_posicion", "punto_fijo",
           "secante", "newton", "newton_mejorado"]

# ------------------------------------------------------------
# 1. Cada función con su raíz marcada
# ------------------------------------------------------------
for nombre, (titulo, raiz) in funciones.items():
    datos = np.loadtxt(DATA + nombre + ".csv", delimiter=",", skiprows=1)
    x = datos[:, 0]
    y = datos[:, 1]

    plt.figure(figsize=(7, 4))
    plt.plot(x, y, label="f(x)")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.plot(raiz, 0, "ro", label=f"raíz ≈ {raiz:.6f}")
    if nombre == "raiz_doble":
        plt.title(titulo + " — toca el eje x sin cruzarlo")
    else:
        plt.title(titulo)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.savefig(ASSETS + "funcion_" + nombre + ".png", dpi=150, bbox_inches="tight")
    plt.close()

# ------------------------------------------------------------
# 2. Convergencia: |error| vs iteración (escala log)
# ------------------------------------------------------------
# leer el historial: lista de (funcion, metodo, iteracion, error)
filas = []
archivo = open(DATA + "historial_iteraciones.csv")
archivo.readline()   # saltar encabezado
for linea in archivo:
    partes = linea.strip().split(",")
    filas.append((partes[0], partes[1], int(partes[2]), float(partes[4])))
archivo.close()

for nombre, (titulo, raiz) in funciones.items():
    plt.figure(figsize=(7, 4))
    for metodo in metodos:
        iteraciones = [fila[2] for fila in filas if fila[0] == nombre and fila[1] == metodo]
        errores = [fila[3] for fila in filas if fila[0] == nombre and fila[1] == metodo]
        if len(errores) == 0:
            continue   # el método no aplica en esta función
        errores = np.maximum(errores, 1e-17)   # el log no acepta 0
        plt.semilogy(iteraciones, errores, marker="o", markersize=3, label=metodo)
    plt.title("Convergencia — " + titulo)
    plt.xlabel("Iteración")
    plt.ylabel("|error| (escala log)")
    plt.legend()
    plt.grid(True)
    plt.savefig(ASSETS + "convergencia_" + nombre + ".png", dpi=150, bbox_inches="tight")
    plt.close()

# ------------------------------------------------------------
# 3. Resumen de iteraciones por método y función
# ------------------------------------------------------------
iters = {}   # (funcion, metodo) -> iteraciones (0 si no aplica)
archivo = open(DATA + "resumen_convergencia.csv")
archivo.readline()
for linea in archivo:
    partes = linea.strip().split(",")
    if partes[2] == "":
        iters[(partes[0], partes[1])] = 0
    else:
        iters[(partes[0], partes[1])] = int(partes[2])
archivo.close()

nombres = list(funciones.keys())
ancho = 0.13
posiciones = np.arange(len(nombres))

plt.figure(figsize=(11, 5))
for i, metodo in enumerate(metodos):
    valores = [iters[(nombre, metodo)] for nombre in nombres]
    plt.bar(posiciones + i * ancho, valores, ancho, label=metodo)
    for j in range(len(valores)):
        if valores[j] == 0:
            plt.text(posiciones[j] + i * ancho, 1, "n/a", ha="center", fontsize=7, rotation=90)

plt.xticks(posiciones + ancho * 2.5, nombres)
plt.title("Iteraciones por método y función (n/a = no aplica)")
plt.xlabel("Función")
plt.ylabel("Iteraciones")
plt.legend()
plt.grid(True, axis="y")
plt.savefig(ASSETS + "resumen_iteraciones.png", dpi=150, bbox_inches="tight")
plt.close()

print("Gráficos guardados en", ASSETS)