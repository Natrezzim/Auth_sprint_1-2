import asyncio

import aioredis

from tests.functional.settings import REDIS_HOST, REDIS_PORT

red = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}', encoding="utf-8", decode_responses=True)


async def redis():
    ping = False

    while not ping:
        print('Connecting to redis...')
        await asyncio.sleep(2)
        ping = await red.ping()

    await red.close()
    print('Connected to redis!')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(redis())
    loop.close()
