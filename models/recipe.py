from models.dict_mixin import ToDictMixin
from models.dict_mixin import FromDictMixin
from models.exceptions import UpdateRecipeException


class Recipe(ToDictMixin, FromDictMixin):
    """
    Recipe Model persist and looku
    """
    EXCLUDED_UPDATE = ['url']

    def __init__(self, **kargs):
        self.name = kargs.pop('name', 'UNDEFINED_RECIPE_NAME')
        self.url = kargs.pop('url', None)
        self.description = kargs.pop('description', None)
        self.ingredients = kargs.pop('ingredients', [])
        self.category = kargs.pop('category', None)
        self.cuisine = kargs.pop('cuisine', None)
        self.date_published = kargs.pop('date_published', None)
        self.nutrition_facts = kargs.pop('nutrition_facts', None)

    def update_from_raw_dict(self, kargs):
        missing_keys = {}
        for key, value in self.__dict__.items():
            if key not in self.EXCLUDED_UPDATE:
                try:
                    self.__dict__[key] = kargs[key]
                except KeyError:
                    missing_keys[key] = 'missing'
        if missing_keys:
            raise UpdateRecipeException(missing_keys, kargs.keys())


class NutritionFacts(ToDictMixin, FromDictMixin):

    def __init__(self, **kargs):
        self.calories = kargs.pop('calories', None)
        self.carbohydrate = kargs.pop('carbohydrate', None)
        self.fat = kargs.pop('fat', None)
        self.fiber = kargs.pop('fiber', None)
        self.protein = kargs.pop('protein', None)
        self.sugar = kargs.pop('sugar', None)


class RawRecipe(Recipe):

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.raw_html = kargs.pop('raw_html')
