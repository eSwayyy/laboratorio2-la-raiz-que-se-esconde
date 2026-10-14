# Evaluación 2 — La raíz que se esconde

**Universidad Católica del Maule — Computación Numérica (INF323)**

**Integrante:** Alonso Javier Vergara Quiroz - 21.825.897-2

### ¿Qué método convergió en menos iteraciones en cada función? ¿Por qué?

- **Polinómica, exponencial y mixta:** Newton y Newton mejorado (2 iteraciones).
- **Logarítmica y trigonométrica:** empate entre secante, Newton y Newton mejorado (3 iteraciones).
- **Raíz doble:** Newton mejorado (1 iteración).

Los métodos con convergencia superlineal o cuadrática (secante, Newton) necesitan entre 2 y 3 iteraciones, mientras que los lineales necesitan más: bisección 19–20, falsa posición 4–12 y punto fijo 4–33. La razón es que en un método cuadrático el error se eleva al cuadrado en cada paso, mientras que en uno lineal el error solo se multiplica por una constante.

### ¿Qué orden de convergencia tiene cada método y cómo se refleja en el gráfico |error| vs iteración?

| Método | Orden | Cómo se ve en el gráfico (escala log) |
|---|---|---|
| Bisección | Lineal (la cota del error se reduce a la mitad en cada paso) | Recta descendente con dientes de sierra, porque el error real no baja de forma monótona |
| Falsa posición | Lineal | Recta descendente |
| Punto fijo | Lineal, con razón \|g′(raíz)\| | Recta cuya pendiente depende de \|g′(raíz)\| |
| Secante | Superlineal (≈ 1,618) | Curva que cae más rápido que una recta, pero menos que Newton |
| Newton | Cuadrático (en raíz simple) | Cae casi en vertical en 2–3 iteraciones |
| Newton mejorado | Cuadrático (también en raíz múltiple) | Igual que Newton en raíz simple; en la raíz doble llega a la raíz en 1 iteración |

Los gráficos están en `src/assets/convergencia_*.png`.

### ¿Qué métodos requieren un intervalo con cambio de signo y cuáles no?

- **Requieren cambio de signo f(a)·f(b) < 0:** bisección y falsa posición (métodos cerrados). En el código lanzan un error si no se cumple, lo que ocurrió con (x − 2)² en [1, 3].
- **No lo requieren:** punto fijo, secante, Newton y Newton mejorado (métodos abiertos). Solo necesitan una estimación inicial, pero no garantizan convergencia: el punto fijo necesita |g′| < 1, Newton necesita f′ ≠ 0 cerca de la raíz y la secante necesita f(x₁) ≠ f(x₀).

### En la raíz doble: ¿qué métodos fallan o no aplican y cuál se comporta mejor?

Función (x − 2)², raíz doble en x = 2, con f(2) = f′(2) = 0.

| Método | Resultado |
|---|---|
| Bisección | **No aplica**: en [1, 3], f(1)·f(3) = +1, sin cambio de signo |
| Falsa posición | **No aplica**, por la misma razón |
| Punto fijo (g = x + (x−2)²) | **Falla**: con x₀ = 1.2 llegó al tope de 100 iteraciones con error 9.2e-3 (convergencia muy lenta, porque g′(2) = 1); con x₀ = 0, 3 y 10 **diverge** |
| Secante | Converge en 14 iteraciones (error 7.4e-4), pero de forma lineal |
| Newton | Converge en 10 iteraciones (error 7.8e-4), pero de forma lineal |
| **Newton mejorado** | **Converge en 1 iteración** (raíz exacta) |

Evidencia visual en: `convergencia_raiz_doble.png`

### ¿Cómo influyen el intervalo inicial y la estimación inicial?

Para responder, se repitieron las pruebas con los mismos métodos cambiando el intervalo o x₀.

**Intervalo inicial (métodos cerrados):**

| Función | Intervalo | Bisección | Falsa posición |
|---|---|---|---|
| polinómica | [1, 2] | 20 | 12 |
| polinómica | [1.4, 1.6] | 18 | 5 |
| polinómica | [0, 5] | 23 | 75 |
| polinómica | [−10, 10] | 25 | no converge (tope) |
| polinómica | [1, 100] | 27 | no converge (tope) |
| exponencial | [0, 1] | 20 | 7 |
| exponencial | [0.5, 0.6] | 16 | 3 |
| exponencial | [−5, 5] | 22 | no converge (tope) |
| exponencial | [0, 100] | 26 | 8 |

- La **bisección** siempre converge, y sus iteraciones crecen despacio con el ancho del intervalo: el número de pasos es aproximadamente log₂((b − a)/tol), de modo que pasar de ancho 0.2 a 99 solo suma 9 iteraciones (18 a 27).
- La **falsa posición** es mucho más sensible: con un intervalo angosto necesita 3–5 iteraciones (más rápida que la bisección), pero con intervalos anchos puede volverse lenta (75 iteraciones en [0, 5]) o no converger en 100 (en [−10, 10] y [1, 100] para la polinómica, y [−5, 5] para la exponencial). No depende solo del ancho: en la exponencial, [0, 100] converge en 8 y [−5, 5] no converge. Esto es coherente con que, en funciones convexas, uno de los extremos queda casi fijo y el intervalo no se achica.

**Estimación inicial x₀ (métodos abiertos):**

