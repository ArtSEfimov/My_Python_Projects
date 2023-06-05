def func(a):
    if a > 5:
        return 3, 4
    if a < 3:
        return None
    if a == 4:
        return 1, 2, 3


res = func(4)

print(res)
