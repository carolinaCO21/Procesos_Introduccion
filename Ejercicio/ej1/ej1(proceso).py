"""
Docstring for Multiprocessing.Ejercicio.ej1

Crea una función en Python que sea capaz de sumar todos los números desde el 1 hasta un valor introducido por parámetro, 
incluyendo ambos valores y mostrar el resultado por pantalla.

Desde el programa principal crea varios procesos que ejecuten la función anterior. 
El programa principal debe imprimir un mensaje indicando que todos los procesos han terminado después 
de que los procesos hayan impreso el resultado.


"""

from multiprocessing import Process
from typing import List
import os

def sumSecuencia(hasta: int) -> int:
    total: int = 0
    for i in range(1, hasta + 1):
        total += i

    return total


def worker(limite: int) -> None:
    print(f"[Hijo] PID={os.getpid()} padre={os.getppid()}")
    total = sumSecuencia(limite)
    print(f"Suma hasta {limite}: {total}")

# Aqui tenemos un control sobre cuando arranca o termina cada hijo en concreto
if __name__ == "__main__":
    print(f"[Padre] PID={os.getpid()}")
    objetivos = [4, 7, 10]
    procesos: List[Process] = []

    for limite in objetivos:
        #proceso por objetivo
        proceso = Process(target=worker, args=(limite,))
        # lanza cada suma en paralelo
        proceso.start() # ← Lanza INMEDIATAMENTE cada proceso
        print(f"[Padre] Lanzado hijo PID={proceso.pid} para {limite}")
        #almacenamos la referencia para poder sincronizar después
        procesos.append(proceso)
    #recorre las referencias guardadas y llama a join(); esto bloquea al proceso principal hasta que cada hijo termina su impresión
    for proceso in procesos:
        proceso.join() # ← Espera a que terminen DESPUÉS de lanzarlos todos

    print("Todos los procesos han terminado.")



    """
    multiprocessing.Pool: 
    colocar sumSecuencia como función pura que devuelve la suma, crear un Pool, 
    ejecutar pool.map(sumSecuencia, objetivos) y luego iterar sobre los resultados para imprimirlos. 
    El pool te aporta reutilización de procesos para muchos límites, aunque ya no controlas individualmente 
    el ciclo de cada hijo ni ves sus PIDs directamente.
    
    
    
    
    
    """