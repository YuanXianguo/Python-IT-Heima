import time

s1 = time.perf_counter()
for i in range(501):
    for j in range(i+1):
        k = 1000 - i - j
        if i ** 2 + j ** 2 == k ** 2:
            print(i, j, k)
s2 = time.perf_counter()
for i in range(1000):
    for j in range(1000):
        k = 1000 - i - j
        if i ** 2 + j ** 2 == k ** 2:
            print(i, j, k)
s3 = time.perf_counter()
for i in range(1000):
    for j in range(1000):
        for k in range(1000):
            if i + j + k == 1000 and i ** 2 + j ** 2 == k ** 2:
                print(i, j, k)
s4 = time.perf_counter()

print(s2-s1, s3-s2, s4-s3)
