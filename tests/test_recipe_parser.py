from unittest import TestCase
from tests import load_mock_file

from models.recipe import Recipe
from parsers.html_recipe_parser import HtmlRecipeParser


class TestMealRecipeParser(TestCase):
    """
    TestMealParser: Test Cases for parse meal entity from given url
    """
    def setUp(self) -> None:
        self.recipe_parser = HtmlRecipeParser()
        self.meal_html_mock = str(load_mock_file('tests/mock/pancake.html'), 'utf-8')

    def test_url_to_meal_recipe(self):
        recipe = self.recipe_parser.html_to_recipe(self.meal_html_mock)
        self.assertIsInstance(recipe, Recipe)