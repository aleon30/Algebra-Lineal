import tkinter as tk
from splinesCubicos import Splines

def accion():
    try:
        texto = str(txt.get('1.0', 'end-1c'))
        lineas = texto.split("\n")
        pares = []
        for linea in lineas:
            valores = linea.split(" ")
            pares.append([float(valores[0]), float(valores[1])])
        pares = sorted(pares)
        splines = Splines(pares)
        splines.graficar()
    except:
        if texto == "":
            print("No se ha ingresado ninguna coordenada.")
        elif len(lineas) == 1:
            print("Error. Debe haber al menos 2 coordenadas.")
        else:
            print("Error. Formato de coordenadas incorrecto.")

ventana = tk.Tk()
ventana.title("Splines Cúbicos")
ventana.geometry('500x350')

txt = tk.Label(ventana, text="Splines Cúbicos vs. Polinomio de Lagrange", font=("Arial", 16, "bold"), bg="lime", relief="raised")
txt.pack(pady=20)

txt = tk.Label(ventana, text="Ingrese las coordenadas X e Y de los puntos a graficar separadas con un espacio.\nCada nueva cordenada debe ir en una línea diferente.")
txt.pack(pady=5)

txt = tk.Text(ventana, height=5, width=40)
txt.pack(pady=10)

btn = tk.Button(ventana, text="Graficar Splines", bg="lightblue", command=accion)
btn.pack(pady=10)

btn = tk.Button(ventana, text="Salir", bg="red", command=ventana.destroy)
btn.pack(pady=10)

ventana.mainloop()