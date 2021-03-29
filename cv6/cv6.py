from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep
from random import randint


class Shared(object):
    def __init__(self, capacity):
        self.customers = 0
        self.capacity = capacity
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.barber_done = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.mutex = Mutex()


def barber(shared):
    while True:
        shared.customer.wait()
        shared.barber.signal()

        cut_hair()

        shared.customer_done.wait()
        shared.barber_done.signal()


def customer(shared, cid):
    shared.mutex.lock()
    print(f"zakaznik {cid}: prisiel som do holicstva, caka tu {shared.customers} ludi")
    if shared.customers == shared.capacity:
        shared.mutex.unlock()
        print(f"zakaznik {cid}: cakaren je plna, odchadzam")
        return
    shared.customers += 1
    shared.mutex.unlock()

    shared.customer.signal()
    shared.barber.wait()

    get_haircut(cid)

    shared.customer_done.signal()
    shared.barber_done.wait()

    shared.mutex.lock()
    shared.customers -= 1
    print(f"zakaznik {cid}: odchadzam ostrihany z holicstva, ostava tu {shared.customers} ludi")
    shared.mutex.unlock()



def cut_hair():
    print(f"holic: zacinam strihat vlasy")


def get_haircut(cid):
    print(f"zakaznik {cid}: zaciatok mojho strihu")
    sleep(0.5 + randint(0, 3))


def run():
    customers_capacity = 9

    shared = Shared(customers_capacity)
    cid = 0
    customer_threads = []
    barber_thread = Thread(barber, shared)

    while True:
        sleep(randint(0, 2))
        customer_threads.append(Thread(customer, shared, cid))
        cid += 1

    for c in customer_threads:
        c.join()
    barber_thread.join()


if __name__ == "__main__":
    run()
