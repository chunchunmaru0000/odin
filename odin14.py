import random
import threading
import time

arrayed = []
numberOfThreads = 7


def calculate_array(immenseness, number):
    global arrayed
    print(f'thread {number} born')
    arrayed.append(sum([random.randint(-1000, 1000) for _ in range(immenseness)]))
    print(f'thread {number} passed out, time now is {time.time() - toki}')


toki = time.time()

threads = [threading.Thread(target=calculate_array, args=(10000000 // numberOfThreads, _)) for _ in range(numberOfThreads)]
[threads[_].start() for _ in range(numberOfThreads)]
[threads[_].join() for _ in range(numberOfThreads)]

print(f'################################\nsum = {sum(arrayed)}\n終わりだ\ntime {time.time() - toki}')
