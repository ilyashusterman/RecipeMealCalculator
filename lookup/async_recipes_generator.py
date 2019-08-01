from collections.abc import AsyncGenerator
from typing import Type, Optional, Any

from lookup.concurrent_lookup import ConcurrentLookup


class AsyncRecipesGenerator(AsyncGenerator):
    """
    Generate recipes by lookup method for query then loads recipes asynchronously
    """
    def __init__(self, query, lookup_recipe_func, load_found_recipe_func):
        self.query = query
        self.lookup_recipe_func = lookup_recipe_func
        self.load_found_recipe_func = load_found_recipe_func
        self.recipes = None
        super().__init__()

    async def __anext__(self):
        for recipe in self.recipes:
            return recipe
        else:
            raise StopAsyncIteration

    def asend(self, value):
        pass

    def athrow(self, typ: Type[BaseException],
               val: Optional[BaseException] = ..., tb: Any = ...):
        pass

    def aclose(self):
        pass

    def __aiter__(self):
        recipes_generator = self.lookup_recipe_func(self.query)
        self.recipes = ConcurrentLookup(recipes_generator, self.load_found_recipe_func).load_recipes()
        return self

