"""
Modifica el ejercicio anterior para usar un Pool
 para lanzar varios procesos de forma concurrente.
 Recuerda que al tener dos argumentos debes usar el
 método starmap en vez de map.

"""

import os
from multiprocessing import Pool

# Función que calcula la suma de una secuencia de números entre inicio y fin (ambos inclusive)
def sumSecuencia(inicio: int, fin: int) -> int:
    # Si inicio es mayor que fin, invertimos los valores para hacer la suma correcta
    if inicio > fin:
        return sum(range(fin, inicio+1))
    return sum(range(inicio, fin+1))


def worker(i: int, f: int):
    # Mostramos el PID del proceso hijo y su proceso padre
    print(f"[Hijo] PID={os.getpid()} padre={os.getppid()}")
    resultado = sumSecuencia(i, f)
    print(f"Suma desde {i} hasta {f}: {resultado}")
    # Retornamos el resultado para que Pool pueda recogerlo
    return resultado

if __name__ == '__main__':
    print(f"[Padre] PID={os.getpid()}")

    ranges = [(1, 4), (3, 7), (5, 10)]

    # Creamos un Pool de procesos
    # Pool gestiona automáticamente un conjunto de procesos worker
    with Pool() as pool:
        # starmap() distribuye las tuplas de 'ranges' entre los procesos del Pool
        # starmap es necesario cuando la función recibe múltiples argumentos
        # map() es para funciones con un solo argumento
        # starmap() desempaqueta cada tupla y pasa los elementos como argumentos separados
        resultados = pool.starmap(worker, ranges)
        
    # El bloque 'with' se asegura de que pool.close() y pool.join() se llamen automáticamente
    # close() 
    # join() espera a que todos los procesos terminen
    
    print("[Padre] Todos los procesos han terminado.")
    print(f"Resultados obtenidos: {resultados}")