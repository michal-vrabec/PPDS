from fei.ppds import *


class Shared:
    def __init__(self, threads_n):
        self.fibonacci_sequence = [0, 1] + [0] * threads_n
        self.semaphores = [Semaphore(0)] * (threads_n + 2)
        self.semaphores[0].signal(1)
        self.semaphores[1].signal(2)

        self.events = [Event()] * (threads_n + 2)
        self.events[0].signal()
        self.events[1].signal()

    def count_fibonacci_sequence_semaphores(self, i):
        self.semaphores[i].wait()
        self.semaphores[i + 1].wait()
        self.fibonacci_sequence[i + 2] = self.fibonacci_sequence[i] + self.fibonacci_sequence[i + 1]
        self.semaphores[i + 2].signal(2)

    def count_fibonacci_sequence_events(self, i):
        self.events[i].wait()
        self.events[i + 1].wait()
        self.fibonacci_sequence[i + 2] = self.fibonacci_sequence[i] + self.fibonacci_sequence[i + 1]
        self.events[i + 2].signal()


def count_fibonacci_sequence(shared_object, i):
    # shared_object.count_fibonacci_sequence_semaphores(i)
    shared_object.count_fibonacci_sequence_events(i)


number_of_threads = 20
shared = Shared(number_of_threads)

threads = [None] * number_of_threads
for j, thread in enumerate(threads):
    threads[j] = Thread(count_fibonacci_sequence, shared, j)

for j, thread in enumerate(threads):
    threads[j].join

print(shared.fibonacci_sequence)
