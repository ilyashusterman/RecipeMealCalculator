from unittest import TestCase, skip

from api.recipes_api import RecipesApi
from tests import save_mock_file


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