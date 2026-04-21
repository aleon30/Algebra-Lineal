import matplotlib.pyplot as plt
import numpy as np
from Funciones import calcular_splines, interpolacion_lagrange

# Datos de prueba (puedes cambiarlos)
coordsX = np.array([0, 1, 4, 9])
coordsY = np.array([0, 1, 16, 81])

# 1. Calcular Coeficientes del Spline
a, b, c, d = calcular_splines(coordsX, coordsY)

# 2. Mostrar Reglas de Correspondencia
print("--- Ecuaciones de los Splines por Intervalo ---")
for i in range(len(a)):
    print(f"Intervalo [{coordsX[i]}, {coordsX[i+1]}]:")
    print(f"S_{i}(x) = {a[i]:.2f} + {b[i]:.2f}(x-{coordsX[i]}) + {c[i]:.2f}(x-{coordsX[i]})^2 + {d[i]:.2f}(x-{coordsX[i]})^3\n")

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
    y_spline.append(a[idx] + b[idx]*dx + c[idx]*dx**2 + d[idx]*dx**3)

plt.figure(figsize=(10, 6))
plt.plot(x_grafica, y_spline, label='Spline Cúbico', color='blue', linewidth=2)
plt.plot(x_grafica, y_lagrange, '--', label='Lagrange', color='red', alpha=0.7)
plt.scatter(coordsX, coordsY, color='black', zorder=5, label='Datos Originales')

plt.title('Comparación: Spline Cúbico vs Lagrange')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()