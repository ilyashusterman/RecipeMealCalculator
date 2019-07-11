from unittest import TestCase
from tests import load_mock_file

from models.meal_recipe import Recipe
from parsers.recipe_parser import RecipeParser


class TestMealRecipeParser(TestCase):
    """
    TestMealParser: Test Cases for parse meal entity from given url
    """
    def setUp(self) -> None:
        self.meal_parser = RecipeParser()
        self.meal_html_mock = str(load_mock_file('tests/mock/pancake.html'), 'utf-8')

    def test_url_to_meal_recipe(self):
        meal_recipe = self.meal_parser.html_to_meal_recipe(self.meal_html_mock)
        self.assertIsInstance(meal_recipe, Recipe)