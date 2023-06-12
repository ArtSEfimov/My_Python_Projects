a = {1: [3, 4, 5, 6], 2: []}
b = {2: [], 1: [3, 4, 5, 6], }

c = {key: b[key].copy() for key in b}
print(c)
#
c[2].append('sdfsdfs')
#
print(b)
