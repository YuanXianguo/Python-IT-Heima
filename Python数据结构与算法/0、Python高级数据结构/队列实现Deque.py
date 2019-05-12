from collections import deque

q = deque(range(5))
q.append(5)
q.appendleft(6)
print(q)
print(q.pop())
print(q.popleft())
print(q.rotate(3))
print(q)
print(q.rotate(-1))
print(q)
