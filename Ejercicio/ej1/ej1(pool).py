from multiprocessing import Pool
import os

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
    print(f"[Padre] PID={os.getpid()}")
    objetivos = [4, 7, 10]
    
    # Crear un Pool de procesos
    # with asegura que el pool se cierra correctamente (equivalente a llamar pool.close() y pool.join())
    with Pool() as pool:
        # pool.map aplica worker a cada elemento de objetivos
        # pool.map() ejecuta la función en paralelo para cada valor y devuelve una lista con los resultados
        resultados = pool.map(worker, objetivos)
    
    # Los prints ya se hicieron dentro de worker, resultados contiene los valores retornados
    print("Todos los procesos han terminado.")