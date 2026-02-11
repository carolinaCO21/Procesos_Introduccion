"""
EJERCICIO 2 - Filtrado de Empleados por Departamento y Salario
===============================================================
El programa filtra empleados de un fichero usando tres procesos
que se comunican mediante Pipes.

DECISIONES DE DISEÑO:
- Se usan Pipes como medio de comunicación entre procesos, ya que es el más
  apropiado para enviar datos secuenciales de un proceso a otro.
- Proceso 1 recibe: departamento y conexión de envío al Proceso 2
- Proceso 2 recibe: salario mínimo, conexión de recepción del Proceso 1,
  y conexión de envío al Proceso 3
- Proceso 3 recibe: conexión de recepción del Proceso 2
- Se envía "FIN" como señal de terminación entre procesos
"""

import multiprocessing
import os

# Directorio donde están los archivos
DIRECTORIO = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_SALARIOS = os.path.join(DIRECTORIO, "salarios.txt")
ARCHIVO_EMPLEADOS = os.path.join(DIRECTORIO, "empleados.txt")


def proceso1_filtrar_departamento(departamento, conn_envio):
    """
    Proceso 1: Lee el fichero salarios.txt y envía al Proceso 2
    las líneas que contengan el departamento especificado.
    Envía las líneas SIN el campo departamento.
    
    Parámetros:
    - departamento: nombre del departamento a filtrar
    - conn_envio: conexión Pipe para enviar datos al Proceso 2
    
    Decisión: Necesita el departamento para filtrar y la conexión
    para comunicarse con el siguiente proceso.
    """
    try:
        with open(ARCHIVO_SALARIOS, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    # Formato: Apellido Nombre Departamento Salario
                    partes = linea.split()
                    if len(partes) >= 4:
                        apellido = partes[0]
                        nombre = partes[1]
                        depto = partes[2]
                        salario = partes[3]
                        
                        # Filtrar por departamento
                        if depto.upper() == departamento.upper():
                            # Enviar línea SIN el departamento
                            linea_sin_depto = f"{apellido} {nombre} {salario}"
                            conn_envio.send(linea_sin_depto)
                            print(f"P1 -> P2: {linea_sin_depto}")
        
        # Señal de fin
        conn_envio.send("FIN")
        print("P1: Finalizado")
    finally:
        conn_envio.close()


def proceso2_filtrar_salario(salario_minimo, conn_recepcion, conn_envio):
    """
    Proceso 2: Recibe líneas del Proceso 1 y envía al Proceso 3
    aquellas cuyo salario sea >= al salario mínimo.
    
    Parámetros:
    - salario_minimo: salario mínimo para filtrar
    - conn_recepcion: conexión Pipe para recibir datos del Proceso 1
    - conn_envio: conexión Pipe para enviar datos al Proceso 3
    
    Decisión: Necesita el salario mínimo, conexión de entrada y de salida.
    """
    try:
        while True:
            linea = conn_recepcion.recv()
            
            if linea == "FIN":
                break
            
            # Formato recibido: Apellido Nombre Salario
            partes = linea.split()
            if len(partes) >= 3:
                salario = int(partes[-1])  # El salario es el último campo
                
                # Filtrar por salario mínimo
                if salario >= salario_minimo:
                    conn_envio.send(linea)
                    print(f"P2 -> P3: {linea}")
        
        # Señal de fin
        conn_envio.send("FIN")
        print("P2: Finalizado")
    finally:
        conn_recepcion.close()
        conn_envio.close()


def proceso3_escribir_archivo(conn_recepcion):
    """
    Proceso 3: Recibe líneas del Proceso 2 y las escribe en empleados.txt
    con el formato: Apellido Nombre, Salario
    
    Parámetros:
    - conn_recepcion: conexión Pipe para recibir datos del Proceso 2
    
    Decisión: Solo necesita la conexión de entrada, el archivo de salida es fijo.
    """
    try:
        with open(ARCHIVO_EMPLEADOS, 'w', encoding='utf-8') as f:
            while True:
                linea = conn_recepcion.recv()
                
                if linea == "FIN":
                    break
                
                # Formato recibido: Apellido Nombre Salario
                partes = linea.split()
                if len(partes) >= 3:
                    apellido = partes[0]
                    nombre = partes[1]
                    salario = partes[2]
                    
                    # Escribir con formato: Apellido Nombre, Salario
                    linea_formateada = f"{apellido} {nombre}, {salario}"
                    f.write(linea_formateada + "\n")
                    print(f"P3: Escrito -> {linea_formateada}")
        
        print("P3: Finalizado")
    finally:
        conn_recepcion.close()


def main():
    """
    Main: Pide al usuario un departamento y un salario mínimo,
    luego lanza los procesos en orden con comunicación mediante Pipes.
    Espera a que todos los procesos terminen.
    """
    print("=" * 60)
    print("FILTRADO DE EMPLEADOS POR DEPARTAMENTO Y SALARIO")
    print("=" * 60)
    print("\nDepartamentos disponibles: Ventas, IT, RRHH")
    
    # Solicitar datos al usuario
    departamento = input("\nIntroduce el nombre del departamento: ")
    salario_minimo = int(input("Introduce el salario mínimo: "))
    
    print(f"\nFiltrando empleados del departamento '{departamento}' con salario >= {salario_minimo}")
    print("-" * 60)
    
    # Crear Pipes para comunicación entre procesos
    # Pipe 1: Proceso 1 -> Proceso 2
    conn1_recv, conn1_send = multiprocessing.Pipe(duplex=False)
    
    # Pipe 2: Proceso 2 -> Proceso 3
    conn2_recv, conn2_send = multiprocessing.Pipe(duplex=False)
    
    # Crear los procesos en el orden correcto
    # Proceso 3 primero (receptor final)
    p3 = multiprocessing.Process(
        target=proceso3_escribir_archivo,
        args=(conn2_recv,)
    )
    
    # Proceso 2 (intermediario)
    p2 = multiprocessing.Process(
        target=proceso2_filtrar_salario,
        args=(salario_minimo, conn1_recv, conn2_send)
    )
    
    # Proceso 1 (emisor inicial)
    p1 = multiprocessing.Process(
        target=proceso1_filtrar_departamento,
        args=(departamento, conn1_send)
    )
    
    # Iniciar todos los procesos
    # IMPORTANTE: Iniciar antes de cerrar los pipes locales, o fallará en Windows
    p3.start()
    p2.start()
    p1.start()

# Comentario:
    #Primero hago los start() (para que los hijos reciban sus conexiones abiertas).
    #Después hago los close() en el padre para que el padre no se quede con copias abiertas que impidan que los hijos detecten el fin de la comunicación.
    # Cerrar conexiones en el proceso principal que no usamos
    # Ahora sí podemos liberar los recursos locales
    conn1_send.close()
    conn1_recv.close()
    conn2_send.close()
    conn2_recv.close()
    
    # Esperar a que terminen todos los procesos
    p1.join()
    p2.join()
    p3.join()
    
    print("-" * 60)
    print("\nPROCESO COMPLETADO")
    print(f"Resultados guardados en: empleados.txt")
    
    # Mostrar contenido del archivo de salida
    print("\nContenido del archivo empleados.txt:")
    print("-" * 40)
    if os.path.exists(ARCHIVO_EMPLEADOS):
        with open(ARCHIVO_EMPLEADOS, 'r', encoding='utf-8') as f:
            contenido = f.read()
            if contenido:
                print(contenido)
            else:
                print("(No se encontraron empleados que cumplan los criterios)")


if __name__ == "__main__":
    main()

"""
El programa procesa líneas de texto una por una, en orden.
No necesito persistencia, ni acceso aleatorio, ni que varios procesos compitan por coger el dato.

"""