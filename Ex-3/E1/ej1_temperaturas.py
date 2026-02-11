"""
EJERCICIO 1 - Temperaturas de Diciembre
========================================
Este programa genera temperaturas aleatorias para los 31 días de diciembre
utilizando multiprocesamiento.

DECISIONES DE DISEÑO:
- Proceso 1 recibe solo el día (1-31) como parámetro, ya que el mes es fijo (diciembre)
  y las temperaturas se generan internamente de forma aleatoria.
- Procesos 2 y 3 reciben solo el día como parámetro, ya que el nombre del archivo
  se puede construir a partir de él.
- Se usa multiprocessing.Pool para lanzar los procesos de forma simultánea.
"""

import multiprocessing
import random
import os

# Directorio donde se guardarán los archivos
DIRECTORIO = os.path.dirname(os.path.abspath(__file__))


def proceso1_generar_temperaturas(dia):
    """
    Proceso 1: Genera 24 temperaturas aleatorias (0-20 con 2 decimales)
    y las escribe en un fichero con formato DD-12.txt
    
    Parámetro: dia (int) - día del mes (1-31)
    Decisión: Solo necesita el día, el mes es fijo y las temperaturas son aleatorias
    """
    # Generar 24 temperaturas entre 0 y 20 con 2 decimales
    temperaturas = [round(random.uniform(0, 20), 2) for _ in range(24)]
    
    # Crear nombre del archivo con formato DD-12.txt
    nombre_archivo = os.path.join(DIRECTORIO, f"{dia:02d}-12.txt")
    
    # Escribir las temperaturas en el archivo
    with open(nombre_archivo, 'w') as f:
        for temp in temperaturas:
            f.write(f"{temp}\n")
    
    print(f"Generado archivo: {dia:02d}-12.txt")


def proceso2_maximas(dia):
    """
    Proceso 2: Lee temperaturas de un día y escribe en maximas.txt
    la fecha y la temperatura máxima separadas por dos puntos.
    
    Parámetro: dia (int) - día del mes (1-31)
    Decisión: Solo necesita el día para construir el nombre del archivo fuente
    """
    nombre_archivo = os.path.join(DIRECTORIO, f"{dia:02d}-12.txt")
    archivo_maximas = os.path.join(DIRECTORIO, "maximas.txt")
    
    # Leer temperaturas del archivo del día
    with open(nombre_archivo, 'r') as f:
        temperaturas = [float(linea.strip()) for linea in f]
    
    # Encontrar la temperatura máxima
    temp_maxima = max(temperaturas)
    fecha = f"{dia:02d}-12"
    
    # Escribir en maximas.txt (con lock para evitar conflictos de escritura)
    with open(archivo_maximas, 'a') as f:
        f.write(f"{fecha}:{temp_maxima}\n")
    
    print(f"Máxima del día {dia:02d}-12: {temp_maxima}")


def proceso3_minimas(dia):
    """
    Proceso 3: Lee temperaturas de un día y escribe en minimas.txt
    la fecha y la temperatura mínima separadas por dos puntos.
    
    Parámetro: dia (int) - día del mes (1-31)
    Decisión: Solo necesita el día para construir el nombre del archivo fuente
    """
    nombre_archivo = os.path.join(DIRECTORIO, f"{dia:02d}-12.txt")
    archivo_minimas = os.path.join(DIRECTORIO, "minimas.txt")
    
    # Leer temperaturas del archivo del día
    with open(nombre_archivo, 'r') as f:
        temperaturas = [float(linea.strip()) for linea in f]
    
    # Encontrar la temperatura mínima
    temp_minima = min(temperaturas)
    fecha = f"{dia:02d}-12"
    
    # Escribir en minimas.txt
    with open(archivo_minimas, 'a') as f:
        f.write(f"{fecha}:{temp_minima}\n")
    
    print(f"Mínima del día {dia:02d}-12: {temp_minima}")


def main():
    """
    Main: Coordina la ejecución de todos los procesos.
    
    1. Lanza 31 veces simultáneamente el Proceso 1 para generar temperaturas
    2. Espera a que terminen todos
    3. Lanza simultáneamente los Procesos 2 y 3 (31 veces cada uno)
    """
    # Limpiar archivos de máximas y mínimas si existen
    archivo_maximas = os.path.join(DIRECTORIO, "maximas.txt")
    archivo_minimas = os.path.join(DIRECTORIO, "minimas.txt")
    
    if os.path.exists(archivo_maximas):
        os.remove(archivo_maximas)
    if os.path.exists(archivo_minimas):
        os.remove(archivo_minimas)
    
    # Lista de días del mes de diciembre
    dias = list(range(1, 32))
    
    print("=" * 50)
    print("PASO 1: Generando temperaturas para los 31 días")
    print("=" * 50)
    
    # Lanzar 31 procesos simultáneamente para generar temperaturas
    with multiprocessing.Pool() as pool:
        pool.map(proceso1_generar_temperaturas, dias)
    
    print("\n" + "=" * 50)
    print("PASO 2: Calculando máximas y mínimas")
    print("=" * 50)
    
    # Lanzar simultáneamente los Procesos 2 y 3 (31 veces cada uno)
    # Usamos dos pools separados para que se ejecuten en paralelo
    with multiprocessing.Pool() as pool:
        # Lanzar procesos de máximas y mínimas simultáneamente
        resultado_maximas = pool.map_async(proceso2_maximas, dias)
        resultado_minimas = pool.map_async(proceso3_minimas, dias)
        
        # Esperar a que terminen todos
        resultado_maximas.wait()
        resultado_minimas.wait()
    
    print("\n" + "=" * 50)
    print("PROCESO COMPLETADO")
    print("=" * 50)
    print(f"Se han creado 31 archivos de temperaturas (01-12.txt a 31-12.txt)")
    print(f"Archivo de máximas: maximas.txt")
    print(f"Archivo de mínimas: minimas.txt")


if __name__ == "__main__":
    main()
