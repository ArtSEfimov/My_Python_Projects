a = {1: '1'}

b = {1: ['11'], 3: ['3']}
c = {}

for k in c:
    a.setdefault(k, list()).extend(c[k])

print(len(a))
b = list(i for i in range(100_000_000))

a = list(1 for _ in range(100_000_000))

from time import time

start = time()
print(len(set(b)) == 1)
print(time() - start)

start = time()
print(all(
    map(
        lambda x: x == b[0], b
    )
))
print(time()-start)


start = time()
print(sum(b)//len(b) == b[0])
print(time() - start)