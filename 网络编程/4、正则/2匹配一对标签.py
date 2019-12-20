import re


def match_tag(t):
    # 普通匹配
    res = re.match(r"<\w*>.*</\w*>", t)
    if res:
        print(1, res.group())

    # 分组匹配
    res = re.match(r"<(\w*)>.*</\1>", t)
    if res:
        print(2, res.group())

    # 分组匹配2对
    res = re.match(r"<(\w*)><(\w*)>.*</\2></\1>", t)
    if res:
        print(3, res.group())

    # 别名匹配
    res = re.match(r"<(?P<p1>\w*)><(?P<p2>\w*)>.*</(?P=p2)></(?P=p1)>", t)
    if res:
        print(4, res.group())


if __name__ == '__main__':
    t = "<h1>add</h1>"
    match_tag(t)
    print()

    t = "<h1>add</h2>"
    match_tag(t)
    print()

    t = "<body><h1>add</h1></body>"
    match_tag(t)
