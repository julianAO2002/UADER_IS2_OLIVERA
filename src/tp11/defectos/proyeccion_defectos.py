"""Projection of the total number of defects (mu0) from early test data.

Two approximate regression models are fitted on the cumulative defects:

1. Exponential (Goel-Okumoto): mu(t) = mu0 * (1 - exp(-b * t)).
   For each b in a grid the best mu0 is obtained by linear least squares
   and the pair with the lowest squared error is kept.
2. Linear rate model: defects found in a period vs cumulative defects
   before it, d_t = a - k * M_(t-1). The x-intercept a / k estimates mu0.

Usage: python proyeccion_defectos.py   (writes the PNG charts next to it)
"""

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

AQUI = pathlib.Path(__file__).parent

DATASETS = {
    "aplicativo": {
        "titulo": "Aplicativo (dias de test)",
        "eje": "Dia",
        "defectos": [9, 18, 5, 7, 23, 2, 8],
    },
    "collatz": {
        "titulo": "Collatz (sesiones S1..S9)",
        "eje": "Sesion",
        "defectos": [8, 6, 1, 1, 1, 9, 0, 8, 0],
    },
}


def ajuste_exponencial(t, acumulado):
    """Fit mu(t) = mu0 * (1 - exp(-b t)); return (mu0, b, sse)."""
    mejor = (0.0, 0.0, float("inf"))
    for b in np.linspace(0.001, 3, 30000):
        forma = 1 - np.exp(-b * t)
        mu0 = float(forma @ acumulado / (forma @ forma))
        sse = float(((acumulado - mu0 * forma) ** 2).sum())
        if sse < mejor[2]:
            mejor = (mu0, float(b), sse)
    return mejor


def ajuste_lineal_tasa(defectos, acumulado):
    """Fit d_t = a - k * M_(t-1); return (mu0, a, k)."""
    previo = np.concatenate(([0.0], acumulado[:-1]))
    pendiente, ordenada = np.polyfit(previo, defectos, 1)
    k = -pendiente
    mu0 = ordenada / k if k > 0 else float("inf")
    return float(mu0), float(ordenada), float(k)


def analizar(nombre, datos):
    """Print the projection of one dataset and save its chart."""
    defectos = np.array(datos["defectos"], dtype=float)
    acumulado = defectos.cumsum()
    t = np.arange(1, len(defectos) + 1, dtype=float)
    mu0_exp, b, sse = ajuste_exponencial(t, acumulado)
    mu0_lin, a, k = ajuste_lineal_tasa(defectos, acumulado)
    r2 = 1 - sse / float(((acumulado - acumulado.mean()) ** 2).sum())

    print("== %s ==" % datos["titulo"])
    print("defectos      :", datos["defectos"])
    print("acumulado     :", acumulado.astype(int).tolist())
    print("exponencial   : mu0 = %.1f  b = %.4f  R2 = %.3f" % (mu0_exp, b, r2))
    print("lineal (tasa) : mu0 = %.1f  a = %.2f  k = %.4f" % (mu0_lin, a, k))
    print("detectados    : %d  ->  pendientes (exp) = %.1f"
          % (acumulado[-1], mu0_exp - acumulado[-1]))
    print()

    horizonte = np.linspace(0, len(t) * 3, 300)
    plt.figure(figsize=(7, 4))
    plt.step(t, acumulado, where="post", label="Acumulado observado")
    plt.plot(t, acumulado, "o")
    plt.plot(horizonte, mu0_exp * (1 - np.exp(-b * horizonte)),
             label="Exponencial mu0=%.1f" % mu0_exp)
    plt.axhline(mu0_exp, ls="--", lw=0.8, color="gray")
    plt.xlabel(datos["eje"])
    plt.ylabel("Defectos acumulados")
    plt.title(datos["titulo"])
    plt.legend()
    plt.tight_layout()
    plt.savefig(AQUI / ("proyeccion_%s.png" % nombre), dpi=110)
    plt.close()
    return mu0_exp, mu0_lin


if __name__ == "__main__":
    for clave, valores in DATASETS.items():
        analizar(clave, valores)
