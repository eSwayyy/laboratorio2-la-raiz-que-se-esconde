## Entorno (venv)

Requiere Python 3.10 o superior. Desde la raíz del repositorio:

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Dependencias (`requirements.txt`): `numpy` y `matplotlib`.

## Qué hace cada script

Todos los scripts están en `src/scripts/`.

| Script | Qué hace |
| --- | --- |
| `metodos.py` | Implementa con NumPy los seis métodos: `biseccion`, `falsa_posicion`, `punto_fijo`, `secante`, `newton` y `newton_mejorado`. Cada uno recibe la tolerancia y el tope de iteraciones, y devuelve la raíz junto con el historial de aproximaciones. Los métodos cerrados lanzan un error si no hay cambio de signo. No se ejecuta directamente: lo importan los demás scripts. |
| `funciones.py` | Define las seis funciones de prueba (polinómica, raíz doble, logarítmica, exponencial, trigonométrica y mixta), con su primera derivada (Newton), su segunda derivada (Newton mejorado) y el despeje `g(x)` (punto fijo). No se ejecuta directamente: lo importan los demás scripts. |
| `generar_datos.py` | Fija el ambiente controlado (tolerancia `1e-6`, máximo 100 iteraciones, intervalo `[a, b]` y estimación inicial `x₀` de cada función), verifica el cambio de signo `f(a)·f(b)` y ejecuta los seis métodos en cada función. Genera en `src/data/` un CSV por función con columnas `(x, f(x))`, `resumen_convergencia.csv` (iteraciones, raíz, error y estado por método) e `historial_iteraciones.csv` (aproximación y error en cada iteración). |
| `graficar.py` | Lee los CSV de `src/data/` y guarda en `src/assets/` tres tipos de gráficos: cada función con su raíz marcada (`funcion_*.png`), la convergencia `\|error\|` vs iteración en escala logarítmica comparando los métodos (`convergencia_*.png`) y el resumen de iteraciones por método y función (`resumen_iteraciones.png`). |
| `experimentos.py` | Ejecuta pruebas adicionales para el informe y guarda el resultado en `src/data/experimentos.txt`: (A) efecto del intervalo inicial en bisección y falsa posición, (B) efecto de la estimación inicial `x₀` en punto fijo, secante, Newton y Newton mejorado, y (C) estimación numérica del orden de convergencia de cada método. |

## Cómo ejecutar

Con el entorno activado y **desde la raíz del repositorio** (los scripts usan rutas relativas `src/data/` y `src/assets/`), en este orden:

```bash
python src/scripts/generar_datos.py
python src/scripts/graficar.py
python src/scripts/experimentos.py
```

`graficar.py` necesita que `generar_datos.py` se haya ejecutado antes, porque lee los CSV que este genera. `experimentos.py` es independiente.

## Resultados

El análisis de convergencia y la conclusión están en [`informe.md`](informe.md).