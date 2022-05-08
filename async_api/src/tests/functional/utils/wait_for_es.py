import asyncio

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import ELASTIC_HOST, ELASTIC_PORT

es = AsyncElasticsearch([f'{ELASTIC_HOST}: {ELASTIC_PORT}'], verify_certs=False)


async def elastic():
    ping = False

    while not ping:
        print('Connecting to elastic...')
        await asyncio.sleep(2)
        ping = await es.ping()

    await es.close()
    print('Connected to elastic!')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(elastic())
    loop.stop()
    loop.close()
