# irmof2x-h2-simulations

Crystal structures and example simulation inputs for the molecular study of
hydrogen adsorption and diffusion in **IRMOF-1 (MOF-5)** and its halogenated
**IRMOF-2-X (X = F, Cl, Br, I)** derivatives.

This repository accompanies the manuscript:

> C. Morales-Díaz, A. Mejía, G. Alonso.
> *Halogenation effects on hydrogen storage and transport in IRMOFs.*
> International Journal of Hydrogen Energy (under review), 2026.

It is intended to make the simulations reproducible: the exact framework
structures used in the study, together with representative input files for the
grand canonical Monte Carlo (GCMC), Widom insertion, textural, and molecular
dynamics (MD) calculations.

---

## Contents

```
.
├── README.md
├── LICENSE
├── structures/                 # Framework crystal structures (CIF)
│   ├── IRMOF-1.cif
│   ├── IRMOF-2-F.cif
│   ├── IRMOF-2-Cl.cif
│   ├── IRMOF-2-Br.cif
│   └── IRMOF-2-I.cif
└── examples/                   # Representative input files
    ├── raspa/                  # RASPA2
    │   ├── gcmc/               #   adsorption isotherms (GCMC)
    │   ├── widom/              #   Henry constant & zero-loading isosteric heat
    │   └── textural/           #   He void fraction, pore volume, surface area, PSD
    └── lammps/                 # LAMMPS
        └── diffusion/          #   NVT MD, self-diffusion from the MSD
```

> Note: this is the initial release containing **CIFs and example inputs** only.
> Additional analysis scripts and raw data may be added in later versions.

---

## Structures

| File | Material | Origin |
|------|----------|--------|
| `IRMOF-1.cif`   | IRMOF-1 (MOF-5) | Experimental coordinates of Li et al. (1999) |
| `IRMOF-2-Br.cif`| IRMOF-2-Br      | Experimental unit cell of Eddaoudi et al. (2002) |
| `IRMOF-2-F/Cl/I.cif` | IRMOF-2-F, -Cl, -I | Generated from the IRMOF-2-Br baseline by halogen substitution |

The IRMOF-2-X series was built from the IRMOF-2-Br unit cell by replacing the
bromine substituent with the target halogen and adjusting the C(aryl)–X bond
length to its equilibrium value (CRC Handbook), preserving the substituent
orientation and the isoreticular connectivity. Lattice parameters and atomic
positions are held fixed (rigid framework) throughout the simulations.

---

## Force field

All host–guest and guest–guest interactions use a first-order
Feynman–Hibbs (FH) quantum-corrected effective potential:

- **Framework** Lennard–Jones parameters: Universal Force Field (UFF).
- **Partial charges:** extended Charge Equilibration (QEq).
- **H₂ model:** three-site Darkrim–Levesque model (LJ + point charges on the
  centre of mass and the two H atoms).
- **Mixing rules:** Lorentz–Berthelot; **cutoff:** 12.8 Å (shifted).

The full parameter tables are given in the Supplementary Material of the paper.

---

## Software

| Task | Code |
|------|------|
| GCMC adsorption isotherms, Widom insertion, textural properties | [RASPA2](https://github.com/iRASPA/RASPA2) |
| Molecular dynamics / self-diffusion | [LAMMPS](https://www.lammps.org) |
| Bulk fugacities & SAFT-VRQ-Mie confinement model | [ThermoPack](https://github.com/thermotools/thermopack) |

### Reproducing the calculations (outline)

- **GCMC:** 1×10⁴ equilibration + 2×10⁴ production cycles per pressure point;
  insertion/deletion/translation/rotation moves; Ewald summation (relative
  precision 10⁻⁶). Reservoir fugacities from SAFT-VRQ-Mie.
- **Widom insertion:** test-particle insertions on the empty framework to obtain
  the Henry constant and zero-loading isosteric heat.
- **MD (diffusion):** NVT ensemble, Nosé–Hoover thermostat (0.1 ps), rigid H₂,
  1 fs timestep, 0.5 ns equilibration + 10 ns production, PPPM (10⁻⁶).
  A 2×2×2 supercell is used at low loading. Self-diffusion coefficients are
  obtained from the centre-of-mass mean-squared displacement (Einstein relation,
  multiple time origins).

Paths to the structure files inside the example inputs may need to be adjusted
to your local directory layout.

---

## Citation

If you use these files, please cite the paper:

```bibtex
@article{moralesdiaz_halogenation_2026,
  title   = {Halogenation effects on hydrogen storage and transport in IRMOFs},
  author  = {Morales-D{\'i}az, Carlos and Mej{\'i}a, Andr{\'e}s and Alonso, Gerard},
  journal = {International Journal of Hydrogen Energy},
  year    = {2026},
  note    = {Under review}
}
```

Please also cite the original structure sources (Li et al. 1999; Eddaoudi et
al. 2002) and the simulation codes (RASPA2, LAMMPS, ThermoPack) as appropriate.

---

## License

Released under the **Creative Commons Attribution 4.0 International
(CC-BY-4.0)** license — see `LICENSE`. You are free to share and adapt the
material with attribution.

---

## Contact

Departamento de Ingeniería Química, Universidad de Concepción, Chile.
Corresponding author: Gerard Alonso — <geraralonso@udec.cl>

## Acknowledgements

Funded by ANID (Beca Doctorado Nacional 2022-21220172; FONDECYT 11230012 and
1230654). Computations used the NLHPC supercomputing infrastructure
(CCSS210001).
