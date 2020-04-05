from bs4 import BeautifulSoup as bs

def html_parse(input_string):
    ret_soup = bs(input_string, 'html.parser')

    return ret_soup
