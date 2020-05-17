from bs4 import BeautifulSoup


def html_parse(input_string):
    ret_soup = BeautifulSoup(input_string, 'html.parser')

    return ret_soup
