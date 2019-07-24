from requests import get

from parsers.html_recipe_parser import TastyHtmlRecipeParser


class RecipesApi:
    """
    RecipesApi: responsible for fetching recipes
    """
    @classmethod
    def get_html_text(cls, url):
        """
        :param url: str
        :return: str
        """
        response = get(url)
        if response.status_code != 200:
            raise Exception(
                'Url not valid url %s %s' % (url, response.content))
        return response.text


class TastyApi(RecipesApi, TastyHtmlRecipeParser):
    """
    TastyApi: fetching tasty list recipes url and search recipes by query meal
    """
    BASE_URL =  'https://tasty.co/'
    QUERY_SEARCH_FORMAT = 'search?q=%s'

    @classmethod
    def find_recipes_urls(cls, query):
        url_search = '%s%s' % (cls.BASE_URL, cls.QUERY_SEARCH_FORMAT % query)
        raw_recipes = cls.get_html_text(url_search)
        with open('pancakes_recipes_search.html', 'w') as f:
            f.write(raw_recipes)

        return cls.recipes_lookup(raw_recipes)
