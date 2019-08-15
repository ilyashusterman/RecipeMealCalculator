from api.recipes_api import TastyApi


async def test_async_recipes():
    import time
    start = time.time()

    api = TastyApi()
    async_gen = api.get_recipes_generator('pancake')
    results = [recipe.to_dict() async for recipe in async_gen ]
    print('Took results %s %.3f seconds' % (len(results), (time.time() - start)))


if __name__ == '__main__':
    import asyncio
    asyncio.run(test_async_recipes())