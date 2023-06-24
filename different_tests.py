# a = (1, 2)
# a = ((1, 2),)
a=(1,)


try:
    c, = a
    print('hello try')
except ValueError:
    c = a
    print('hello except')
else:
    if type(c) == int:
        c = c,
        print('hello else')
print(c)
