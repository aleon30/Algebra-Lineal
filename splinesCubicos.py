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
    
    def analisis_cuantitativo(self):
        print("\n--- Análisis Cuantitativo: Diferencia Absoluta (Spline vs Lagrange) ---")
        puntos_medios = self.coordsX[:-1] + np.diff(self.coordsX) / 2

        diferencias = []
        vals_spline = []
        vals_lagrange = []

        for pm in puntos_medios:
            val_lagrange = interpolacion_lagrange(self.coordsX, self.coordsY, pm)
            val_spline = self.evaluar_spline(np.array([pm]))[0]
            diferencia = abs(val_lagrange - val_spline)
            diferencias.append(diferencia)
            vals_spline.append(val_spline)
            vals_lagrange.append(val_lagrange)
            print(f"Punto medio x={pm:.2f} | Spline: {val_spline:.4f} | Lagrange: {val_lagrange:.4f} | Dif. Absoluta: {diferencia:.4f}")

        # --- Gráfica de diferencias ---
        x_grafica = np.linspace(self.coordsX[0], self.coordsX[-1], 500)
        dif_continua = np.abs(
            self.evaluar_spline(x_grafica) -
            np.array([interpolacion_lagrange(self.coordsX, self.coordsY, v) for v in x_grafica])
        )

        fig, ax = plt.subplots(figsize=(11, 5))

        # Área bajo la curva de diferencia
        ax.fill_between(x_grafica, dif_continua, alpha=0.15, color='steelblue')
        ax.plot(x_grafica, dif_continua, color='steelblue', linewidth=2, label='|Spline − Lagrange|')

        # Puntos medios destacados
        ax.scatter(puntos_medios, diferencias, color='crimson', zorder=5,
            s=70, label='Diferencia en puntos medios')

        # Anotaciones en cada punto medio
        for pm, dif in zip(puntos_medios, diferencias):
            ax.annotate(f'{dif:.4f}', xy=(pm, dif),
                        xytext=(0, 10), textcoords='offset points',
                        ha='center', fontsize=8, color='crimson')

        # Líneas verticales en los nodos originales
        for x in self.coordsX:
            ax.axvline(x, color='gray', linewidth=0.7, linestyle=':', alpha=0.6)

        # Máxima diferencia
        idx_max = np.argmax(dif_continua)
        ax.annotate(f'Máx: {dif_continua[idx_max]:.4f}',
                    xy=(x_grafica[idx_max], dif_continua[idx_max]),
                    xytext=(15, -15), textcoords='offset points',
                    arrowprops=dict(arrowstyle='->', color='navy'),
                    fontsize=9, color='navy')

        fig.canvas.manager.set_window_title("Análisis Cuantitativo")
        ax.set_title('Diferencia Absoluta: Spline Cúbico vs. Polinomio de Lagrange', fontsize=13)
        ax.set_xlabel('X')
        ax.set_ylabel('|Diferencia|')
        ax.legend()
        ax.grid(True, alpha=0.4)
        plt.tight_layout()
        plt.show()