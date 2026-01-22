"""
Docstring for Multiprocessing.Ejercicio.ej1 - Versión NO CONCURRENTE

Crea una función en Python que sea capaz de sumar todos los números desde el 1 hasta un valor introducido por parámetro, 
incluyendo ambos valores y mostrar el resultado por pantalla.

Esta versión usa Process pero ejecuta los procesos de forma SECUENCIAL (start + join inmediato).
NO hay paralelismo: cada proceso termina antes de lanzar el siguiente.

"""

from multiprocessing import Process
import os

def sumSecuencia(hasta: int) -> int:
    return sum(range(1, hasta +1))


def worker(limite: int) -> None:
    print(f"[Hijo] PID={os.getpid()} padre={os.getppid()}")
    total = sumSecuencia(limite)
    print(f"Suma hasta {limite}: {total}")


if __name__ == "__main__":
    print(f"[Padre] PID={os.getpid()}")
    objetivos = [4, 7, 10]
    
    # Ejecución SECUENCIAL con Process
    # Cada proceso se lanza y ESPERA a que termine antes de lanzar el siguiente
    for limite in objetivos:
        proceso = Process(target=worker, args=(limite,))
        proceso.start()  # Lanza el proceso
        print(f"[Padre] Lanzado hijo PID={proceso.pid} para {limite}")
        proceso.join()   # ← ESPERA inmediatamente - NO HAY PARALELISMO
    
    print("Todos los procesos han terminado.")


 #cada proceso hijo solo calcula e imprime su resultado. No necesita comunicar nada al padre no IPC