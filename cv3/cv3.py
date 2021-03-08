from fei.ppds import Mutex, Semaphore, Thread
from random import randint
from time import sleep


class Shared:
    def __init__(self, buffer_size):
        self.empty = Semaphore(buffer_size)
        self.full = Semaphore(0)
        self.mutex = Mutex()
        self.buffer = []

        self.items_produced = 0
        self.stop = False


def produce(shared_object, time_production):
    while True:
        sleep(time_production)

        shared_object.empty.wait()
        shared_object.mutex.lock()
        if shared_object.stop:
            shared_object.mutex.unlock()
            break

        shared_object.buffer.append(1)
        shared_object.items_produced += 1

        shared_object.mutex.unlock()
        shared_object.full.signal()


def consume(shared_object, time_consumption):
    while True:
        shared_object.full.wait()
        shared_object.mutex.lock()
        if shared_object.stop:
            shared_object.mutex.unlock()
            break

        shared_object.buffer.pop(0)

        shared_object.mutex.unlock()
        shared_object.empty.signal()

        sleep(time_consumption)


def timer(shared_object, producers_count, consumers_count):
    sleep(60)
    shared_object.mutex.lock()
    shared_object.stop = True
    shared_object.full.signal(consumers_count)
    shared_object.empty.signal(producers_count)
    shared_object.mutex.unlock()


for i in range(120):
    number_of_producers = randint(1, 10)
    number_of_consumers = randint(1, 10)
    production_time = randint(1, 10)
    consumption_time = randint(1, 10)
    capacity = randint(1, 10)

    producers = [None] * number_of_producers
    consumers = [None] * number_of_consumers
    shared = Shared(capacity)

    for j in range(number_of_producers):
        producers[j] = Thread(produce, shared, production_time)

    for j in range(number_of_consumers):
        consumers[j] = Thread(consume, shared, consumption_time)

    timer_thread = Thread(timer, shared, number_of_producers, number_of_consumers)

    timer_thread.join()
    for producer in producers:
        producer.join()

    for consumer in consumers:
        consumer.join()

    print('finished 1')

