import asyncio
import argparse
import json
import logging


from api.recipes_api import TastyApi

TASTY_API = TastyApi()


async def find_async_recipes(query='pancake', find_func=TASTY_API.find_recipes_async):
    import time
    start = time.time()
    async_gen = find_func(query)
    results = [recipe.to_dict() async for recipe in async_gen]
    print('Results=\n%s' % json.dumps(results, indent=2))
    total_time = time.time() - start
    print('Took results %s %.3f seconds' % (len(results), total_time))


def find_meals(query):
    asyncio.run(find_async_recipes(query))


def find_tasty_meals(query):
    asyncio.run(find_async_recipes(query, TASTY_API.find_raw_recipes_async))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Find Recipes with calories calculations.')
    parser.add_argument('--find', help='find meals by query')
    parser.add_argument('--find-raw', help='find tasty raw meals by query')
    args = parser.parse_args()
    if args.find:
        find_meals(args.find)
    elif args.find_raw:
        find_tasty_meals(args.find_raw)
