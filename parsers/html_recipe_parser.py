import json
from bs4 import BeautifulSoup

from models.recipe import Recipe


class HtmlRecipeParserMixin:
    """
    RecipeParser converts raw string to Recipe class
    """
    @classmethod
    def html_to_recipe(cls, raw_html):
        """
        parse Recipe from html string
        :param raw_html: str
        :return: Recipe
        """
        raw_soup = BeautifulSoup(raw_html, 'html.parser')
        recipe_element = cls.recipe_lookup(raw_soup)
        recipe_json = json.loads(recipe_element.text)
        recipe_raw = cls.beautify_recipe_json(recipe_json)
        return Recipe.from_raw_dict(recipe_raw)

    @classmethod
    def recipe_lookup(cls, raw_soup):
        raise NotImplemented

    @classmethod
    def beautify_recipe_json(cls, recipe_json):
        raise NotImplemented


class TastyHtmlRecipeParser(HtmlRecipeParserMixin):

    RECIPE_KEYWORDS = {
        'ingredient': 'ingredients',
        'datepublished': 'date_published'
    }

    @classmethod
    def recipe_lookup(cls, raw_soup):
        return raw_soup.find(type='application/ld+json')

    @classmethod
    def beautify_recipe_json(cls, recipe_json):
        return {
            cls.beautify_recipe_key(key): value
            for key, value in recipe_json.items()
        }

    @classmethod
    def beautify_recipe_key(cls, key):
        new_key = key.split('recipe')[1] if 'recipe' in key else key
        key = new_key.lower()
        return cls.RECIPE_KEYWORDS.get(key, key)

    @classmethod
    def recipes_lookup(self, raw_soup):
        raw_soup.find(type='application/ld+json')