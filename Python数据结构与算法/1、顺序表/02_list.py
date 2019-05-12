from timeit import Timer

N = 10000


def t1():
    li = []
    for i in range(N):
        li.append(i)


def t2():
    li = []
    for i in range(N):
        li += [i]


def t3():
    li = [i for i in range(N)]


def t4():
    li = list(range(N))


timer1 = Timer("t1()", "from __main__ import t1")
print(timer1.timeit(1000))

timer2 = Timer("t2()", "from __main__ import t2")
print(timer2.timeit(1000))

timer3 = Timer("t3()", "from __main__ import t3")
print(timer3.timeit(1000))

timer4 = Timer("t4()", "from __main__ import t4")
print(timer4.timeit(1000))
