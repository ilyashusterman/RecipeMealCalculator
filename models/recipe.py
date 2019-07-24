from models.dict_mixin import ToDictMixin


class Recipe(ToDictMixin):
    """
    Recipe Model
    """
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

