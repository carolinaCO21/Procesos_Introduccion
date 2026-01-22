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
"""
Usa 2 Pipes:

Pipe productor → consumidor: Para enviar los números
Pipe consumidor → padre: Para devolver el resultado final

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
  # Pedir al usuario la ruta del fichero
  ruta_entrada = input("Introduce la ruta del fichero con los números: ").strip()
  fichero_numeros = Path(ruta_entrada)
  
  # Verificar que el fichero existe
  if not fichero_numeros.exists():
    print(f"Error: El fichero '{fichero_numeros}' no existe")
    exit(1)
  
  # Verificar que es un archivo, no un directorio
  if fichero_numeros.is_dir():
    print(f"Error: '{fichero_numeros}' es un directorio, no un archivo")
    print("Debes especificar la ruta completa del archivo, por ejemplo: numeros.txt")
    exit(1)

  # Crear DOS tuberías (Pipes) para comunicación entre procesos
  # POR QUÉ 2 PIPES:
  # - Pipe 1 (productor → consumidor): Para enviar números a procesar
  # - Pipe 2 (consumidor → padre): Para devolver resultado al padre
  # 
  # Cada Pipe es UNIDIRECCIONAL (duplex=False), por tanto:
  # - El productor solo envía, no recibe
  # - El consumidor recibe del productor Y envía al padre
  # - El padre solo recibe resultados, no envía
  # 
  # Si usamos duplex=True (bidireccional), necesitaríamos solo 1 Pipe,
  # pero es menos eficiente y más complejo de gestionar.
  
  # Pipe 1: Productor → Consumidor (para enviar números)
  receptor_numeros, emisor_numeros = Pipe(duplex=False)
  
  # Pipe 2: Consumidor → Padre (para devolver resultado)
  receptor_resultados, emisor_resultados = Pipe(duplex=False)

  # Crear el proceso productor
  # Este proceso lee el fichero y envía los números por Pipe 1
  proceso_productor = Process(target=productor, args=(str(fichero_numeros), emisor_numeros))
  
  # Crear el proceso consumidor
  # Este proceso recibe números de Pipe 1 y envía el resultado por Pipe 2
  proceso_consumidor = Process(target=consumidor, args=(receptor_numeros, emisor_resultados))

  proceso_productor.start()
  proceso_consumidor.start()

  # El proceso padre cierra los extremos del Pipe que no usa
  # Esto es IMPORTANTE para evitar deadlocks:
  # - El padre no envía números, cierra emisor_numeros
  # - El padre no recibe números, cierra receptor_numeros
  # - El padre no envía resultados, cierra emisor_resultados
  emisor_numeros.close()
  receptor_numeros.close()
  emisor_resultados.close()

  proceso_productor.join()
  proceso_consumidor.join()

  numeros, total = receptor_resultados.recv()
  receptor_resultados.close()

  print(f"Numeros recibidos: {numeros}")
  print(f"Suma total recibida: {total}")

