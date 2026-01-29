from multiprocessing import Process, Pipe


def process1(conn) :
    conn.send("(extremo izq)(Hola extremo derecho)")
    conn.close()

def process2(conn):
    mensaje = conn.recv()
    print("(Extremo dercho+)Mensaje recibido:", mensaje)
    conn. close()

if __name__ == '__main__':
    left, right = Pipe()
    p1 = Process(target=process1, args=(left, ))
    p2 = Process(target=process2, args=(right,))

    p1.start()
    p2.start()