import json
import logging

from bs4 import BeautifulSoup

from models.recipe import Recipe


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
        recipe_raw = cls.beautify_recipe_json(recipe_dict)
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
    def beautify_recipe_json(cls, recipe_json):
        raise NotImplemented


class TastyHtmlRecipeParser(HtmlRecipeParserMixin):

    RECIPE_KEYWORDS = {
        'ingredient': 'ingredients',
        'datepublished': 'date_published'
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
    def find_recipes_from_html(cls, raw_html):
        """

        :param raw_html: str
        :return: recipes generator
        """
        raw_soup = cls.get_raw_soup(raw_html=raw_html)
        for raw_query in raw_soup.find_all('a', class_='feed-item analyt-unit-tap'):
            if 'recipe' in raw_query['href']:
                raw_dict = {
                    'url': raw_query['href'],
                    'name': raw_query.h6.text
                }
                yield Recipe.from_raw_dict(raw_dict)
