from multiprocessing import Pool
import os
import time

"""
Se mide tiempo_transcurrido: inicio -> fin
varios procesos con Pool


"""


"""

Modifica el ejercicio anterior (ej1 (proceso))para que el programa principal use un Pool para lanzar 
varios procesos de forma concurrente. Cambia el valor del número de procesos y compara 
los tiempos que tarda en ejecutarse en los distintos casos.




"""
def sumSecuencia(hasta: int) -> int:
    total: int = 0
    for i in range(1, hasta + 1):
        total += i
    return total

# Pool espera funciones que retornen valores
def worker(limite: int) -> int:
    print(f"[Hijo] PID={os.getpid()} padre={os.getppid()}")
    total = sumSecuencia(limite)
    print(f"Suma hasta {limite}: {total}")
    return total

if __name__ == "__main__":
    print(f"[Padre] PID={os.getpid()}\n")
    objetivos = [4, 7, 10]
    
    # Probar con diferentes números de procesos en el Pool
    num_procesos_a_probar = [1, 2, 3, 4]
    
    print("=" * 60)
    print("COMPARACIÓN DE TIEMPOS CON DIFERENTES NÚMEROS DE PROCESOS")
    print("=" * 60)
    
    for num_procesos in num_procesos_a_probar:
        print(f"\n--- Pool con {num_procesos} proceso(s) ---")
        
        inicio = time.time()
        """
        Un Pool contiene un número fijo de procesos trabajadores (workers) 
        que se reutilizan para ejecutar tareas.
        Conceptos clave:
        Pool(processes=N) → Crea N procesos que se mantienen vivos
        """
        # with en pool automáticamente llama a pool.close() y pool.join()
        # Crear un Pool de procesos con número específico 
        with Pool(processes=num_procesos) as pool:
            # pool.map aplica worker a cada elemento de objetivos
            resultados = pool.map(worker, objetivos)
        
        fin = time.time()
        tiempo_transcurrido = fin - inicio
        
        print(f"✓ Tiempo con {num_procesos} proceso(s): {tiempo_transcurrido:.4f} segundos")
    
    print("\n" + "=" * 60)
    print("Todos los procesos han terminado.")
    print("=" * 60)
    
    # Más procesos ≠ mejor rendimiento (3-4 procesos son similares o peores)
    # Overhead domina: Crear/gestionar procesos cuesta más que la tarea en

    """
    Con Pool (automático):
    El Pool usa IPC internamente (generalmente Pipes o Queues)
    La función worker simplemente retorna el valor (return total)
    El Pool captura automáticamente el valor retornado y lo envía al padre
    pool.map() devuelve directamente los resultados  
    """