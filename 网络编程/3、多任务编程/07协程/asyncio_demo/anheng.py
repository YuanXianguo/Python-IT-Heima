import asyncio


class B(object):
    def __init__(self):
        self._value = 0

    def value(self):
        return self._value


class Counter1(B):
    async def add(self):
        value = self._value + 1
        asyncio.sleep(1)
        self._value = value


class Counter2(B):
    async def add(self):
        self._value += 1
        asyncio.sleep(1)


def main():
    c1 = Counter1()
    res1 = asyncio.gather(*[c1.add() for i in range(100)])

    c2 = Counter2()
    res2 = asyncio.gather(*[c2.add() for i in range(100)])

    loop = asyncio.get_event_loop()
    all = asyncio.gather(res1, res2)
    loop.run_until_complete(all)
    loop.close()
    print(c1.value(), c2.value())


if __name__ == '__main__':
    main()
