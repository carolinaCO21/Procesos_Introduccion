from multiprocessing import Process
import os

def saludar(nombre: str) -> None:
    print(f"[HIJO] Hola {nombre}. PID={os.getpid()}")


if __name__ == "__main__":
    print(f"[PADRE]. PID={os.getpid()}")

    p = Process(target = saludar, args=("Ana",))
    p.start()
    p.join()

    print("[PADRE] El proceso ha terminado")


"""
from multiprocessing import Process
import os
import time

def saludar(nombre: str) -> None:
    print(f"[HIJO] Hola {nombre}. PID={os.getpid()}")

  if __name__ == " __main__ ":
    print(f"[PADRE]. PID={os.getpid()}")

    p = Process(target = saludar, args=("Ana", ) )
    inicio = time.perf_counter()
    p.start()
    p.join()
    fin = time.perf_counter()
    tiempo_proceso = fin - inicio
    print("[PADRE] El proceso ha terminado")
    print(f"El proceso ha tardado {tiempo_proceso:



    X

    segundos"



"""