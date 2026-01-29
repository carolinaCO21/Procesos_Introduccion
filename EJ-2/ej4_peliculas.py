import multiprocessing
import os

# Para realizar este ejercicio es necesario que definas 2 procesos distintos y un Main:
# Proceso 1: Recibe como parámetros una ruta de fichero y un año. El proceso leerá el fichero el cual almacena en cada línea la información de una película: nombre y año de estreno separados por punto y coma (;). ... Debe enviar al siguiente proceso únicamente aquellas películas que se hayan estrenado en el año introducido por parámetro.
# Proceso 2: Recibirá un número indeterminado de películas y debe almacenarlas en un fichero de nombre peliculasXXXX, donde XXXX es el año de estreno de las películas.
# Main: Pide al usuario que introduzca un año por teclado, debe ser menor al actual. También solicitará la ruta al fichero donde se encuentran almacenadas las películas.

def filtrar_peliculas(year, queue, ruta_fichero):
    """Proceso 1: Lee el fichero y envía a la cola las que coinciden con el año."""
    print(f"P1: Buscando películas del año {year} en {ruta_fichero}...")
    
    try:
        with open(ruta_fichero, "r", encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if not linea: continue
                
                parts = linea.split(";")
                if len(parts) >= 2:
                    # parts[1] es el año (ej: " 1999")
                    movie_year = parts[1].strip()
                    if movie_year == str(year):
                        queue.put(linea)
                        
    except FileNotFoundError:
        print(f"Error: No se encuentra {ruta_fichero}")
    
    # Señal de fin
    queue.put(None)

def escribir_peliculas(ruta_salida, queue):
    """Proceso 2: Lee de la cola y escribe en el fichero especificado solo si hay resultados."""
    # Eliminamos fichero previo si existe para no dejar datos antiguos erróneos
    if os.path.exists(ruta_salida):
        try:
            os.remove(ruta_salida)
        except OSError:
            pass

    print(f"P2: Esperando resultados para {ruta_salida}...")
    
    f = None
    try:
        while True:
            datos = queue.get()
            if datos is None:
                break
            
            # Apertura diferida: solo creamos el fichero si llega el primer dato
            if f is None:
                f = open(ruta_salida, "w", encoding='utf-8')
            
            f.write(datos + "\n")
            print(f" -> Guardada: {datos}")
    finally:
        if f:
            f.close()
        else:
            print("No hay pelis de ese año. No se ha generado fichero.")

if __name__ == "__main__":
    try:
        # Nota: En VS Code la entrada interactiva puede no funcionar bien si no se usa una terminal externa o integrada adecuada.
        # Por defecto, asumiremos valores si falla, pero el ejercicio pide input.
        print("--- Buscador de Películas ---")
        year_input = input("Introduce el año de las películas a buscar (ej. 1999): ").strip()
        ruta_input = input("Introduce la ruta del fichero de películas (Intro para default 'peliculas.txt'): ").strip()
        
        if not ruta_input:
            ruta_input = os.path.join(os.path.dirname(__file__), 'peliculas.txt')

        # Validación simple del año
        if not year_input.isdigit():
            print("El año debe ser un número.")
            exit()
            
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_salida = input("Introduce la ruta/nombre del fichero de salida: ").strip()
        if not ruta_salida:
            ruta_salida = os.path.join(base_dir, f"peliculas{year_input}.txt")
        elif not os.path.isabs(ruta_salida):
            ruta_salida = os.path.join(base_dir, ruta_salida)

        cola = multiprocessing.Queue()
        
        p1 = multiprocessing.Process(target=filtrar_peliculas, args=(year_input, cola, ruta_input))
        p2 = multiprocessing.Process(target=escribir_peliculas, args=(ruta_salida, cola))
        
        p1.start()
        p2.start()
        
        p1.join()
        p2.join()
        
        print("Proceso terminado.")
    except KeyboardInterrupt:
        print("\nCancelado por el usuario.")
    except EOFError:
        print("\nError al leer entrada (posiblemente terminal no interactiva).")
