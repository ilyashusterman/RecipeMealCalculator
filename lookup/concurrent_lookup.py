from concurrent.futures import ThreadPoolExecutor


class ConcurrentLookup:

    def __init__(self, recipes=None, load_recipe_func=None):
        self.recipes = recipes
        self.load_recipe_func = load_recipe_func

    @classmethod
    def from_lookup_recipes(cls, recipes):
        return cls(recipes=recipes)

    def load_recipes(self):
        pool = ThreadPoolExecutor()
        self.recipes = pool.map(self.load_recipe_func, self.recipes)
        return self.recipes