| Función | x₀ | Punto fijo | Secante | Newton | Newton mejorado |
|---|---|---|---|---|---|
| polinómica | 1.5 | 7 | 3 | 2 | 2 |
| polinómica | 1 | 8 | 6 | 5 | 5 |
| polinómica | 3 | 9 | 7 | 5 | 6 |
| polinómica | 10 | 9 | 12 | 9 | 8 |
| polinómica | 0.5 | 9 | 28 | 37 | 28 |
| polinómica | 0 | 9 | 9 | 30 | 4 |
| trigonométrica | 0.5 | 33 | 3 | 3 | 3 |
| trigonométrica | 3 | 34 | 7 | 5 | 5 |
| trigonométrica | 4 | 31 | 7 | 38 | 7 |
| trigonométrica | 10 | 32 | 7 | no converge | 21 |
| trigonométrica | −3 | 34 | 7 | no converge | 9 |
| mixta | 0.5 | 4 | 3 | 2 | 2 |
| mixta | 0.1 | 3 | 4 | 3 | no converge |
| mixta | 0.01 | 4 | 5 | 4 | no converge |
| mixta | 5 | 6 | no converge | no converge | no converge |

- **Newton** es el más sensible: pasa de 2 iteraciones (x₀ = 1.5 en la polinómica) a 37 (x₀ = 0.5) o a no converger en 100 iteraciones (trigonométrica con x₀ = 10 y −3; mixta con x₀ = 5). En la polinómica, x₀ = 0.5 queda cerca de un punto donde f′ ≈ 0 (f′(x) = 3x² − 1 se anula en x ≈ 0.577), y la tangente casi horizontal lanza la iteración lejos de la raíz. En la trigonométrica f′ = −sin(x) − 1 se acerca a 0 periódicamente, con el mismo efecto.
- **Newton mejorado** no corrige esto: en la mixta con x₀ = 0.1 y 0.01 no converge, porque la iteración salió del dominio (x ≤ 0, donde √x no existe). En la polinómica con x₀ = 0, en cambio, necesitó 4 iteraciones frente a 30 de Newton.
- **Secante** fue en general más robusta que Newton en la trigonométrica (7 iteraciones incluso con x₀ = 10 y −3, donde Newton no converge), pero falló en la mixta con x₀ = 5.
- **Punto fijo** casi no depende de x₀ en las funciones de raíz simple (polinómica: 7–9; trigonométrica: 31–34), porque el despeje g elegido es una contracción en esa zona. En cambio, en la raíz doble depende por completo de x₀ (ver 3.4).

### ¿Qué método se recomienda según el tipo de función (velocidad vs robustez)?

| Situación | Método recomendado | Fundamento |
|---|---|---|
| Se conoce un intervalo con cambio de signo y se prioriza que no falle | **Bisección** | Converge siempre (18–27 iteraciones en todos los intervalos probados) |
| Función derivable de raíz simple, con buena estimación inicial | **Newton** | 2–3 iteraciones, convergencia cuadrática |
| No se dispone de la derivada | **Secante** | 3–7 iteraciones, solo una f nueva por iteración, y más robusta que Newton en la trigonométrica |
| Raíz múltiple o sospecha de f′(raíz) = 0 | **Newton mejorado** | 1 iteración en la raíz doble, frente a 10 de Newton |
| Intervalo muy angosto y cambio de signo | **Falsa posición** | 3–5 iteraciones; pero con intervalos anchos puede no converger |
| Solo si existe un despeje x = g(x) con \|g′\| < 1 | **Punto fijo** | Lineal y más lento (21–33 iteraciones en la exponencial y trigonométrica); inutilizable en la raíz doble |

---

## Conclusión

**¿Qué método elegirían para cada tipo de función y por qué (velocidad vs robustez)?** \
Para las funciones de raíz simple (polinómica, logarítmica, exponencial, trigonométrica y mixta), los métodos más eficientes fueron Newton y la secante, con 2–3 iteraciones frente a las 19–20 de la bisección. Pero esa velocidad tiene un precio en robustez: Newton falló con ciertas estimaciones iniciales (no convergió en 100 iteraciones en la trigonométrica con x₀ = 10 y −3, ni en la mixta con x₀ = 5), mientras que la bisección convergió en todos los intervalos probados. La elección depende entonces que se busca, si se busca seguridad, bisección; si se prefiere rapidez en convergencia, Newton; si no se tiene la derivada, secante. Para raíces múltiples, Newton mejorado.

**¿Qué ocurrió en la raíz doble y qué dice eso sobre «tener raíz» frente a «cambiar de signo»?** \
En (x − 2)² la función vale 0 en x = 2, es decir, tiene raíz, pero nunca cambia de signo, de modo que bisección y falsa posición no pudieron aplicarse en ningún intervalo. Además, como f′(2) = 0, los métodos abiertos se ven afectados: Newton y la secante pasaron de convergencia cuadrática/superlineal a lineal (10 y 14 iteraciones), el punto fijo llegó al tope o divergió, y solo Newton mejorado, que incorpora f″, recuperó la convergencia rápida (1 iteración).

**¿Cómo cambió el número de iteraciones al mover el intervalo o la estimación inicial?** \
En los métodos cerrados, ensanchar el intervalo de ancho 0.2 a 99 aumentó la bisección de 18 a 27 iteraciones (efecto logarítmico), pero hizo que la falsa posición pasara de 5 iteraciones a 75 o a no converger. En los abiertos, mover x₀ cambió Newton de 2 a 37 iteraciones o a no converger, mientras que el punto fijo, con un despeje contractivo, casi no se vio afectado (7–9 iteraciones en la polinómica). La estimación inicial importa más cuanto más rápido es el método: los más veloces son también los más sensibles.

Estas conclusiones se apoyan en los datos de `src/data/resumen_convergencia.csv` y en los gráficos de `src/assets/`.