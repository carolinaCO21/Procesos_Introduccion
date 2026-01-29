"""Version del ejercicio 3 que solicita la secuencia por consola."""

from __future__ import annotations

import os
from multiprocessing import Process, Queue


def sumSecuencia(secuencia: tuple[int, ...]) -> int:
    """Devuelve la suma de todos los elementos de la tupla."""
    return sum(secuencia)


def solicitar_numeros(cola: Queue) -> None:
    """Pide números al usuario y los envía por la cola."""
    print("Introduce números enteros. Pulsa Intro sin escribir nada para terminar.")
    while True:
        entrada = input("Número: ").strip()
        if not entrada:
            break
        if not entrada.lstrip("+-").isdigit():
            print("Valor no válido. Intenta de nuevo.")
            continue
        cola.put(int(entrada))
    cola.put(None)


def consumidor(cola: Queue, resultados: Queue) -> None:
    """Lee números de la cola, calcula la suma y devuelve el total."""
    print(f"[Consumidor] PID={os.getpid()} padre={os.getppid()}")
    numeros: list[int] = []
    while True:
        elemento = cola.get()
        if elemento is None:
            break
        numeros.append(int(elemento))
    total = sumSecuencia(tuple(numeros))
    resultados.put((tuple(numeros), total))


if __name__ == "__main__":
    print(f"[Principal] PID={os.getpid()}")
    cola_numeros: Queue = Queue()
    cola_resultados: Queue = Queue()

    proceso_consumidor = Process(target=consumidor, args=(cola_numeros, cola_resultados))
    proceso_consumidor.start()

    solicitar_numeros(cola_numeros)

    proceso_consumidor.join()

    numeros, total = cola_resultados.get()
    print(f"Números recibidos: {numeros}")
    print(f"Suma total recibida: {total}")
