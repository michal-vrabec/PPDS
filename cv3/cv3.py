from fei.ppds import Mutex, Semaphore, Thread
from time import sleep


class Shared:
    def __init__(self, buffer_size):
        self.empty = Semaphore(buffer_size)
        self.full = Semaphore(0)
        self.mutex = Mutex()
        self.buffer = []


def produce(shared_object, time):
    while True:
        sleep(time)

        shared_object.empty.wait()
        shared_object.mutex.lock()

        shared_object.buffer.append(1)
        print('produced')
        shared_object.mutex.unlock()
        shared_object.full.signal()


def consume(shared_object, time):
    while True:
        shared_object.full.wait()
        shared_object.mutex.lock()

        shared_object.buffer.pop(0)
        print('consumed')
        shared_object.mutex.unlock()
        shared_object.empty.signal()

        sleep(time)


number_of_producers = 5
number_of_consumers = 5
production_time = 2
consumption_time = 2
capacity = 10

producers = [None] * number_of_producers
consumers = [None] * number_of_consumers
shared = Shared(capacity)


for i in range(number_of_producers):
    producers[i] = Thread(produce, shared, production_time)

for i in range(number_of_consumers):
    consumers[i] = Thread(consume, shared, consumption_time)

for producer in producers:
    producer.join()

for consumer in consumers:
    consumer.join()

