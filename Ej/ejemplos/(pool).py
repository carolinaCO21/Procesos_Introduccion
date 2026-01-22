from multiprocessing import Pool

def square(number):
    """Funcion que calcula el cuadrado de un numero"""
    return number*number

if __name__ == '__main__':
    # Con Pool indicamos que vamos a tener 3 procesos en paralelo
    with Pool(processes=3) as pool:
        # Creamos una lista con los datos de entrada
        numbers = [1,2,3,4,5]

        # Ejecutamos la función square y le pasamos la lista con los datos
        results = pool.map(square, numbers)

        print("Resultados:", results)
