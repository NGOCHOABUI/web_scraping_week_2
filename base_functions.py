from bs4 import BeautifulSoup
import requests

class Base_Functions():
    def __init__(self):
        pass

    @classmethod   
    def get_url(cls, url):
        try:
            response = requests.get(url).text
            soup = BeautifulSoup(response, 'html.parser')
            return soup
        except Exception as err:
            print('ERROR BY REQUEST:', err)