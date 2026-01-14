"""
Docstring for Multiprocessing.Ejercicio.ej4

En este caso, vuelve a realizar la comunicación entre procesos pero usando tuberías (Pipe), de forma que la función que se encarga de leer los números del fichero se los envíe (send) al proceso que se encarga de la suma. El proceso que suma los números tiene que recibir (recv) un número y realizar la suma. Una vez que el proceso que lee el fichero termine de leer números en el fichero, debe enviar un None. El que recibe números dejará de realizar sumas cuando reciba un None.

"""