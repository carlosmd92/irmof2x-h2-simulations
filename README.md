# irmof2x-h2-simulations

Crystal structures and example simulation inputs for hydrogen adsorption and
diffusion in **IRMOF-1 (MOF-5)** and its halogenated **IRMOF-2-X (X = F, Cl, Br, I)**
derivatives.

Accompanies: C. Morales-Díaz, A. Mejía, G. Alonso, *Halogenation effects on
hydrogen storage and transport in IRMOFs*, International Journal of Hydrogen
Energy (under review), 2026.

## Contents

```
neutral_cif/                  Framework structures (CIF): IRMOF-1 and IRMOF-2-X
mof_data/                     Supporting framework data used by the inputs
simulation.input.template     RASPA2 input template (GCMC / Widom / textural)
in.lammps.template            LAMMPS input template (NVT MD, self-diffusion)
```

The IRMOF-2-X structures were built from the IRMOF-2-Br unit cell
(Eddaoudi et al. 2002) by halogen substitution with equilibrium C(aryl)–X bond
lengths; IRMOF-1 follows Li et al. (1999). Frameworks are rigid.

## Usage

Interactions use UFF Lennard-Jones parameters, QEq charges, the three-site
Darkrim–Levesque H₂ model, and a first-order Feynman–Hibbs quantum correction.
Run GCMC / Widom / textural calculations with [RASPA2](https://github.com/iRASPA/RASPA2)
and MD diffusion with [LAMMPS](https://www.lammps.org). Edit the `.template`
files to set the framework, temperature, and pressure for each run.

## Citation

```bibtex
@article{moralesdiaz_halogenation_2026,
  title   = {Halogenation effects on hydrogen storage and transport in IRMOFs},
  author  = {Morales-D{\'i}az, Carlos and Mej{\'i}a, Andr{\'e}s and Alonso, Gerard},
  journal = {International Journal of Hydrogen Energy},
  year    = {2026},
  note    = {Under review}
}
```

## License

CC-BY-4.0 — see [`LICENSE`](LICENSE).

## Contact
Carlos Morales-Díaz - <cmoralesd@udec.cl>
Gerard Alonso - <geraralonso@udec.cl>
Departamento de Ingeniería Química, Universidad de Concepción, Chile.
