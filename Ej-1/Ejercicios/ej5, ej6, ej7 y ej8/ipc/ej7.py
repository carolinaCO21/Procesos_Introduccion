"""
Docstring for Multiprocessing.Ejercicio.ej7

Realiza el ejercicio anterior pero esta vez va a 
haber otra función que lea los números de un fichero. 
En el fichero habrá dos números por línea separados por un espacio. 
En este caso, tienes que llevar a cabo una comunicación entre los dos
procesos utilizando colas (Queue), de forma que la función que 
se encarga de leer los números los guarde en la cola, 
y la función que realiza la suma, recibirá la cola y tomará de ahí los dos números.


"""

import os
from multiprocessing import Process, Queue

def sumSecuencia(inicio: int, fin: int) -> int:
    # Si inicio es mayor que fin, invertimos los valores para hacer la suma correcta
    if inicio > fin:
        return sum(range(fin, inicio+1))
    return sum(range(inicio, fin+1))


# Función que lee los números del fichero y los guarda en la cola
# Esta función es ejecutada por el proceso productor
# Recibe: ruta_fichero (str) y cola (Queue compartida entre procesos)
def leer_fichero(ruta_fichero: str, cola: Queue):
    """
    Lee pares de números de un fichero y los coloca en la cola.
    Cada línea del fichero debe tener dos números separados por espacio.
    La cola es compartida con los procesos consumidores (workers).
    """
    print(f"[Lector] PID={os.getpid()} - Leyendo fichero {ruta_fichero}")
    
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
                        # Guardar la tupla en la cola
                        cola.put((inicio, fin))
                        print(f"[Lector] Enviado a la cola: ({inicio}, {fin})")
        
        # Señal de fin: enviar None para indicar que no hay más datos
        cola.put(None)
        print("[Lector] Fin de lectura - señal enviada")
    
    except FileNotFoundError:
        print(f"[Lector] Error: Fichero {ruta_fichero} no encontrado")
        cola.put(None)


# Función worker que toma números de la cola y realiza las sumas
# Esta función será ejecutada por procesos consumidores
def worker_suma(cola: Queue, id_worker: int):
    """
    Toma pares de números de la cola y calcula su suma.
    Se detiene cuando recibe None (señal de finalización).
    Muestra el resultado por pantalla.
    """
    print(f"[Worker-{id_worker}] PID={os.getpid()} - Esperando datos de la cola")
    
    while True:
        # Obtener datos de la cola (bloqueante: espera hasta que haya datos)
        datos = cola.get()
        
        # Si recibimos None, es la señal de que no hay más datos
        if datos is None:
            # Volver a poner None en la cola para que otros workers también puedan terminar
            cola.put(None)
            print(f"[Worker-{id_worker}] Señal de fin recibida - terminando")
            break
        
        # Desempaquetar los datos
        inicio, fin = datos
        
        # Calcular la suma
        resultado = sumSecuencia(inicio, fin)
        
        # Mostrar el resultado por pantalla
        print(f"[Worker-{id_worker}] Suma desde {inicio} hasta {fin}: {resultado}")


if __name__ == '__main__':
    print(f"[Padre] PID={os.getpid()}")
    
    # Pedir al usuario la ruta del fichero
    ruta_fichero = input("Introduce la ruta del fichero con los números: ").strip()
    
    # Verificar que el fichero existe
    if not os.path.exists(ruta_fichero):
        print(f"[Padre] Error: El fichero '{ruta_fichero}' no existe")
        exit(1)
    
    # Crear la cola compartida entre procesos
    # Queue es thread-safe y process-safe, permite comunicación entre procesos
    cola = Queue()
    
    # Crear el proceso lector (productor)
    # Este proceso lee el fichero y coloca los datos en la cola
    proceso_lector = Process(target=leer_fichero, args=(ruta_fichero, cola))
    
    # Crear procesos workers (consumidores)
    # Estos procesos toman datos de la cola y realizan las sumas
    num_workers = 2  # Número de procesos consumidores
    procesos_workers = []
    
    for i in range(num_workers):
        proceso = Process(target=worker_suma, args=(cola, i+1))
        procesos_workers.append(proceso)
    
    # Iniciar todos los procesos
    proceso_lector.start()
    print(f"[Padre] Proceso lector iniciado - PID={proceso_lector.pid}")
    
    for i, proceso in enumerate(procesos_workers):
        proceso.start()
        print(f"[Padre] Worker {i+1} iniciado - PID={proceso.pid}")
    
    # Esperar a que todos los procesos terminen
    proceso_lector.join()
    print("[Padre] Proceso lector terminado")
    
    for i, proceso in enumerate(procesos_workers):
        proceso.join()
        print(f"[Padre] Worker {i+1} terminado")
    
    print("[Padre] Todos los procesos han terminado.")