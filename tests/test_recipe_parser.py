from unittest import TestCase
from tests import load_mock_file

from models.recipe import Recipe, NutritionFacts
from parsers.html_recipe_parser import TastyHtmlRecipeParser


class TestRecipeParser(TestCase):
    """
    TestRecipeParser: Test Cases for parse meal entity from given url
    """
    def setUp(self) -> None:
        self.recipe_parser = TastyHtmlRecipeParser()
        self.tasty_recipe_html_mock = str(load_mock_file('tests/mock/pancake.html'), 'utf-8')
        self.tasty_fluffy_recipe_html_mock = str(load_mock_file('tests/mock/test_fluffy_pancakes.html'), 'utf-8')
        self.tasty_recipes_html_mock = str(load_mock_file('tests/mock/pancakes_recipes_search.html'), 'utf-8')

    def test_html_to_recipe(self):
        recipe = self.recipe_parser.html_to_recipe(self.tasty_recipe_html_mock)
        self.assertIsInstance(recipe, Recipe)
        self.assertEqual(len(recipe.ingredients), 12)
        self.assertIsInstance(recipe.nutrition_facts, NutritionFacts)
        self.assertEqual(recipe.nutrition_facts.protein, '7 grams')
        self.assertEqual(recipe.nutrition_facts.fat, '16 grams')

    def test_html_to_fluffy_pancake_recipe(self):
        recipe = self.recipe_parser.html_to_recipe(self.tasty_fluffy_recipe_html_mock)
        self.assertIsInstance(recipe, Recipe)
        self.assertEqual(len(recipe.ingredients), 7)

    def test_recipes_lookup(self):
        recipes = self.recipe_parser.find_recipes_from_html(self.tasty_recipes_html_mock)
        self.assertEqual(len(list(recipes)), 18)
