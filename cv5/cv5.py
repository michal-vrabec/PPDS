from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print


class Shared(object):
    def __init__(self):
        self.servings = 0
        self.mutex = Mutex()
        self.emptyPot = Semaphore(0)
        self.fullPot = Semaphore(0)


def cook(shared, capacity):
    while True:
        shared.emptyPot.wait()
        put_servings_in_pot(shared, capacity)
        shared.fullPot.signal()


def get_serving_from_pot(shared, sid):
    shared.servings -= 1
    print(f"divoch {sid}: zostatok porcii v hrnci je {shared.servings}")


def eat(sid):
    print(f"divoch {sid}: hodujem")
    sleep(0.2 + randint(0, 3) / 10)


def put_servings_in_pot(shared, M):
    print(f"kuchar: varim")
    sleep(0.5 + randint(0, 3) / 10)
    shared.servings += M


def savage(shared, sid):
    while True:
        shared.mutex.lock()
        print(f"divoch {sid}: pocet porcii v hrnci je {shared.servings}")
        if shared.servings == 0:
            print(f"divoch {sid}: budim kuchara")
            shared.emptyPot.signal()
            shared.fullPot.wait()
        get_serving_from_pot(shared, sid)
        shared.mutex.unlock()
        eat(sid)


def run():
    pot_capacity = 13
    savage_count = 15

    shared = Shared()
    savages = [Thread(savage, shared, sid) for sid in range(savage_count)]
    savages.append(Thread(cook, shared, pot_capacity))

    for s in savages:
        s.join()


if __name__ == "__main__":
    run()
