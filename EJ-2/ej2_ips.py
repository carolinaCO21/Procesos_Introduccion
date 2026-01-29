import multiprocessing
import random
import time

# 2. En este ejercicio vamos a lanzar varios procesos, cuyas entradas y
#  salidas están enlazadas. Para ello tendremos tres procesos distintos:
# Proceso 1: Va a generar 10 direcciones IP de forma aleatoria y se las 
# enviará al Proceso 2.
# Proceso 2: Va a leer las direcciones IP que recibe del Proceso 1 y
#  va a enviar al Proceso 3 únicamente aquellas que pertenezcan a las
#  clases A, B o C.
# Proceso 3: Va a leer las direcciones IP procedentes del Proceso 2
#  (no se sabe qué número llegarán) y va a imprimir por consola la dirección IP
#  y a continuación la clase a la que pertenece.Lanza los tres procesos en orden.

def generar_ips(conn_salida):
    """Proceso 1: Genera 10 IPs aleatorias y las envía."""
    print("P1: Generando IPs...")
    for _ in range(10):
        ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        conn_salida.send(ip)
    conn_salida.send(None) # Señal de fin
    conn_salida.close()

def filtrar_ips(conn_entrada, conn_salida):
    """Proceso 2: Recibe IPs, clasifica y envía las válidas (A, B, C)."""
    while True:
        ip = conn_entrada.recv()
        if ip is None:
            break
        
        primer_octeto = int(ip.split('.')[0])
        clase = None
        
        if 0 <= primer_octeto <= 127:
            clase = 'A'
        elif 128 <= primer_octeto <= 191:
            clase = 'B'
        elif 192 <= primer_octeto <= 223:
            clase = 'C'
        
        if clase:
            conn_salida.send((ip, clase))
    
    conn_salida.send(None) # Señal de fin
    conn_entrada.close()
    conn_salida.close()

def imprimir_ips(conn_entrada):
    """Proceso 3: Imprime la IP y su clase."""
    print("P3: Resultados recibidos:")
    while True:
        datos = conn_entrada.recv()
        if datos is None:
            break
        ip, clase = datos
        print(f"IP: {ip} -> Clase {clase}")
    conn_entrada.close()

if __name__ == "__main__":
    # Pipes para conectar P1 -> P2 y P2 -> P3
    # Pipe() devuelve (conn1, conn2) donde conn1 es para recibir y conn2 para enviar (o bidireccional)
    # Aquí usaremos: P1 escribe en p1_w, P2 lee de p1_r
    p1_r, p1_w = multiprocessing.Pipe()
    # P2 escribe en p2_w, P3 lee de p2_r
    p2_r, p2_w = multiprocessing.Pipe()

    proceso1 = multiprocessing.Process(target=generar_ips, args=(p1_w,))
    proceso2 = multiprocessing.Process(target=filtrar_ips, args=(p1_r, p2_w))
    proceso3 = multiprocessing.Process(target=imprimir_ips, args=(p2_r,))

    proceso1.start()
    proceso2.start()
    proceso3.start()

    proceso1.join()
    proceso2.join()
    proceso3.join()
