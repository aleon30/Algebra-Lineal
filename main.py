import tkinter as tk
from tkinter import ttk, messagebox
from splinesCubicos import Splines

# Funciones para los botones

def accion():
    try:
        texto = str(entrada.get('1.0', 'end-1c'))
        if not texto.strip():
            messagebox.showwarning("Aviso", "No se ha ingresado ninguna coordenada.")
            return
        lineas = texto.split("\n")
        pares = []
        for linea in lineas:
            valores = linea.split(" ")
            if len(valores) != 2:
                messagebox.showerror("Error", "Formato de coordenadas incorrecto.")
                return
            pares.append([float(valores[0]), float(valores[1])])
        pares = sorted(pares)
        splines = Splines(pares)
        splines.graficar()
    except:
        if len(lineas) == 1:
            messagebox.showerror("Error", "Debe haber al menos 2 coordenadas.")
        else:
            messagebox.showerror("Error", "Formato de coordenadas incorrecto.")

def limpiar():
    entrada.delete("1.0", tk.END)

# Configuración de la ventana principal

ventana = tk.Tk()
ventana.title("Splines Cúbicos vs. Polinomio de Lagrange")
ventana.configure(bg="white")
ventana.geometry("600x500")

ANCHO = 600

# Elementos de la interfaz

titulo = tk.Label(
    ventana,
    text="Splines Cúbicos vs. Polinomio de Lagrange",
    font=("Helvetica", 16, "bold"),
    fg="white",
    bg="darkblue",
    anchor="center",
    wraplength=ANCHO - 20,
    padx=10,
    pady=10,
)
titulo.pack(fill="x", padx=0, pady=0)

desc_frame = tk.Frame(ventana, bg="skyblue")
desc_frame.pack(fill="x", padx=0, pady=10)

linea1 = tk.Frame(desc_frame, bg="skyblue")
linea1.pack(pady=(4, 0))

tk.Label(linea1, text="Ingrese las coordenadas X e Y de los puntos a graficar separadas con un ",
         font=("Helvetica", 10, "italic"), fg="black", bg="skyblue").pack(side="left")
tk.Label(linea1, text="espacio",
         font=("Helvetica", 10, "bold"), fg="red", bg="white",
         relief="flat", padx=3).pack(side="left")
tk.Label(linea1, text=".",
         font=("Helvetica", 10, "italic"), fg="black", bg="skyblue").pack(side="left")

linea2 = tk.Frame(desc_frame, bg="skyblue")
linea2.pack(pady=(2, 4))

tk.Label(linea2, text="Cada nueva coordenada debe ir en una ",
         font=("Helvetica", 10, "italic"), fg="black", bg="skyblue").pack(side="left")
tk.Label(linea2, text="línea diferente",
         font=("Helvetica", 10, "bold"), fg="red", bg="white",
         relief="flat", padx=3).pack(side="left")
tk.Label(linea2, text=".",
         font=("Helvetica", 10, "italic"), fg="black", bg="skyblue").pack(side="left")

input_frame = tk.Frame(ventana, bg="white")
input_frame.pack(pady=6)

entrada = tk.Text(
    input_frame,
    width=50,
    height=10,
    font=("Helvetica", 11),
    relief="solid",
    bd=1,
)
entrada.pack()

estilo = ttk.Style()
estilo.theme_use("clam")
 
estilo.configure("Graficar.TButton",
                 font=("Helvetica", 12),
                 foreground="black",
                 background="#32CD32",       
                 bordercolor="#228B22",
                 padding=(20, 8))
estilo.map("Graficar.TButton",
           background=[("active", "skyblue"), ("pressed", "#0099cc")],
           foreground=[("active", "white"),   ("pressed", "white")])
 
estilo.configure("Limpiar.TButton",
                 font=("Helvetica", 12),
                 foreground="black",
                 background="#808080",       
                 bordercolor="#555555",
                 padding=(20, 8))
estilo.map("Limpiar.TButton",
           background=[("active", "skyblue"), ("pressed", "#0099cc")],
           foreground=[("active", "white"),   ("pressed", "white")])
 
estilo.configure("Salir.TButton",
                 font=("Helvetica", 12),
                 foreground="black",
                 background="#CC0000",       
                 bordercolor="#880000",
                 padding=(20, 8))
estilo.map("Salir.TButton",
           background=[("active", "skyblue"), ("pressed", "#0099cc")],
           foreground=[("active", "white"),   ("pressed", "white")])

botones_frame = tk.Frame(ventana, bg="white")
botones_frame.pack(pady=12)
 
ttk.Button(botones_frame, text="Graficar Splines",
           style="Graficar.TButton", command=accion).pack(pady=5)
 
ttk.Button(botones_frame, text="Limpiar",
           style="Limpiar.TButton", command=limpiar).pack(pady=5)
 
ttk.Button(botones_frame, text="Salir",
           style="Salir.TButton", command=ventana.destroy).pack(pady=5)

ventana.mainloop()