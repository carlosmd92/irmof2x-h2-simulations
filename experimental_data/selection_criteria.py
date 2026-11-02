"""Retention criteria for experimental H2 isotherms on IRMOF-1 at 77 K.

The NIST/ARPA-E Adsorption Database indexes many H2 isotherms on IRMOF-1 near
77 K. A fraction carry mislabelled units and report physically impossible
uptakes. Two criteria remove them before the isotherms are used as a reference
distribution:

1. Physical upper bound. The absolute uptake cannot exceed the pore volume
   filled with liquid H2 at its normal boiling point,

       n_max = V_pore * rho_liq / M
             = 1.3812 cm3/g * 70.85 g/L / 2.016 g/mol = 48.5 mol/kg.

   Isotherms whose maximum exceeds 60 mol/kg (24% above this bound, allowing for
   samples with a larger pore volume than the ideal crystal) are discarded.

2. Lower bound. Isotherms whose maximum over the measured range is below
   0.5 mol/kg are discarded as incompatible with IRMOF-1 at 77 K.

Input is a JSON list of isotherm records, one per isotherm:

    [{"DOI": "...", "P": [bar, ...], "A": [mol/kg, ...]}, ...]

Output is a CSV with the inter-laboratory distribution of the retained isotherms
at a set of reference pressures.

Usage:
    python selection_criteria.py isotherms.json dispersion_irmof1_77K.csv
"""
import argparse
import json
from collections import Counter

import numpy as np
import pandas as pd

V_PORE = 1.3812   # cm3/g, accessible pore volume of IRMOF-1
RHO_LIQ = 70.85   # g/L, liquid H2 at its normal boiling point
M = 2.016         # g/mol, H2
N_MAX_PHYS = V_PORE * RHO_LIQ / M   # 48.5 mol/kg

UPPER = 60.0      # mol/kg, discard isotherms whose maximum exceeds this
LOWER = 0.5       # mol/kg, discard isotherms whose maximum is below this
REF_P = [0.5, 1, 2, 5, 10, 20, 30, 50, 80]   # reference pressures (bar)
MIN_CURVES = 5    # minimum isotherms contributing at a pressure for it to be reported


def retain(records):
    """Apply the two criteria; return retained records and the drop log."""
    kept, dropped = [], []
    for r in records:
        A = np.asarray(r["A"], float)
        P = np.asarray(r["P"], float)
        ok = np.isfinite(A) & np.isfinite(P)
        if ok.sum() < 3:
            dropped.append((r["DOI"], "fewer than 3 finite points")); continue
        A, P = A[ok], P[ok]
        if A.max() > UPPER:
            dropped.append((r["DOI"], f"maximum {A.max():.0f} mol/kg above bound")); continue
        if A.max() < LOWER:
            dropped.append((r["DOI"], f"maximum {A.max():.3f} mol/kg below {LOWER}")); continue
        kept.append({"DOI": r["DOI"], "P": P, "A": A})
    return kept, dropped


def distribution(kept):
    """Inter-laboratory distribution of the retained isotherms at REF_P."""
    rows = []
    for p in REF_P:
        contributing = [k for k in kept if k["P"].min() <= p <= k["P"].max()]
        vals = np.array([float(np.interp(p, k["P"], k["A"])) for k in contributing])
        vals = vals[np.isfinite(vals)]
        if vals.size < MIN_CURVES:
            continue
        median = float(np.median(vals))
        p10, p90 = np.percentile(vals, [10, 90])
        rows.append({
            "P_bar": p,
            "n": int(vals.size),
            "n_sources": len({k["DOI"] for k in contributing}),
            "median": round(median, 3),
            "mean": round(float(vals.mean()), 3),
            "std": round(float(vals.std(ddof=1)), 3),
            "cv_pct": round(100 * float(vals.std(ddof=1)) / float(vals.mean()), 1),
            "p10": round(float(p10), 3),
            "p25": round(float(np.percentile(vals, 25)), 3),
            "p75": round(float(np.percentile(vals, 75)), 3),
            "p90": round(float(p90), 3),
            "p10_p90_range_pct": round(100 * (p90 - p10) / median, 1),
        })
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser(description="Apply retention criteria to IRMOF-1 H2 isotherms.")
    ap.add_argument("input", help="JSON list of isotherm records {DOI, P [bar], A [mol/kg]}")
    ap.add_argument("output", help="output CSV for the retained-isotherm distribution")
    args = ap.parse_args()

    records = json.load(open(args.input, encoding="utf-8"))
    kept, dropped = retain(records)

    print(f"physical bound (pore filled with liquid H2): {N_MAX_PHYS:.1f} mol/kg")
    print(f"isotherms read:     {len(records):4d} from {len({r['DOI'] for r in records})} publications")
    print(f"isotherms retained: {len(kept):4d} from {len({k['DOI'] for k in kept})} publications")
    if dropped:
        print("discarded (count by DOI):")
        for doi, count in Counter(d[0] for d in dropped).most_common():
            reason = next(d[1] for d in dropped if d[0] == doi)
            print(f"  {count:3d}  {doi}  ({reason})")

    distribution(kept).to_csv(args.output, index=False)
    print(f"\nwrote {args.output}")


if __name__ == "__main__":
    main()
