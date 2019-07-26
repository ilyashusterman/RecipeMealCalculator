from models.dict_mixin import ToDictMixin
from models.exceptions import UpdateRecipeException


class Recipe(ToDictMixin):
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

    @classmethod
    def from_raw_dict(cls, kargs):
        return cls(**kargs)

    def update_from_raw_dict(self, kargs):
        missing_keys = {}
        for key, value in self.__dict__.items():
            if key not in self.EXCLUDED_UPDATE:
                try:
                    self.__dict__[key] = kargs[key]
                except KeyError as e:
                    missing_keys[key] = 'missing'
        if missing_keys:
            raise UpdateRecipeException(missing_keys, kargs.keys())
