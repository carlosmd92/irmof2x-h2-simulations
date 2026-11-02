"""
Dispersion experimental de H2 en IRMOF-1 a 77 K, con filtro fisico.

El primer paso incluia curvas con captaciones de hasta 217 mol/kg, imposibles.
Provienen de unidades mal etiquetadas en la base, no de los datos originales.

Criterio de exclusion, fisico y no arbitrario: la captacion absoluta no puede
superar el volumen de poro lleno de H2 liquido en su punto de ebullicion normal,

    n_max = V_poro * rho_liq / M = 1.3812 cm3/g * 70.85 g/L / 2.016 g/mol
          = 48.5 mol/kg

Se descarta toda curva cuyo maximo supere 60 mol/kg, un 24 % por encima de esa
cota para dar margen a muestras con volumen de poro mayor al del cristal ideal.
Se descartan tambien las curvas cuyo maximo no llega a 0,5 mol/kg, incompatibles
con IRMOF-1 a 77 K en el rango medido.

Cada curva excluida se reporta con su DOI para que la exclusion sea auditable.
"""
import json
import numpy as np
import pandas as pd

W = r"C:/Users/Alberto/Desktop/remediacion/datos_experimentales"
DAT = W

V_PORO, RHO_LIQ, M = 1.3812, 70.85, 2.016
N_MAX_FIS = V_PORO * RHO_LIQ / M
HI, LO = 60.0, 0.5

rows = json.load(open(f"{DAT}/irmof1_77K_curvas.json", encoding="utf-8"))
print(f"cota fisica (poro lleno de H2 liquido): {N_MAX_FIS:.1f} mol/kg")
print(f"curvas descargadas: {len(rows)}  de {len(set(r['DOI'] for r in rows))} publicaciones\n")

good, bad = [], []
for r in rows:
    A = np.array(r["A"], float)
    P = np.array(r["P"], float)
    m = np.isfinite(A) & np.isfinite(P)
    if m.sum() < 3:
        bad.append((r, "menos de 3 puntos finitos")); continue
    A, P = A[m], P[m]
    if A.max() > HI:
        bad.append((r, f"maximo {A.max():.0f} mol/kg > cota")); continue
    if A.max() < LO:
        bad.append((r, f"maximo {A.max():.3f} mol/kg < 0,5")); continue
    r = dict(r); r["A"], r["P"] = A.tolist(), P.tolist()
    r["Pmin"], r["Pmax"] = float(P.min()), float(P.max())
    good.append(r)

print("=== curvas excluidas ===")
from collections import Counter
for doi, c in Counter(b[0]["DOI"] for b in bad).most_common():
    ej = next(b[1] for b in bad if b[0]["DOI"] == doi)
    print(f"  {c:3d}  {doi}   ({ej})")
print(f"\nretenidas: {len(good)} curvas de {len(set(r['DOI'] for r in good))} publicaciones")

TARGET = [0.5, 1, 2, 5, 10, 20, 30, 50, 80]
stat = []
for p in TARGET:
    v, d = [], []
    for r in good:
        if r["Pmin"] <= p <= r["Pmax"]:
            y = float(np.interp(p, r["P"], r["A"]))
            if np.isfinite(y):
                v.append(y); d.append(r["DOI"])
    if len(v) < 5:
        continue
    v = np.array(v)
    stat.append(dict(P_bar=p, n=len(v), n_doi=len(set(d)),
                     mediana=np.median(v), media=v.mean(), sd=v.std(ddof=1),
                     cv_pct=100 * v.std(ddof=1) / v.mean(),
                     p10=np.percentile(v, 10), p25=np.percentile(v, 25),
                     p75=np.percentile(v, 75), p90=np.percentile(v, 90),
                     rango_p10_p90_pct=100 * (np.percentile(v, 90) - np.percentile(v, 10))
                     / np.median(v)))
s = pd.DataFrame(stat)
s.to_csv(f"{W}/dispersion_irmof1_77K.csv", index=False)
pd.set_option("display.width", 240)
print("\n=== dispersion experimental, IRMOF-1 a 77 K (mol/kg) ===")
print(s[["P_bar", "n", "n_doi", "mediana", "cv_pct", "p10", "p90",
         "rango_p10_p90_pct"]].round(1).to_string(index=False))

CSV = (r"C:/Users/Alberto/Desktop/remediacion/cb_isotermas_resultados/results_cb.csv")
d = pd.read_csv(CSV)
d = d[(d.MOF == "IRMOF-1") & (np.isclose(d["Temperature_[K]"], 77.15))].sort_values("Pressure_[bar]")
print("\n=== posicion de la simulacion en la distribucion experimental ===")
print(f"{'P':>5} {'sim ALA':>8} {'sim ALE':>8} {'mediana':>8} {'pct ALA':>8} {'pct ALE':>8}")
out = []
for _, r in s.iterrows():
    p = r.P_bar
    a = float(np.interp(p, d["Pressure_[bar]"], d["ALA_[mol/kg framework]"]))
    e = float(np.interp(p, d["Pressure_[bar]"], d["ALE_[mol/kg framework]"]))
    v = np.array([float(np.interp(p, x["P"], x["A"])) for x in good
                  if x["Pmin"] <= p <= x["Pmax"]])
    pa, pe = 100 * (v < a).mean(), 100 * (v < e).mean()
    out.append(dict(P_bar=p, sim_ALA=a, sim_ALE=e, mediana=r.mediana,
                    pct_ALA=pa, pct_ALE=pe))
    print(f"{p:5.1f} {a:8.2f} {e:8.2f} {r.mediana:8.2f} {pa:7.0f}% {pe:7.0f}%")
pd.DataFrame(out).to_csv(f"{W}/posicion_simulacion_irmof1.csv", index=False)
json.dump(good, open(f"{DAT}/irmof1_77K_curvas_limpias.json", "w", encoding="utf-8"))
print(f"\n-> {W}/dispersion_irmof1_77K.csv")
print(f"-> {W}/posicion_simulacion_irmof1.csv")
