from collections import defaultdict
"""defaultdict这个类型除了在处理不存在的键的操作之外与普通的字典完全相同。
当查找一个不存在的键操作发生时，它的default_factory会被调用，提供一个默认的值，
并且将这对键值存储下来。其他的参数同普通的字典方法dict()一致，
一个defaultdict的实例同内建dict一样拥有同样地操作。"""


s = "the quick brown fox jumps over the lazy dog"
words = s.split()

# 查找不存在的键操作时，将其值定义为空列表
location = defaultdict(list)

"""在同时需要用到index和value值的时候可以用到enumerate，
参数为可遍历的变量，如字符串，列表等，返回enumerate类"""
for index, word in enumerate(words):
    location[word].append(index)


if __name__ == '__main__':
    print(location)
    print(location['1'])
