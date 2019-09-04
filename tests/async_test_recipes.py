from api.recipes_api import TastyApi


async def find_async_recipes(query='pancake'):
    import time
    start = time.time()

    api = TastyApi()
    async_gen = api.get_recipes_generator(query)
    results = [recipe.to_dict() async for recipe in async_gen ]
    print('Took results %s %.3f seconds' % (len(results), (time.time() - start)))


if __name__ == '__main__':
    import asyncio
    asyncio.run(find_async_recipes())
