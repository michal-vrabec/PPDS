from fei.ppds import Mutex, Semaphore, Thread
from random import randint
from time import sleep
import pandas as pd


class Shared:
    def __init__(self, buffer_size):
        self.empty = Semaphore(buffer_size)
        self.full = Semaphore(0)
        self.mutex = Mutex()
        self.buffer = []

        self.items_produced = 0
        self.items_consumed = 0
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
        shared_object.items_consumed += 1

        shared_object.mutex.unlock()
        shared_object.empty.signal()

        sleep(time_consumption)


def timer(shared_object, producers_count, consumers_count, combination_id):
    global repetition_produced
    global repetition_consumed
    sleep(60)
    shared_object.mutex.lock()
    shared_object.stop = True

    repetition_produced[combination_id].append(shared_object.items_produced)
    repetition_consumed[combination_id].append(shared_object.items_consumed)

    shared_object.full.signal(consumers_count)
    shared_object.empty.signal(producers_count)
    shared_object.mutex.unlock()


cycle_max = 110
producers = [None] * cycle_max
consumers = [None] * cycle_max
shared = [None] * cycle_max
timer_threads = [None] * cycle_max
repetition_produced = [[] for _ in range(cycle_max)]
repetition_consumed = [[] for _ in range(cycle_max)]
df = pd.DataFrame(columns=['producers', 'consumers', 'production_time',
                           'consumption_time', 'capacity', 'produced', 'consumed'])

for i in range(cycle_max):
    number_of_producers = randint(1, 15)
    number_of_consumers = randint(1, 15)
    production_time = randint(1, 15)
    consumption_time = randint(1, 15)
    capacity = randint(1, 15)

    df.loc[i] = [number_of_producers, number_of_consumers, production_time, consumption_time,
                 capacity, 0, 0]


for _ in range(10):
    for i in range(cycle_max):
        number_of_producers = df.at[i, 'producers']
        number_of_consumers = df.at[i, 'consumers']
        production_time = df.at[i, 'production_time']
        consumption_time = df.at[i, 'consumption_time']
        capacity = df.at[i, 'capacity']

        producers[i] = [None] * number_of_producers
        consumers[i] = [None] * number_of_consumers
        shared[i] = Shared(capacity)

        for j in range(number_of_producers):
            producers[i][j] = Thread(produce, shared[i], production_time)

        for j in range(number_of_consumers):
            consumers[i][j] = Thread(consume, shared[i], consumption_time)

        timer_threads[i] = Thread(timer, shared[i], number_of_producers, number_of_consumers, i)
        df.loc[i] = [number_of_producers, number_of_consumers, production_time, consumption_time,
                     capacity, 0, 0]

    for timer_thread in timer_threads:
        timer_thread.join()

    for producer_i in producers:
        for producer in producer_i:
            producer.join()

    for consumer_i in consumers:
        for consumer in consumer_i:
            producer.join()

for i in range(cycle_max):
    df.at[i, 'produced'] = round(sum(repetition_produced[i]) / len(repetition_produced[i]), 2)
    df.at[i, 'consumed'] = round(sum(repetition_consumed[i]) / len(repetition_consumed[i]), 2)

df.to_csv('data.csv', index=False)
