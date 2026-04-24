import matplotlib.pyplot as plt
import numpy as np
from funciones.funcCubicos import calcular_splines, interpolacion_lagrange

# Datos de prueba (puedes cambiarlos)
coordsX = np.array([0, 1, 2, 3])
coordsY = np.array([0, -50, 30, 20])

# 1. Calcular Coeficientes del Spline
a, b, c, d = calcular_splines(coordsX, coordsY)

# 2. Mostrar Reglas de Correspondencia
print("--- Ecuaciones de los Splines por Intervalo ---")
for i in range(len(d)):
    print(f"Intervalo [{coordsX[i]}, {coordsX[i+1]}]:")
    print(f"S_{i}(x) = {a[i]:.2f}(x-{coordsX[i]})^3 + {b[i]:.2f}(x-{coordsX[i]})^2 + {c[i]:.2f}(x-{coordsX[i]}) + {d[i]:.2f}\n")

# 3. Preparar datos para graficar
x_grafica = np.linspace(min(coordsX), max(coordsX), 200)
y_spline = []
y_lagrange = [interpolacion_lagrange(coordsX, coordsY, val) for val in x_grafica]

# Evaluación de Splines
for val in x_grafica:
    idx = 0
    for i in range(len(coordsX)-1):
        if coordsX[i] <= val <= coordsX[i+1]:
            idx = i
            break
    dx = val - coordsX[idx]
    y_spline.append(a[idx]*dx**3 + b[idx]*dx**2 + c[idx]*dx + d[idx])

fig = plt.figure(figsize=(10, 6))
plt.plot(x_grafica, y_spline, label='Spline Cúbico', color='blue', linewidth=2)
plt.plot(x_grafica, y_lagrange, '--', label='Lagrange', color='red', alpha=0.7)
plt.scatter(coordsX, coordsY, color='black', zorder=5, label='Datos')

fig.canvas.manager.set_window_title("Spline Cúbico vs. Lagrange")
plt.title('Comparación: Spline Cúbico vs. Polinomio Interpolador de Lagrange')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()