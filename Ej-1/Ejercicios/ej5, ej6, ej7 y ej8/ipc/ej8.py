"""
Docstring for Multiprocessing.Ejercicio.ej8

En este caso, vuelve a realizar la comunicación entre
 procesos pero usando tuberías (Pipe), de forma que la
   función que se encarga de leer los números del fichero 
   se los envíe (send) al proceso que los suma.
     El proceso que suma los números tiene que recibir (recv) 
     los dos números y realizar la suma entre ellos.
"""

import os
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection

def sumSecuencia(inicio: int, fin: int) -> int:
    # Si inicio es mayor que fin, invertimos los valores para hacer la suma correcta
    if inicio > fin:
        return sum(range(fin, inicio+1))
    return sum(range(inicio, fin+1))


# Función que lee los números del fichero y los envía por la tubería
# Esta función es ejecutada por el proceso productor
def leer_fichero(ruta_fichero: str, emisor: Connection):
    """
    Lee pares de números de un fichero y los envía por la tubería (Pipe).
    Cada línea del fichero debe tener dos números separados por espacio.
    """
    print(f"[Lector] PID={os.getpid()}")
    
    try:
        with open(ruta_fichero, 'r') as archivo:
            for linea in archivo:
                # Eliminar espacios en blanco y saltos de línea
                linea = linea.strip()
                if linea:  # Si la línea no está vacía
                    # Separar los dos números
                    numeros = linea.split()
                    if len(numeros) == 2:
                        inicio = int(numeros[0])
                        fin = int(numeros[1])
                        # Enviar la tupla por la tubería
                        emisor.send((inicio, fin))
                        print(f"[Lector] Enviado: ({inicio}, {fin})")
        
        # Señal de fin: enviar None para indicar que no hay más datos
        emisor.send(None)
        print("[Lector] Fin de lectura - señal enviada")
    
    except FileNotFoundError:
        print(f"[Lector] Error: Fichero {ruta_fichero} no encontrado")
        emisor.send(None)
    
    finally:
        # Cerrar el extremo emisor
        emisor.close()


# Función que recibe números de la tubería y realiza las sumas
# Esta función será ejecutada por el proceso consumidor
def worker_suma(receptor: Connection, emisor_resultados: Connection):
    """
    Recibe pares de números de la tubería (Pipe) y calcula su suma.
    Se detiene cuando recibe None (señal de finalización).
    Envía los resultados al padre por otro Pipe.
    """
    print(f"[Worker] PID={os.getpid()} - Esperando datos")
    resultados = []  # Lista para acumular todos los resultados
    
    while True:
        # Recibir datos de la tubería (bloqueante: espera hasta que haya datos)
        datos = receptor.recv()
        
        # Si recibimos None, es la señal de que no hay más datos
        if datos is None:
            print(f"[Worker] Señal de fin recibida - terminando")
            break
        
        # Desempaquetar los datos
        inicio, fin = datos
        
        # Calcular la suma
        resultado = sumSecuencia(inicio, fin)
        
        # Mostrar el resultado por pantalla
        print(f"[Worker] Suma desde {inicio} hasta {fin}: {resultado}")
        
        # Guardar el resultado para enviarlo al padre
        resultados.append((inicio, fin, resultado))
    
    # Enviar todos los resultados al padre por el segundo Pipe
    emisor_resultados.send(resultados)
    
    # Cerrar los extremos
    receptor.close()
    emisor_resultados.close()


if __name__ == '__main__':
    print(f"[Padre] PID={os.getpid()}")
    
    # Pedir al usuario la ruta del fichero
    ruta_fichero = input("Introduce la ruta del fichero con los números: ").strip()
    
    # Verificar que el fichero existe
    if not os.path.exists(ruta_fichero):
        print(f"[Padre] Error: El fichero '{ruta_fichero}' no existe")
        exit(1)
    
    # Crear DOS tuberías (Pipes) para comunicación entre procesos
    # POR QUÉ 2 PIPES:
    # - Pipe 1 (productor → consumidor): Para enviar datos a procesar
    # - Pipe 2 (consumidor → padre): Para devolver resultados al padre
    # 
    # Cada Pipe es UNIDIRECCIONAL (duplex=False), por tanto:
    # - El productor solo envía, no recibe
    # - El consumidor recibe del productor Y envía al padre
    # - El padre solo recibe resultados, no envía
    # 
    # Si usamos duplex=True (bidireccional), necesitaríamos solo 1 Pipe,
    # pero es menos eficiente y más complejo de gestionar.
    
    # Pipe 1: Productor → Consumidor (para enviar pares de números)
    receptor_datos, emisor_datos = Pipe(duplex=False)
    
    # Pipe 2: Consumidor → Padre (para devolver resultados)
    receptor_resultados, emisor_resultados = Pipe(duplex=False)
    
    # Crear el proceso lector (productor)
    # Este proceso lee el fichero y envía los datos por Pipe 1
    proceso_lector = Process(target=leer_fichero, args=(ruta_fichero, emisor_datos))
    
    # Crear el proceso worker (consumidor)
    # Este proceso recibe datos de Pipe 1 y envía resultados por Pipe 2
    proceso_worker = Process(target=worker_suma, args=(receptor_datos, emisor_resultados))
    
    # Iniciar los procesos
    proceso_lector.start()
    print(f"[Padre] Proceso lector iniciado - PID={proceso_lector.pid}")
    
    proceso_worker.start()
    print(f"[Padre] Worker iniciado - PID={proceso_worker.pid}")
    
    # El proceso padre cierra los extremos del Pipe que no usa
    # Esto es IMPORTANTE para evitar deadlocks:
    # - El padre no envía datos, cierra emisor_datos
    # - El padre no envía resultados, cierra emisor_resultados
    # - El padre no recibe datos, cierra receptor_datos
    emisor_datos.close()
    emisor_resultados.close()
    receptor_datos.close()
    
    # Esperar a que los procesos terminen
    proceso_lector.join()
    print("[Padre] Proceso lector terminado")
    
    proceso_worker.join()
    print("[Padre] Worker terminado")
    
    # Recibir los resultados del worker por el Pipe 2
    resultados = receptor_resultados.recv()
    receptor_resultados.close()
    
    # Mostrar resumen de resultados
    print("\n" + "="*60)
    print("=== RESULTADOS RECIBIDOS DEL WORKER ===")
    print("="*60)
    for inicio, fin, suma in resultados:
        print(f"Rango [{inicio}, {fin}] = {suma}")
    
    suma_total = sum(suma for _, _, suma in resultados)
    print(f"\nSuma total de todas las operaciones: {suma_total}")
    print("="*60)
    
    print("\n[Padre] Todos los procesos han terminado.")