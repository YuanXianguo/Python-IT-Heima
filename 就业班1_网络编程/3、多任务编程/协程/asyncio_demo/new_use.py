import asyncio


async def main():
    """async 关键字替代了 @asyncio.coroutine 这个装饰器, await 替代了 yield from。
    至此, 协程成为了一种新的语法, 而不再是一种生成器类型。"""
    print("waiting for chain1")
    res1 = await chain1()
    print("waiting for chain2")
    res2 = await chain2(res1)
    return res1, res2


async def chain1():
    print("chain1")
    return "res1"


async def chain2(arg):
    print("chain2")
    return "Derived from {}".format(arg)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        res = loop.run_until_complete(main())
        print("res value: {}".format(res))
    finally:
        loop.close()
