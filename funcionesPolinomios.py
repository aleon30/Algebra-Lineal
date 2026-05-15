import numpy as np

def interpolacion_lagrange(x_puntos, y_puntos, x_val):
    # Calcula el valor de Lagrange en un punto x_val.
    n = len(x_puntos)
    resultado = 0
    for i in range(n):
        termino = y_puntos[i]
        for j in range(n):
            if i != j:
                termino *= (x_val - x_puntos[j]) / (x_puntos[i] - x_puntos[j])
        resultado += termino
    return resultado

def calcular_splines(x, y):
    n = len(x) - 1
    h = np.diff(x)

    # Sistema matricial para Spline Natural (matriz tridiagonal)
    M = np.zeros((n + 1, n + 1))
    B = np.zeros(n + 1)

    # Condiciones de frontera: spline natural (g[0] = g[n] = 0)
    M[0, 0] = 1
    M[n, n] = 1

    for i in range(1, n):
        M[i, i-1] = h[i-1]
        M[i, i]   = 2 * (h[i-1] + h[i])
        M[i, i+1] = h[i]
        B[i] = 6 * ((y[i+1] - y[i]) / h[i] - (y[i] - y[i-1]) / h[i-1])

    # Resolver sistema para segundas derivadas g
    g = np.linalg.solve(M, B)

    # Calcular coeficientes para cada segmento i en [x_i, x_{i+1}]
    # S_i(x) = a*(x-x_i)^3 + b*(x-x_i)^2 + c*(x-x_i) + d
    a = np.zeros(n)
    b = np.zeros(n) 
    c = np.zeros(n)
    d = y[:-1]

    for i in range(n):
        a[i] = (g[i+1] - g[i]) / (6 * h[i])
        b[i] = g[i] / 2
        c[i] = (y[i+1] - y[i]) / h[i] - h[i] * (2*g[i] + g[i+1]) / 6

    return a, b, c, d