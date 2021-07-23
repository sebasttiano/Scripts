"""
Asyncio, async/await
"""

# План:
# 1. Asyncio фреймворк для создания событийных циклов
# 2. Пример простой асинхронной программы времен Python 3.4
# 3. Синтаксис Async/await на замену @asyncio.gen_init и yield from
# 4. Пример асинхронного скачивания файлов
import asyncio
from time import time

# ------------------- Этот код был до версии Python 3.5 ---------------------#
# @asyncio.coroutine # Превращает функцию в корутину, генератор.
# def print_nums():
#     num = 1
#     while True:
#         print(num)
#         num += 1
#         yield from asyncio.sleep(0.1) # Аналог sleep для генераторов, чтобы не отдавайть контроль исполнения в event loop
#
# @asyncio.coroutine
# def print_time():
#     count = 0
#     while True:
#         if count % 3 == 0:
#             print(f'{count} seconds have passed')
#         count += 1
#         yield from asyncio.sleep(1)
#
#
# @asyncio.coroutine
# def main():
#     task1 = asyncio.ensure_future(print_nums())
#     task2 = asyncio.ensure_future(print_time())
#
#     yield from asyncio.gather(task1, task2)


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     loop.close()

# ----------------------- Этот код после Python 3.5 включительно --------------
async def print_nums(): # async вместо декоратора @asyncio.coroutine. Превращает функцию в корутину, генератор.
    num = 1
    while True:
        print(num)
        num += 1
        await asyncio.sleep(0.1) # Аналог sleep для генераторов, чтобы не отдавайть контроль исполнения в event loop
        # await c Python3.5 вместо yield from


async def print_time():
    count = 0
    while True:
        if count % 3 == 0:
            print(f'{count} seconds have passed')
        count += 1
        await asyncio.sleep(1)


async def main():
    task1 = asyncio.create_task(print_nums()) # c версии 3.6 create_task вместо ensure_future
    task2 = asyncio.create_task(print_time())

    await asyncio.gather(task1, task2)

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
    # с версии Python3.7 все вышестоящее заменяется методом run()
    asyncio.run(main())

