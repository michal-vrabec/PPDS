from fei.ppds import *
import numpy as np


class Shared:
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()


# def counter(shared):
# # riesenie z cvicenia - pole sa inkrementuje este predtym ako sa zavrie lock, takze ku danemu indexu
# # pola mozu pristupit obe vlakna naraz a inkrementovat ho
#     while True:
#         if shared.counter >= shared.end:
#             break
#         shared.array[shared.counter] += 1
#         shared.mutex.lock()
#         shared.counter += 1
#         shared.mutex.unlock()


# def counter(shared):
# # nasledujuce riesenie funguje, ale nie je optimalne, kedze je shared objekt zamknuty pocas
# # vsetkych prikazov v cykle
#     while True:
#         shared.mutex.lock()
#         if shared.counter >= shared.end:
#             shared.mutex.unlock()
#             break
#         shared.array[shared.counter] += 1
#         shared.counter += 1
#         shared.mutex.unlock()


def counter(shared):
    # optimalnejsie riesenie ako predtym, kedze pocas inkrementovania nie je objekt uzamknuty
    # index si ulozime do lokalnej premennej, ktora nemoze byt zmenena z druheho threadu
    while True:
        shared.mutex.lock()
        index_temp = shared.counter
        shared.counter += 1
        shared.mutex.unlock()
        if index_temp >= shared.end:
            break
        shared.array[index_temp] += 1


sh = Shared(1_000_000)

t1 = Thread(counter, sh)
t2 = Thread(counter, sh)

t1.join()
t2.join()
histogram = np.histogram(sh.array, bins=[0, 1, 2, 3])
print(histogram)
