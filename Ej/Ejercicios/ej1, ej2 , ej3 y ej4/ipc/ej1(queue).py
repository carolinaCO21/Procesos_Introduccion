from multiprocessing import Process, Queue
import os

def sumSecuencia(limite:int)-> int:
        #range(inicio, fin) genera una secuencia de números que empieza en inicio y termina uno antes de fin.
    return sum(range(1, limite + 1))

def worker_queue(limite: int, cola: Queue) -> None:
    print(f"[Hijo] PID={os.getpid()} padre={os.getppid()}")
    total = sumSecuencia(limite)
    print(f"Suma hasta {limite}: {total}")
    cola.put((limite, total))  # Envía resultado a la cola

if __name__ == "__main__":
    print(f"[Padre] PID={os.getpid()}")
    objetivos = [4, 7, 10]
    cola = Queue()
    procesos = []

    for limite in objetivos:
        proceso = Process(target=worker_queue, args=(limite, cola))
        proceso.start()
        procesos.append(proceso)
    
    # Esperar a que terminen
    for proceso in procesos:
        proceso.join()
    
    # Recoger resultados de la cola
    resultados = []
    while not cola.empty():
        resultados.append(cola.get())
    
    print(f"Resultados recogidos: {resultados}")
    print("Todos los procesos han terminado.")

    """
En este ejercicio se usó IPC (Inter-Process Communication) mediante una Queue (cola) para 
comunicar los procesos hijos con el proceso padre.

Propósito específico:

Los procesos hijos calculan la suma de secuencias numéricas de concurrente y necesitan enviar 
sus resultados de vuelta al proceso padre. La Queue permite que:

Los procesos hijos envíen sus resultados al padre: cola.put((limite, total)) - cada proceso
 hijo pone su resultado en la cola compartida

El proceso padre recoja los resultados: después de esperar a que terminen todos los procesos
(join()), el padre lee los resultados de la cola con cola.get()

Sin IPC, los procesos hijos calcularían los valores pero no habría forma de comunicar esos
 resultados al proceso padre, ya que cada proceso tiene su propio espacio de memoria aislado.
   La Queue resuelve este problema proporcionando un canal de comunicación seguro entre procesos.
    

    
    """