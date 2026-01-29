"""
Docstring for Multiprocessing.Ejercicio.e5
"""

"""
Crea una función en Python que sea capaz de sumar todos los números comprendidos entre dos valores, incluyendo ambos valores 
 y mostrar el resultado por pantalla. 
 Estos valores se les pasará como argumentos. Hay que tener presente que el primer argumento puede ser mayor que el segundo, 
 y habrá que tenerlo presente para realizar la suma.
 Desde el programa principal crea varios procesos que ejecuten la función anterior. El programa principal debe imprimir un mensaje indicando
 que todos los procesos han terminado después de que los procesos hayan impreso el resultado.


"""

import os
from multiprocessing import Process

def sumSecuencia(inicio:int, fin: int) -> int:
    if inicio > fin:
        return sum(range(fin, inicio+1))
    return sum(range(inicio, fin+1))

def worker(i: int, f: int):
    print(f"[Hijo] PID={os.getpid()} padre={os.getppid()}")
    print(f"Suma desde {i} hasta {f}: {sumSecuencia(i, f)}")

if __name__ == '__main__':
    print(f"[Padre] PID={os.getpid()}")

    ranges = [(1, 4), (3, 7), (5, 10)]
    procesos: list[Process] = []

    for inicio, fin in ranges:
        proceso = Process(target=worker, args=(inicio, fin))
        proceso.start()
        print(f"[Padre] Lanzado hijo PID={proceso.pid} para rango ({inicio}, {fin})")
        procesos.append(proceso)

    for proceso in procesos:
        proceso.join()

    print("[Padre] Todos los procesos han terminado.")



