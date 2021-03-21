from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print


class Shared(object):
    def __init__(self, capacity):
        self.servings = 0
        self.savages_mutex = Mutex()
        self.cooks_mutex = Mutex()
        self.emptyPot = Semaphore(0)
        self.fullPot = Semaphore(0)
        self.capacity = capacity


def cook(shared, sid):
    while True:
        shared.emptyPot.wait()

        cook_serving(sid)

        shared.cooks_mutex.lock()
        print(f"kuchar {sid}: pocet porcii v hrnci je {shared.servings}")
        add_serving_to_pot(shared, sid)
        if shared.servings == shared.capacity:
            print(f"kuchar {sid}: hrniec naplneny")
            shared.fullPot.signal()
        shared.cooks_mutex.unlock()


def savage(shared, sid):
    while True:
        shared.savages_mutex.lock()
        print(f"divoch {sid}: pocet porcii v hrnci je {shared.servings}")
        if shared.servings == 0:
            print(f"divoch {sid}: budim kucharov")
            shared.emptyPot.signal(shared.capacity)
            shared.fullPot.wait()
        get_serving_from_pot(shared, sid)
        shared.savages_mutex.unlock()
        eat(sid)


def get_serving_from_pot(shared, sid):
    shared.servings -= 1
    print(f"divoch {sid}: zobral som porciu, zostatok porcii v hrnci je {shared.servings}")


def add_serving_to_pot(shared, sid):
    shared.servings += 1
    print(f"kuchar {sid}: pridal som porciu, v hrnci je {shared.servings} porcii")


def eat(sid):
    print(f"divoch {sid}: hodujem")
    sleep(0.2 + randint(0, 3) / 10)


def cook_serving(sid):
    print(f"kuchar {sid}: varim")
    sleep(0.5 + randint(0, 3) / 10)


def run():
    pot_capacity = 13
    savage_count = 15
    cook_count = 7

    shared = Shared(pot_capacity)
    savages = [Thread(savage, shared, sid) for sid in range(savage_count)]

    cooks = [Thread(cook, shared, sid) for sid in range(cook_count)]

    for s in savages:
        s.join()
    for c in cooks:
        c.join()


if __name__ == "__main__":
    run()
