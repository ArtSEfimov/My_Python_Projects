a={1:'1', 2:'2'}

b = a.setdefault(3,tuple())
print(b)
print(a)