"""
Docstring for Multiprocessing.Ejercicio.ej3

Realiza el ejercicio anterior pero esta vez va a haber otra función que lea los números de un fichero. En el fichero habrá un número por línea. En este caso, tienes que llevar a cabo una comunicación entre los dos procesos utilizando colas (Queue), de forma que la función que se encarga de leer los números los guarde en la cola, y la función que realiza la suma, recibirá la cola y tomará de ahí los números. La función que lee el fichero, una vez haya terminado de leer y de añadir elementos a la cola, debe añadir un objeto None para que el receptor sepa cuándo terminar de leer de la cola.

"""