import json
import logging

from bs4 import BeautifulSoup

from models.recipe import Recipe
from models.recipe import NutritionFacts
from models.recipe import RawRecipe
from parsers.recipe_parser import RecipeParser

class HtmlRecipeParserMixin:
    """
    RecipeParser converts raw string to Recipe class
    """
    FILE_PARSER = 'html.parser'
    @classmethod
    def html_to_recipe(cls, raw_html):
        """
        parse Recipe from html string
        :param raw_html: str
        :return: Recipe
        """
        recipe_raw = cls.from_html_to_recipe_dict(raw_html)
        return Recipe.from_raw_dict(recipe_raw)

    @classmethod
    def from_html_to_recipe_dict(cls, raw_html):
        """

        :param raw_html: str
        :return: dict
        """
        raw_soup = cls.get_raw_soup(raw_html)
        recipe_string = cls.recipe_lookup(raw_soup)
        recipe_dict = cls.get_recipe_dict(recipe_string)
        recipe_raw = cls.beautify_dict_keys(recipe_dict, cls.beautify_recipe_key)
        return recipe_raw

    @classmethod
    def get_recipe_dict(cls, recipe_string):
        recipe_dict = {}
        try:
            recipe_dict = json.loads(recipe_string)
        except json.decoder.JSONDecodeError as e:
            logging.error('Could json not parse recipe dict %s ')
        finally:
            return recipe_dict

    @classmethod
    def get_raw_soup(cls, raw_html):
        raw_soup = BeautifulSoup(raw_html, cls.FILE_PARSER)
        return raw_soup

    @classmethod
    def recipe_lookup(cls, raw_soup):
        raise NotImplemented

    @classmethod
    def beautify_dict_keys(cls, raw_dict, beautify_keys):
        return {
            beautify_keys(key): value
            for key, value in raw_dict.items()
        }

    @classmethod
    def beautify_recipe_key(cls, key):
        raise NotImplemented


class TastyHtmlRecipeParser(HtmlRecipeParserMixin):

    RECIPE_KEYWORDS = {
        'ingredient': 'ingredients',
        'datepublished': 'date_published',
        'nutrition': 'nutrition_facts'
    }

    @classmethod
    def recipe_lookup(cls, raw_soup):
        elements = raw_soup.find_all(type='application/ld+json')
        for element in elements:
            return cls.get_cleaned_recipe(element)

    @classmethod
    def get_cleaned_recipe(cls, element):
        return element.text.strip().replace(',,', ',')

    @classmethod
    def beautify_dict_keys(cls, raw_dict, beautify_keys):
        beautified_recipe = super().beautify_dict_keys(raw_dict, beautify_keys)
        nutrition_facts = {
             key.split('Content')[0]: value
             for key, value in beautified_recipe['nutrition_facts'].items()
        }
        beautified_recipe['nutrition_facts'] = NutritionFacts.from_raw_dict(nutrition_facts)
        return beautified_recipe

    @classmethod
    def beautify_recipe_key(cls, key):
        new_key = key.split('recipe')[1] if 'recipe' in key else key
        key = new_key.lower()
        return cls.RECIPE_KEYWORDS.get(key, key)

    @classmethod
    def find_recipes_from_html(cls, raw_html):
        """

        :param raw_html: str
        :return: recipes generator
        """
        def raw_dict_func(raw_query, raw_html=None):
            return {
                'url': raw_query['href'],
                'name': raw_query.h6.text
            }
        return cls.parse_recipes_from_html(raw_html, raw_dict_func)

    @classmethod
    def find_raw_recipes_from_html(cls, raw_html):
        def raw_dict_func(raw_query, raw_html=None):
            return {
                'url': raw_query['href'],
                'name': raw_query.h6.text,
                'raw_html': raw_html
            }
        return cls.parse_recipes_from_html(raw_html, raw_dict_func, recipe_model=RawRecipe)

    @classmethod
    def parse_recipes_from_html(cls, raw_html, raw_dict_func, recipe_model=Recipe):
        """

        :param raw_html: str
        :return: recipes generator
        """
        raw_soup = cls.get_raw_soup(raw_html=raw_html)
        for raw_query in raw_soup.find_all('a', class_='feed-item analyt-unit-tap'):
            if 'recipe' in raw_query['href']:
                raw_dict = raw_dict_func(raw_query, raw_html)
                yield recipe_model.from_raw_dict(raw_dict)
