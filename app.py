
import asyncio
import datetime
import numpy as np
import pickle
from primesieve.numpy import primes
from BTrees.OOBTree import OOBTree

nhilos = 10
nelements = 10000
bash_size = 100
max_limit = 1000

bucles = int(nelements / bash_size)
_primes = primes(max_limit)
_fibonaci = []

def fib_iterative(n):
    a, b = 0, 1
    while n > b:
        a, b = b, a + b
        n -= 1
        _fibonaci.append(b)
    return a

fib_iterative(max_limit)

_dict = {}
for x in _primes:
    _dict[x] = True

t = OOBTree()
t.update(_dict)

_dict = {}
for x in _fibonaci:
    _dict[x] = True

h = OOBTree()
h.update(_dict)

primos = []
fibonacis = []


@asyncio.coroutine
def find(task):
    yield from asyncio.sleep(2)
    calculate()
    
def calculate():
    values = np.random.randint(nelements, size=(max_limit)) #(1000)
    for x in values:
        if t.has_key(x) > 0:
            primos.append(x)
        if h.has_key(x) > 0:
            fibonacis.append(x)
 
loop = asyncio.get_event_loop()
tasks = []
for x in range(0, bucles):
    if x % nhilos == 0:
        tasks.append(asyncio.ensure_future(find(x)))
        loop.run_until_complete(asyncio.wait(tasks))
        tasks = []
        print("Ciclo: {} de {}".format(x, bucles))


loop.close()

primos.sort()
fibonacis.sort()

with open('primos.dump', 'wb') as fp:
    pickle.dump(primos, fp)

with open('fibonacis.dump', 'wb') as fp:
    pickle.dump(fibonacis, fp)

print("los numeros primos estan en: primos.dump")
print("los numeros fibonacis estan en: fibonacis.dump")