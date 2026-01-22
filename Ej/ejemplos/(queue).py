from multiprocessing import Process, Queue

def producer(objects):
    for i in range(10):
        objects.put(i)

def consumer(objects):
    while True:
        item = objects.get()
        if item is None:
            break
        print(item)

if __name__== '__main__':
    queue = Queue()
    p1 = Process(target=producer, args=(queue, ))
    p2 = Process(target=consumer, args=(queue, ))

    p1.start()
    p2.start()

    p1.join()
    queue.put(None)

    p2.join()

    print("Se han terminado ambos procesos")