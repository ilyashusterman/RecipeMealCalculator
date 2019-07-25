import logging

from requests import get

from models.recipes_lookup import RecipesLookup
from parsers.html_recipe_parser import TastyHtmlRecipeParser


class RecipesApi:
    """
    RecipesApi: responsible for fetching recipes
    """
    @classmethod
    def get_html_text(cls, url):
        """
        :param url: str
        :return: str
        """
        response = get(url)
        if response.status_code != 200:
            raise Exception(
                'Url not valid url %s %s' % (url, response.content))
        return response.text


class TastyApi(RecipesApi, TastyHtmlRecipeParser):
    """
    TastyApi: fetching tasty list recipes url and search recipes by query meal
    """
    BASE_URL = 'https://tasty.co/'
    QUERY_SEARCH_FORMAT = 'search?q=%s'

    @classmethod
    def find_loaded_recipes(cls, query):
        unpacked_recipes = cls.find_recipes_with_urls(query)
        return cls.load_recipes(unpacked_recipes)

    @classmethod
    def load_recipes(cls, unpacked_recipes):
        recipes_lookup = RecipesLookup(unpacked_recipes, load_recipe_func=cls.load_recipe)
        recipes_lookup.load_recipes()
        return recipes_lookup.recipes

    @classmethod
    def find_recipes_with_urls(cls, query):
        """

        :param query: str
        :return: RecipesLookup
        """
        url_search = '%s%s' % (cls.BASE_URL, cls.QUERY_SEARCH_FORMAT % query)
        raw_recipes = cls.get_html_text(url_search)
        return cls.find_recipes_from_html(raw_recipes)

    @classmethod
    def load_recipe(cls, recipe):
        raw_recipe_html = cls.get_html_text(recipe.url)
        raw_recipe_dict = cls.from_html_to_recipe_dict(raw_recipe_html)
        try:
            return recipe.update_from_raw_dict(raw_recipe_dict)
        except Exception as e:
            logging.error('Could not load recipe %s correctly %s' % (recipe.url, e))
        return recipe
