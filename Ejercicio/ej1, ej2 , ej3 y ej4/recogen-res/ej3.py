"""
Docstring for Multiprocessing.Ejercicio.ej3
"""
"""
Realiza el ejercicio anterior pero esta vez va a haber otra función que lea los números de un fichero. 
En el fichero habrá un número por línea.
En este caso, tienes que llevar a cabo una comunicación entre los dos procesos 
utilizando colas (Queue), de forma que la función que se encarga
de leer los números los guarde en la cola, y la función que realiza la suma, recibirá la cola 
y tomará de ahí los números. 

La función que lee el fichero, una vez haya terminado de leer y de añadir elementos a la cola,
debe añadir un objeto None para que el receptor sepa cuándo terminar de leer de la cola.




"""

import os
from multiprocessing import Process, Queue
from pathlib import Path
from typing import Iterable


def sumSecuencia(secuencia: tuple[int, ...]) -> int:
    """Devuelve la suma de los elementos de la tupla recibida."""
    return sum(secuencia)


def productor(ruta_fichero: str, cola: Queue) -> None:
    """Lee números del fichero y los deposita en la cola compartida."""
    print(f"[Productor] PID={os.getpid()} padre={os.getppid()}")
    ruta = Path(ruta_fichero)
    for numero in _leer_numeros(ruta):
        cola.put(numero)
    cola.put(None)


def consumidor(cola: Queue, resultados: Queue) -> None:
    """Extrae los números de la cola, los suma y publica el total."""
    print(f"[Consumidor] PID={os.getpid()} padre={os.getppid()}")
    numeros: list[int] = []
    while True:
        elemento = cola.get()
        if elemento is None:
            break
        numeros.append(int(elemento))
    total = sumSecuencia(tuple(numeros))
    resultados.put(total)

"""
leer → yield → reanudar se conoce como evaluación perezosa (lazy evaluation). 
Cada llamada a next() sobre el generador hace que se lea la siguiente línea, se procese 
y se entregue el número, manteniendo el estado suspendido entre emisiones.
Ese “estado suspendido” evita recomenzar desde cero en cada iteración.


"""
def _leer_numeros(ruta: Path) -> Iterable[int]:
    """Genera los números encontrados en el fichero indicado."""
    # Abre el archivo en modo lectura de texto usando UTF-8
    #para abrir el archivo que apunta Path en modo lectura de texto; la "r" indica “read” y encoding="utf-8" garantiza que los caracteres se interpreten con UTF-8.
    with ruta.open("r", encoding="utf-8") as fichero:
        # Recorre cada línea del fichero secuencialmente
        for linea in fichero:
            # Elimina espacios y saltos de línea en los extremos
            linea_normalizada = linea.strip()
            # Omite líneas vacías o con solo espacios
            if not linea_normalizada:
                continue
            # Verifica que la cadena represente un entero válido
            if not linea_normalizada.lstrip("+-").isdigit():
                continue
            # Convierte la cadena limpia a entero y la emite
            yield int(linea_normalizada)


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    fichero_numeros = base / "numeros.txt"
    if not fichero_numeros.exists():
        raise FileNotFoundError(f"No se encontró el fichero {fichero_numeros}")

    cola_numeros: Queue = Queue()
    cola_resultados: Queue = Queue()

    proceso_productor = Process(target=productor, args=(str(fichero_numeros), cola_numeros))
    proceso_consumidor = Process(target=consumidor, args=(cola_numeros, cola_resultados))

    proceso_productor.start()
    proceso_consumidor.start()

    proceso_productor.join()
    proceso_consumidor.join()

    total = cola_resultados.get()
    print(f"Suma total recibida: {total}")

