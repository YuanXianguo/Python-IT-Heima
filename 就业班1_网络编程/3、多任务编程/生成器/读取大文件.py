def get_lines():
    l = []
    with open("file.txt", "r") as f:
        for line in f:
            l.append(line)
    return l


def get_lines_iter():
    l = []
    with open("file.txt", "r") as f:
        data = f.readlines(50)
        l.append(data)
        yield l


def get_lines_iter2():
    with open("file.txt", "r") as f:
        while True:
            data = f.readlines(50)
            if data:
                yield data
            else:
                return


if __name__ == '__main__':
    for line in get_lines_iter2():
        print(line)
