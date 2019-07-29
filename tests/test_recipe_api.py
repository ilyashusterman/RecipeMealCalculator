from unittest import TestCase, skip

from api.recipes_api import RecipesApi, TastyApi
from tests import save_mock_file, load_mock_file


class TestMealApi(TestCase):
    """
    TestMealApi: Test Cases for fetch htmml content from recipe url
    """
    @skip('Api call to download file')
    def test_get_html_content(self):
        base_url = 'https://tasty.co/recipe/'
        filename = "tasty-101-buttermilk-pancakes"
        url = '%s%s' % (base_url, filename)

        self.extract_url_to_html_file(filename, url)

    def extract_url_to_html_file(self, filename, url):
        content = RecipesApi.get_html_text(url=url)
        self.assertIsInstance(content, str)
        content = content.encode('utf-8')
        save_mock_file(filename='%s.html' % filename, content=content)

    @skip('Require api call to wait..')
    def test_find_unpacked_recipes_with_urls(self):
        api = TastyApi()
        unpacked_recipes = api.find_unpacked_recipes_with_urls('pancake')
        self.assertEqual(len(list(unpacked_recipes)), 18)
        recipes = api.load_recipes(unpacked_recipes)

    @skip('Require api call to wait..')
    def test_load_recipes_to_dict(self):
        api = TastyApi()
        unpacked_recipes = api.find_unpacked_recipes_with_urls('pancake')
        recipes = api.load_recipes(unpacked_recipes)
        self.assertEqual(len(next(recipes).to_dict()), 8)

    def test_load_recipes(self):
        api = TastyApi()
        tasty_recipes_html_mock = str(load_mock_file('tests/mock/pancakes_recipes_search.html'), 'utf-8')
        recipes = api.find_recipes_from_html(tasty_recipes_html_mock)
        recipes = api.load_recipes(recipes)
        self.assertEqual(next(recipes).category, 'Breakfast')
        self.assertIsInstance(recipes, type((i for i in range(1))))