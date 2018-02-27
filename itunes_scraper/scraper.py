from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import pandas as pd

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


def get_itunes_podcast_urls(self):
    """Return a list of all podcast urls on this page."""
    podcast_soup = self.soup.find("div", id="selectedcontent")
    a_list = podcast_soup.find_all("a")
    urls = []
    for tag in a_list:
        urls.append(tag.get('href'))
    return urls


def make_soup(url, parser='html.parser'):
    raw_html = simple_get(url)
    soup = BeautifulSoup(raw_html, parser)
    return soup


def get_table_header(tr):
    column_name = []
    for i, row in enumerate(tr):
        if i == 0:
            headers = row.find_all('th')
            for h in headers:
                column = h.get_text()
                column = column.strip()
                if column:
                    column_name.append(column)
        if i == 1:
            attrs = row.attrs
            attrs_cols = list(attrs.keys())
            [column_name.append(col) for col in attrs_cols]

    return column_name


if __name__ == '__main__':
    url = "https://itunes.apple.com/us/podcast/radiolab/id152249110?mt=2"
    soup = make_soup(url)
    # episodes = soup.find_all(class_= 'podcast-episode')
    # print(episodes)
    table = soup.find_all('table')[0]  # Grab the first table
    tr = table.find_all('tr')
    headers = get_table_header(tr)

    new_table = pd.DataFrame(data=None, columns=headers)

    # populate table!
    # expand df with attrs_cols
    for i, row in enumerate(tr):
        for key in row.attrs.keys():
            new_table.loc[i, key] = row.attrs[key]
