import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import AnchoredText
from funcionesPolinomios import calcular_splines, interpolacion_lagrange

class Splines:
    def __init__(self, pares):
        self.coordsX = np.array([])
        self.coordsY = np.array([])
        for par in pares:
            self.coordsX = np.append(self.coordsX, par[0])
            self.coordsY = np.append(self.coordsY, par[1])
        self.a, self.b, self.c, self.d = calcular_splines(self.coordsX, self.coordsY)

    def texto_correspondencia(self):
        lineas = ["Reglas de correspondencia por intervalo:"]
        for i in range(len(self.d)):
            x0 = self.coordsX[i]
            x1 = self.coordsX[i+1]

            terminos = []
            
            terminos.append(f"{self.a[i]:+.2f}(x{-x0:+.2f})³")
            terminos.append(f"{self.b[i]:+.2f}(x{-x0:+.2f})²")
            terminos.append(f"{self.c[i]:+.2f}(x{-x0:+.2f})")
            terminos.append(f"{self.d[i]:+.2f}")

            ecuacion = " ".join(terminos).lstrip("+").strip()

            if i != len(self.d) - 1:
                lineas.append(f"S_{i} = {ecuacion}, x ∈ [{x0:.1f}, {x1:.1f})")
            else:  
                lineas.append(f"S_{i} = {ecuacion}, x ∈ [{x0:.1f}, {x1:.1f}]")

        return "\n".join(lineas)

    def evaluar_spline(self, x_eval):
        y = np.zeros_like(x_eval)
        n = len(self.coordsX) - 1
        for j, val in enumerate(x_eval):
            i = int(np.clip(np.searchsorted(self.coordsX, val, side='right') - 1, 0, n - 1))
            dx = val - self.coordsX[i]
            y[j] = self.a[i]*dx**3 + self.b[i]*dx**2 + self.c[i]*dx + self.d[i]
        return y

    def graficar(self):
        x_grafica = np.linspace(self.coordsX[0], self.coordsX[-1], 500)
        y_spline  = self.evaluar_spline(x_grafica)
        y_lagrange = np.array([interpolacion_lagrange(self.coordsX, self.coordsY, v) for v in x_grafica])

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(x_grafica, y_spline, label='Spline Cúbico', color='blue', linewidth=2)
        ax.plot(x_grafica, y_lagrange, label='Lagrange', color='red', linewidth=1.5, linestyle='--', alpha=0.7)
        ax.scatter(self.coordsX, self.coordsY, color='black', zorder=5, label='Datos')

        texto = self.texto_correspondencia()
        cuadro = AnchoredText(texto, loc='upper left', prop=dict(size=8, family='monospace'),
            frameon=True, bbox_to_anchor=(1.01, 1), bbox_transform=ax.transAxes)
        cuadro.patch.set_boxstyle("round,pad=0.4")
        cuadro.patch.set_alpha(0.9)
        cuadro.patch.set_edgecolor("gray")
        ax.add_artist(cuadro)

        fig.canvas.manager.set_window_title("Spline Cúbico vs. Lagrange")
        ax.set_title('Comparación: Spline Cúbico vs. Polinomio Interpolador de Lagrange')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend(loc='upper right')
        ax.grid(True)

        plt.tight_layout()
        plt.show()