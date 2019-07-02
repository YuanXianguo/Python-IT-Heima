from collections import Counter

li = ["Dog", "Cat", "Mouse", 42, "Dog", 42, "Cat", "Dog"]
count = Counter(li)
print(type(count))
print(count)
print(count.keys(), count.values())
print(count.most_common(2))  # 出现次数最多的前两个

