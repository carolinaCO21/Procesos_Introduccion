"""
Docstring for Multiprocessing.Ejercicio.ej4

En este caso, vuelve a realizar la comunicación entre procesos pero usando tuberías (Pipe),
 
 de forma que la función que se encarga de leer los números del fichero se los envíe (send) 
 al proceso que se encarga de la suma. 
 
 El proceso que suma los números tiene que recibir 
 (recv) un número y realizar la suma.
  
   Una vez que el proceso que lee el fichero termine de
   leer números en el fichero, debe enviar un None. El que recibe números dejará de realizar 
   sumas cuando reciba un None.

"""

from __future__ import annotations

import os
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from pathlib import Path
from typing import Iterable


def sumSecuencia(secuencia: tuple[int, ...]) -> int:
  """Devuelve la suma de los elementos de la tupla recibida."""
  return sum(secuencia)


def productor(ruta_fichero: str, emisor: Connection) -> None:
  """Lee números del fichero y los envía por la tubería."""
  print(f"[Productor] PID={os.getpid()} padre={os.getppid()}")
  ruta = Path(ruta_fichero)
  for numero in _leer_numeros(ruta):
    emisor.send(numero)
  # Marca de finalización para que el consumidor sepa cuándo detenerse
  emisor.send(None)
  emisor.close()


def consumidor(receptor: Connection, salida: Connection) -> None:
  """Recibe números por la tubería, calcula la suma y la envía al proceso padre."""
  print(f"[Consumidor] PID={os.getpid()} padre={os.getppid()}")
  numeros: list[int] = []
  while True:
    elemento = receptor.recv()
    if elemento is None:
      break
    numeros.append(int(elemento))
  total = sumSecuencia(tuple(numeros))
  # Se devuelve tanto la secuencia consumida como su suma acumulada
  salida.send((tuple(numeros), total))
  salida.close()
  receptor.close()


def _leer_numeros(ruta: Path) -> Iterable[int]:
  """Genera los números encontrados en el fichero indicado."""
  with ruta.open("r", encoding="utf-8") as fichero:
    for linea in fichero:
      linea_normalizada = linea.strip()
      if not linea_normalizada:
        continue
      if not linea_normalizada.lstrip("+-").isdigit():
        continue
      yield int(linea_normalizada)


if __name__ == "__main__":
  base = Path(__file__).resolve().parent
  fichero_numeros = base / "numeros.txt"
  if not fichero_numeros.exists():
    raise FileNotFoundError(f"No se encontró el fichero {fichero_numeros}")

  # Pipe unidireccional productor->consumidor para los números
  receptor_numeros, emisor_numeros = Pipe(duplex=False)
  # Pipe consumidor->padre para reportar el resultado
  receptor_resultados, emisor_resultados = Pipe(duplex=False)

  proceso_productor = Process(target=productor, args=(str(fichero_numeros), emisor_numeros))
  proceso_consumidor = Process(target=consumidor, args=(receptor_numeros, emisor_resultados))

  proceso_productor.start()
  proceso_consumidor.start()

  # El proceso principal no usa estos extremos y los cierra de inmediato
  emisor_numeros.close()
  receptor_numeros.close()
  emisor_resultados.close()

  proceso_productor.join()
  proceso_consumidor.join()

  numeros, total = receptor_resultados.recv()
  receptor_resultados.close()

  print(f"Numeros recibidos: {numeros}")
  print(f"Suma total recibida: {total}")

