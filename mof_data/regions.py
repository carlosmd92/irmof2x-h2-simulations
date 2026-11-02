import os
import glob


def write_region_file(data_file, atom_type, output_file, sphere_radius):
    """Read a LAMMPS data file, extract the coordinates of one atom type, and
    write the corresponding LAMMPS region file: one sphere per atom plus their
    union."""
    coords = []
    reading_atoms = False

    try:
        with open(data_file, "r") as f:
            for line in f:
                stripped = line.strip()

                if "Atoms" in stripped:
                    reading_atoms = True
                    continue

                if reading_atoms:
                    # stop at the next section
                    if "Bonds" in stripped or "Angles" in stripped or "Velocities" in stripped:
                        reading_atoms = False
                        break
                    if not stripped:
                        continue
                    parts = stripped.split()
                    if int(parts[2]) == atom_type:
                        coords.append([float(parts[4]), float(parts[5]), float(parts[6])])

    except FileNotFoundError:
        print(f"Error: data file '{data_file}' not found")
        return

    if not coords:
        print(f"Warning: no atoms of type {atom_type} found in '{data_file}'")
        return

    with open(output_file, "w") as f:
        f.write(f"# Zn-sphere regions for {os.path.basename(data_file)}\n")
        region_ids = []
        for i, (x, y, z) in enumerate(coords):
            region_id = f"zn_sphere_{i + 1}"
            region_ids.append(region_id)
            f.write(f"region {region_id} sphere {x:.4f} {y:.4f} {z:.4f} {sphere_radius}\n")
        if region_ids:
            f.write("\n# Union of all spheres into a single region\n")
            f.write(f"region zn_zones union {len(region_ids)} {' '.join(region_ids)}\n")

    print(f"-> wrote '{output_file}' with {len(coords)} regions")


# Zn atom type (column 3 of the Atoms section) for each framework
MOF_ZN_TYPE = {
    "IRMOF-1": 9,
    "IRMOF-2-Br": 9,
    "IRMOF-2-Cl": 9,
    "IRMOF-2-F": 9,
    "IRMOF-2-I": 9,
}
SPHERE_RADIUS = 3.5

if __name__ == "__main__":
    data_files = glob.glob("*.data")
    if not data_files:
        print("No .data files found in this directory.")
    for data_file in data_files:
        base = os.path.splitext(os.path.basename(data_file))[0]
        if base in MOF_ZN_TYPE:
            output_file = f"regions_{base}.lammps"
            print(f"\nProcessing '{data_file}'...")
            write_region_file(data_file, MOF_ZN_TYPE[base], output_file, SPHERE_RADIUS)
        else:
            print(f"\nWarning: framework '{base}' not in MOF_ZN_TYPE; skipped.")
