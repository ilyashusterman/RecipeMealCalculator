import json


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
        recipe_element = cls.recipe_lookup(raw_soup)
        recipe_json = json.loads(recipe_element.text)
        recipe_raw = cls.beautify_recipe_json(recipe_json)
        return recipe_raw

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
    def find_recipes_from_html(cls, raw_html):
        """

        :param raw_html: str
        :return: recipes generator
        """
        raw_soup = cls.get_raw_soup(raw_html=raw_html)
        for raw_query in raw_soup.find_all('a', class_='feed-item analyt-unit-tap'):
            raw_dict = {
                'url': raw_query['href'],
                'name': raw_query.h6.text
            }
            yield Recipe.from_raw_dict(raw_dict)
