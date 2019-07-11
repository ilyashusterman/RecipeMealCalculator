from requests import get


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