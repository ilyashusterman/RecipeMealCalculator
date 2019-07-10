from requests import get


class MealParser(object):

    def url_to_meal_recipe(self, meal_html_file):
        pass

    def html_to_meal_recipe(self, html):
        pass

    def get_html_text(self, url):
        response = get(url)
        if response.status_code != 200:
            raise Exception('Url not valid url %s %s' % (url, response.content))
        return response.text
