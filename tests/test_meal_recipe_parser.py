from unittest import TestCase, skip
from tests import load_mock_file

from models.meal_recipe import MealRecipe
from parsers.meal_recipe_parser import MealParser


class TestMealRecipeParser(TestCase):
    """
    TestMealParser: Test Cases for parse meal entity from given url
    """
    def setUp(self) -> None:
        self.meal_parser = MealParser()
        # self.meal_html_mock = load_mock_file()

    def test_get_html_content(self):
        content = self.meal_parser.get_html_text(url="https://tasty.co/recipe/tasty-101-buttermilk-pancakes")
        self.assertIsInstance(content, str)

    @skip
    def test_url_to_meal_recipe(self):
        meal_recipe = self.meal_parser.html_to_meal_recipe(self.meal_html_mock)
        self.assertIsInstance(meal_recipe, MealRecipe)