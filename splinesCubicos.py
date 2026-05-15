import matplotlib.pyplot as plt
import numpy as np
from funcionesPolinomios import calcular_splines, interpolacion_lagrange

class Splines:
    def __init__(self, pares):
        self.coordsX = np.array([])
        self.coordsY = np.array([])
        for par in pares:
            self.coordsX = np.append(self.coordsX, par[0])
            self.coordsY = np.append(self.coordsY, par[1])
        self.a, self.b, self.c, self.d = calcular_splines(self.coordsX, self.coordsY)
    
    def imprimirCorrespondencia(self):
        print("--- Ecuaciones de los Splines por Intervalo ---")
        for i in range(len(self.d)):
            print(f"Intervalo [{self.coordsX[i]}, {self.coordsX[i+1]}]:")
            print(f"S_{i}(x) = {self.a[i]:.2f}(x-{self.coordsX[i]})^3 + {self.b[i]:.2f}(x-{self.coordsX[i]})^2 + {self.c[i]:.2f}(x-{self.coordsX[i]}) + {self.d[i]:.2f}\n")
    
    def graficar(self):
        x_grafica = np.linspace(min(self.coordsX), max(self.coordsX), 200)
        y_spline = []
        y_lagrange = [interpolacion_lagrange(self.coordsX, self.coordsY, val) for val in x_grafica]

        for val in x_grafica:
            idx = 0
            for i in range(len(self.coordsX)-1):
                if self.coordsX[i] <= val <= self.coordsX[i+1]:
                    idx = i
                    break
            dx = val - self.coordsX[idx]
            y_spline.append(self.a[idx]*dx**3 + self.b[idx]*dx**2 + self.c[idx]*dx + self.d[idx])

        fig = plt.figure(figsize=(10, 6))
        plt.plot(x_grafica, y_spline, label='Spline Cúbico', color='blue', linewidth=2)
        plt.plot(x_grafica, y_lagrange, '--', label='Lagrange', color='red', alpha=0.7)
        plt.scatter(self.coordsX, self.coordsY, color='black', zorder=5, label='Datos')

        fig.canvas.manager.set_window_title("Spline Cúbico vs. Lagrange")
        plt.title('Comparación: Spline Cúbico vs. Polinomio Interpolador de Lagrange')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid(True)
        plt.show()