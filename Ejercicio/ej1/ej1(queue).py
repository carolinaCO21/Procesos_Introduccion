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