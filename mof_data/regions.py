import os
import glob

def generar_regiones_lammps(archivo_data, tipo_atomo, archivo_salida, radio_esfera):
    """
    Lee un archivo de datos de LAMMPS, extrae las coordenadas de un tipo de átomo
    y escribe directamente el archivo de regiones de LAMMPS.
    """
    coordenadas = []
    leyendo_atomos = False
    
    try:
        with open(archivo_data, 'r') as f:
            for linea in f:
                linea_limpia = linea.strip()
                
                if "Atoms" in linea_limpia:
                    leyendo_atomos = True
                    continue
                
                # Inicia el bloque de lectura de átomos
                if leyendo_atomos:
                    # Condición de parada: si encontramos una nueva sección, paramos.
                    if "Bonds" in linea_limpia or "Angles" in linea_limpia or "Velocities" in linea_limpia:
                        leyendo_atomos = False
                        break
                    
                    # Si la línea está vacía, la ignoramos y continuamos
                    if not linea_limpia:
                        continue
                    
                    # Si es una línea con datos, la procesamos
                    partes = linea_limpia.split()
                    if int(partes[2]) == tipo_atomo:
                        coordenadas.append([float(partes[4]), float(partes[5]), float(partes[6])])

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de datos '{archivo_data}'")
        return

    if not coordenadas:
        print(f"Advertencia: No se encontraron átomos del tipo {tipo_atomo} en '{archivo_data}'")
        return

    # Escribir el archivo de salida
    with open(archivo_salida, 'w') as f:
        f.write(f"# Archivo de regiones para {os.path.basename(archivo_data)} (generado automáticamente)\n")
        
        id_regiones = []
        for i, (x, y, z) in enumerate(coordenadas):
            id_region = f"zn_esfera_{i+1}"
            id_regiones.append(id_region)
            f.write(f"region {id_region} sphere {x:.4f} {y:.4f} {z:.4f} {radio_esfera}\n")
        
        if id_regiones:
            f.write("\n# Unir todas las esferas en una sola región\n")
            union_cmd = f"region zonas_zn union {len(id_regiones)} {' '.join(id_regiones)}\n"
            f.write(union_cmd)

    print(f"-> Archivo '{archivo_salida}' generado con {len(coordenadas)} regiones.")

# ==============================================================================
#                      ### CONFIGURACIÓN PRINCIPAL ###
# ==============================================================================
mof_info = {
    "IRMOF-1": 9,
    "IRMOF-2-Br": 9,
    "IRMOF-2-Cl": 9,
    "IRMOF-2-F": 9,
    "IRMOF-2-I": 9
}
radio_esfera = 3.5
# ==============================================================================

if __name__ == "__main__":
    archivos_data = glob.glob('*.data')
    if not archivos_data:
        print("No se encontraron archivos .data en esta carpeta.")
    else:
        print(f"Se encontraron {len(archivos_data)} archivos .data para procesar...")

    for data_file in archivos_data:
        base_name = os.path.splitext(os.path.basename(data_file))[0]
        if base_name in mof_info:
            tipo_zn = mof_info[base_name]
            output_file = f"regiones_{base_name}.lammps"
            print(f"\nProcesando '{data_file}'...")
            generar_regiones_lammps(data_file, tipo_zn, output_file, radio_esfera)
        else:
            print(f"\nAdvertencia: El MOF '{base_name}' no está en el diccionario 'mof_info'. Se omitirá.")
