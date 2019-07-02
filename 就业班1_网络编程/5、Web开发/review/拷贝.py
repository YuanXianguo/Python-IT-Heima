import copy


a = [1, 2]
b = [3, 4]
c = [a, b]
d = a
h = copy.copy(a)
e = c
f = copy.copy(c)
g = copy.deepcopy(c)
a.append(5)

print(id(a), id(d), id(h))
print(a, d, h)
print(id(c), id(e), id(f), id(g))
print(c, e, f, g)


a = 1
b = copy.copy(a)
print(id(a), id(b))
