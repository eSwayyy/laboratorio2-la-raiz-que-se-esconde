import numpy as np

# ------------------------------------------------------------
#   f(x)    -> la función
#   d_f(x)  -> primera derivada  (Newton, Newton mejorado)
#   dd_f(x) -> segunda derivada  (Newton mejorado)
#   g_f(x)  -> despeje x = g(x)  (punto fijo)
# ------------------------------------------------------------

# intervalo [1, 2]
def polinomica(x):
    return np.power(x, 3) - x - 2

def d_polinomica(x):
    return 3 * np.power(x, 2) - 1

def dd_polinomica(x):
    return 6 * x

def g_polinomica(x):
    return np.cbrt(x + 2)


# x0 = 1.2
def raiz_doble(x):
    return np.power(x - 2, 2)

def d_raiz_doble(x):
    return 2 * (x - 2)

def dd_raiz_doble(x):
    return 2 * np.ones_like(x, dtype=float)

def g_raiz_doble(x):
    return x + np.power(x - 2, 2)


# intervalo [2, 3]
def logaritmica(x):
    return np.log(x) + x - 4

def d_logaritmica(x):
    return 1 / x + 1

def dd_logaritmica(x):
    return -1 / np.power(x, 2)

def g_logaritmica(x):
    return 4 - np.log(x)


# intervalo [0, 1]
def exponencial(x):
    return np.exp(-x) - x

def d_exponencial(x):
    return -np.exp(-x) - 1

def dd_exponencial(x):
    return np.exp(-x)

def g_exponencial(x):
    return np.exp(-x)


# intervalo [0, 1]
def trigonometrica(x):
    return np.cos(x) - x

def d_trigonometrica(x):
    return -np.sin(x) - 1

def dd_trigonometrica(x):
    return -np.cos(x)

def g_trigonometrica(x):
    return np.cos(x)


# intervalo [0.1, 1]
def mixta(x):
    return np.sqrt(x) - np.cos(x)

def d_mixta(x):
    return 1 / (2 * np.sqrt(x)) + np.sin(x)

def dd_mixta(x):
    return -1 / (4 * np.power(x, 1.5)) + np.cos(x)

def g_mixta(x):
    return x - 0.8 * (np.sqrt(x) - np.cos(x))