import logging

from requests import get

from models.exceptions import UpdateRecipeException
from parsers.html_recipe_parser import TastyHtmlRecipeParser
from lookup.concurrent_lookup import ConcurrentLookup
from lookup.async_recipes_generator import AsyncRecipesGenerator


class RecipesApi:
    """
    RecipesApi: responsible for fetching recipes
    """
    @classmethod
    def get_html_text(cls, url, headers=None):
        """
        :param url: str
        :return: str
        """
        response = get(url) if headers is None else get(url, headers=headers)
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

    HEADERS = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }

    @classmethod
    def find_recipes_async(cls, query):
        return cls.get_recipes_generator(query)

    @classmethod
    def find_raw_recipes_async(cls, query):
        return cls.get_recipes_generator(query,
                                         find_func=cls.find_unpacked_raw_recipes_with_urls)

    @classmethod
    def get_recipes_generator(cls, query, find_func=None):
        find_func = cls.find_unpacked_recipes_with_urls if find_func is None else find_func
        return AsyncRecipesGenerator(query,
                                     find_func,
                                     cls.load_recipe)

    @classmethod
    def find_loaded_recipes(cls, query):
        unpacked_recipes = cls.find_unpacked_recipes_with_urls(query)
        return cls.load_recipes(unpacked_recipes)

    @classmethod
    def load_recipes(cls, unpacked_recipes):
        recipes_lookup = ConcurrentLookup(unpacked_recipes, load_recipe_func=cls.load_recipe)
        recipes_lookup.load_recipes()
        return recipes_lookup.recipes

    @classmethod
    def find_unpacked_raw_recipes_with_urls(cls, query):
        return cls.find_recipes_with_urls(query, find_func=cls.find_raw_recipes_from_html)

    @classmethod
    def find_unpacked_recipes_with_urls(cls, query):
        return cls.find_recipes_with_urls(query, find_func=cls.find_recipes_from_html)

    @classmethod
    def find_recipes_with_urls(cls, query, find_func):
        """

        :param query: str
        :return: [] Recipes
        """
        url_search = '%s%s' % (cls.BASE_URL, cls.QUERY_SEARCH_FORMAT % query)
        raw_recipes = cls.get_html_text(url_search)
        return find_func(raw_recipes)

    @classmethod
    def load_recipe(cls, recipe):
        try:
            raw_recipe_html = cls.get_html_text(recipe.url, headers=cls.HEADERS)
        except Exception as e:
            logging.error('Could not load recipe %s correctly %s' % (recipe.url, e))
        else:
            cls.update_recipe_content(raw_recipe_html, recipe)
        finally:
            return recipe

    @classmethod
    def update_recipe_content(cls, raw_recipe_html, recipe):
        raw_recipe_dict = cls.from_html_to_recipe_dict(raw_recipe_html)
        try:
            recipe.update_from_raw_dict(raw_recipe_dict)
        except UpdateRecipeException as e:
            logging.error('Failed update %s Recipe for url %s Due to %s' % (
                recipe.name, recipe.url, e))
            return False
        else:
            return True
