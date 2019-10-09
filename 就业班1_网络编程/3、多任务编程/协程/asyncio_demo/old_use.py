import asyncio


@asyncio.coroutine
def main():
    print('waiting for chain1')
    result1 = yield from chain1()
    print('waiting for chain2')
    result2 = yield from chain2(result1)
    return (result1, result2)


@asyncio.coroutine
def chain1():
    print('in chain1')
    return 'result1'


@asyncio.coroutine
def chain2(arg):
    print('in chain2')
    return 'Derived from {}'.format(arg)


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    try:
        return_value = event_loop.run_until_complete(main())
        print('return value: {}'.format(return_value))
    finally:
        event_loop.close()
