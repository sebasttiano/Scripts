"""
Asyncio, async/await. Example: how to download some data (10 images) in async mode and  time it.
"""
import asyncio
from time import time
import aiohttp # pip install aiohttp  - библиотека работы asyncio с http (tcp и udp есть в коробке)


def write_image(data): # Синхронная функция, так как asyncio не работает с файлами асинхронно. Это возможно начиная с
    # распараллеливания потоков с помощью других библиотек.
    filename = f'file-{int(time() * 1000)}.jpeg'
    with open(filename, 'wb') as file:
        file.write(data)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()     # в асинхронном режиме работы методы должны вызываться с await
        write_image(data)  # Внутри асинхронных функций можно использовать синхронные функции, но не наоборот.
        # но смешивать синх. и асинх. коды плохая идея, т.к. может быть блокировка со стороны синх. Это просто пример.
        # но этот пример все равно быстрее работает, если бы все было синх.


async def main2():
    url = 'https://loremflickr.com/320/240'
    tasks = []

    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)

if __name__ == '__main__':
    t0 = time()
    asyncio.run(main2())
    print(time() - t0)


# The result of this programm about 0.5 - 1.5 sec in running state.