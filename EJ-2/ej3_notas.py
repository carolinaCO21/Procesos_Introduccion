import multiprocessing
import random
import os
import time

# En este ejercicio debes implementar los siguientes procesos y el Main como se explica a continuación:
# Proceso 1: Genera 6 números aleatorios entre 1 y 10, ambos inclusive, y los guarda en un fichero. Estos números deben contener decimales. La ruta a este fichero se le indicará como parámetro de entrada. Estos 6 números representan las notas de un alumno.
# Proceso 2: Lee un fichero pasado por parámetro que contiene las notas de un alumno, cada una en una línea distinta, y realiza la media de las notas. ... Esta media se almacenará en un fichero de nombre medias.txt. Al lado de cada media debe aparecer el nombre del alumno, separados por un espacio.
# Proceso 3: Lee el fichero medias.txt. En cada línea del fichero aparecerá una nota, un espacio y el nombre del alumno. Este proceso debe leer el fichero y obtener la nota máxima. Imprimirá por pantalla la nota máxima junto con el nombre del alumno que la ha obtenido.
# Main: Lanza 10 veces el primer proceso de forma concurrente... 10 ficheros distintos con las notas de cada alumno.
# A continuación, se debe lanzar el proceso 2 ... Por lo que el proceso 2 se lanzará 10 veces también, una por cada fichero generado por el proceso 1, y realizarlo todo de forma simultánea/concurrente.
# Por último, debe lanzarse el proceso 3.

def crear_ficha_alumno(student_id, basedir):
    """Proceso 1: Crea un fichero AlumnoN.txt con notas aleatorias (float)."""
    filename = os.path.join(basedir, f"Alumno{student_id}.txt")
    try:
        with open(filename, "w") as f:
            # Generamos 6 notas decimales entre 1 y 10
            notas = [f"{random.uniform(1, 10):.2f}" for _ in range(6)]
            f.write("\n".join(notas))
    except Exception as e:
        print(f"Error creando {filename}: {e}")

def calcular_media(student_id, lock, basedir):
    """Proceso 2: Lee AlumnoN.txt, calcula media y escribe en medias.txt (protegido por Lock)."""
    in_filename = os.path.join(basedir, f"Alumno{student_id}.txt")
    out_filename = os.path.join(basedir, "medias.txt")
    alumno_name = f"Alumno{student_id}"
    
    try:
        with open(in_filename, "r") as f:
            lines = f.readlines()
            notas = [float(line.strip()) for line in lines if line.strip()]
            
        if notas:
            promedio = sum(notas) / len(notas)
            
            # Sección crítica: escribir en el archivo compartido
            lock.acquire()
            try:
                with open(out_filename, "a") as f_out:
                    # Formato: nota espacio nombre
                    f_out.write(f"{promedio:.2f} {alumno_name}\n")
            finally:
                lock.release()
                
    except FileNotFoundError:
        print(f"No se encontró {in_filename}")

def buscar_maximo(basedir):
    """Proceso 3: Lee medias.txt y muestra la nota más alta."""
    filename = os.path.join(basedir, "medias.txt")
    max_nota = -1.0
    mejor_alumno = ""
    
    try:
        if not os.path.exists(filename):
            print("No hay fichero de medias.")
            return

        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(" ")
                if len(parts) >= 2:
                    # Formato: nota nombre
                    try:
                        nota = float(parts[0])
                        alumno = parts[1]
                        if nota > max_nota:
                            max_nota = nota
                            mejor_alumno = alumno
                    except ValueError:
                        continue
        
        print(f"\n--- Resultado Final ---")
        print(f"La nota máxima es {max_nota} obtenida por {mejor_alumno}")
        
    except Exception as e:
        print(f"Error leyendo medias: {e}")

if __name__ == "__main__":
    basedir = os.path.dirname(os.path.abspath(__file__))
    
    # Limpieza previa
    medias_path = os.path.join(basedir, "medias.txt")
    if os.path.exists(medias_path):
        os.remove(medias_path)
        
    # Paso 1: Crear ficheros de alumnos concurrentemente
    print("Main: Lanzando creación de 10 ficheros de alumnos...")
    ps_creacion = []
    for i in range(1, 11):
        p = multiprocessing.Process(target=crear_ficha_alumno, args=(i, basedir))
        ps_creacion.append(p)
        p.start()
    
    for p in ps_creacion:
        p.join()
        
    # Paso 2: Calcular medias concurrentemente (usando Lock)
    print("Main: Lanzando cálculo de medias concurrentemente...")
    lock = multiprocessing.Lock()
    ps_calculo = []
    for i in range(1, 11):
        p = multiprocessing.Process(target=calcular_media, args=(i, lock, basedir))
        ps_calculo.append(p)
        p.start()
        
    for p in ps_calculo:
        p.join()
        
    # Paso 3: Buscar máximo
    print("Main: Buscando nota máxima...")
    p_final = multiprocessing.Process(target=buscar_maximo, args=(basedir,))
    p_final.start()
    p_final.join()
