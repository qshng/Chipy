from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re

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
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def get_itunes_podcast_urls(self):
    """Return a list of all podcast urls on this page."""
    podcast_soup = self.soup.find("div", id="selectedcontent")
    a_list = podcast_soup.find_all("a")
    urls = []
    for tag in a_list:
        urls.append(tag.get('href'))
    return urls

if __name__ == '__main__':
    starting_url = "https://itunes.apple.com/us/podcast/radiolab/id152249110?mt=2"
    raw_html = simple_get(starting_url)
    soup = BeautifulSoup(raw_html, 'html.parser')
    header = soup.find_all(re.compile('^h[1-6]$'))
    tables = soup.findChildren('table')
    my_table = tables[0]
    rows = my_table.findChildren(['th', 'tr'])
    for row in rows:
        print(row)