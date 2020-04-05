from requests import get
from urllib.parse import quote
from unidecode import unidecode
    
class http():
    def __init__(self, base_url):
        self.base_url = base_url

    def request(self, ext_url):
        if isinstance(ext_url, unicode):
            ext_url = unidecode(ext_url)
        return get(self.base_url + quote(ext_url, "?=&")).text
