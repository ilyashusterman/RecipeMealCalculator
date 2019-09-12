import logging

GRAM_PORTIONS = {
    'cup': 220
}


class RecipeConverterMixin:

    @classmethod
    def get_percentages(cls, recipe):
        if recipe.ingredients:
            recipe.ingredients = [
                cls.convert_ingredient(ingredient)
                for ingredient in recipe.ingredients
            ]
        return recipe.to_dict()

    @classmethod
    def convert_ingredient(cls, ingredient: str):
        for portion, value in GRAM_PORTIONS.items():
            if portion in ingredient:
                amount = ingredient.split(portion)[0]
                try:
                    new_amount = '%.1f ' % (float(amount) * value)
                except ValueError as e:
                    logging.error(e)
                    return ingredient
                else:
                    return ingredient.replace(portion, 'gram').replace(amount, new_amount)
        return ingredient
