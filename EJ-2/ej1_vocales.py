import multiprocessing
import os

# 1. Crea un proceso que cuente las vocales de un fichero de texto.
#  Para ello crea una función que reciba una vocal y devuelva cuántas
#  veces aparece en un fichero. Lanza el proceso de forma paralela 
# para las 5 vocales. Tras lanzarse se imprimirá el resultado por pantalla.

def contar_vocal(vocal, ruta_fichero):
    """Cuenta las ocurrencias de una vocal específica en el fichero."""
    try:
        with open(ruta_fichero, 'r', encoding='utf-8') as f:
            texto = f.read().lower()
            cantidad = texto.count(vocal)
            print(f"Proceso {multiprocessing.current_process().name} - La vocal '{vocal}' aparece {cantidad} veces.")
    except FileNotFoundError:
        print(f"Error: El fichero no se encuentra en {ruta_fichero}")

if __name__ == "__main__":
    # Ruta relativa al fichero about.txt
    ruta_fichero = os.path.join(os.path.dirname(__file__), 'about.txt')
    vocales = ['a', 'e', 'i', 'o', 'u']
    procesos = []

    print(f"Iniciando conteo de vocales en: {os.path.abspath(ruta_fichero)}\n")

    for vocal in vocales:
        # Creamos un proceso por cada vocal
        p = multiprocessing.Process(target=contar_vocal, args=(vocal, ruta_fichero), name=f"Contador-{vocal.upper()}")
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()

    print("\nTodos los procesos han terminado.")
