from unittest import TestCase

from parsers.meal_parser import MealParser


class TestMealParser(TestCase):
    """
    TestMealParser: Test Cases for parse meal entity from given url
    """
    def setUp(self) -> None:
        self.meal_parser = MealParser()
        self.meal_html_file = open('text_meal.html')

    def test_url_to_meal_recipe(self):

        meal_recipe = self.meal_parser.html_to_meal_recipe(self.meal_html_file)
        self.assertIsInstance(meal_recipe, MealRecipe)