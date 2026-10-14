import numpy as np

def biseccion(f, a, b, tol=1e-6, max_iter=100):
    if f(a) * f(b) > 0:
        raise ValueError("No hay cambio de signo, no existe raíz")
    hist = []
    m = a
    for i in range(max_iter):
        m_ant = m
        m = (a + b)/2
        hist.append(m)
        if abs(f(m)) < tol or abs(m - m_ant) < tol:
            break
        if f(a) * f(m) < 0:
            b = m
        else:
            a = m
    return m, np.array(hist)


def falsa_posicion(f, a, b, tol=1e-6, max_iter=100):
    if f(a) * f(b) > 0:
        raise ValueError("No hay cambio de signo, no existe raíz")
    hist = []
    p = a
    for i in range(max_iter):
        c_ant = p
        p = (a * f(b) - b * f(a)) / (f(b) - f(a))
        hist.append(p)
        if abs(f(p)) < tol or abs(p - c_ant) < tol:
            break
        if f(a) * f(p) < 0:
            b = p
        else:
            a = p
    return p, np.array(hist)


def punto_fijo(f, g, x0, tol=1e-6, max_iter=100):
    hist = []
    x = x0
    for i in range(max_iter):
        x_ant = x
        x = g(x)
        hist.append(x)
        if not np.isfinite(x):
            break  # divergió
        if abs(f(x)) < tol or abs(x - x_ant) < tol:
            break
    return x, np.array(hist)


def secante(f, x0, x1, tol=1e-6, max_iter=100):
    hist = []
    for m in range(max_iter):
        denom = f(x1) - f(x0)
        if abs(denom) < 1e-14:
            break  # división por ~0
        x2 = x1 - f(x1) * (x1 - x0) / denom
        hist.append(x2)
        x0, x1 = x1, x2
        if abs(f(x1)) < tol or abs(x1 - x0) < tol:
            break
    x = hist[-1] if hist else x1
    return x, np.array(hist)


def newton(f, df, x0, tol=1e-6, max_iter=100):
    hist = []
    x = x0
    for _ in range(max_iter):
        d = df(x)
        if abs(d) < 1e-14:
            break  # derivada ~0
        x_ant = x
        x = x - f(x) / d
        hist.append(x)
        if abs(f(x)) < tol or abs(x - x_ant) < tol:
            break
    return x, np.array(hist)


def newton_mejorado(f, df, ddf, x0, tol=1e-6, max_iter=100):
    hist = []
    x = x0
    for _ in range(max_iter):
        denom = df(x) ** 2 - f(x) * ddf(x)
        if abs(denom) < 1e-14:
            break
        x_ant = x
        x = x - f(x) * df(x) / denom
        hist.append(x)
        if abs(f(x)) < tol or abs(x - x_ant) < tol:
            break
    return x, np.array(hist)