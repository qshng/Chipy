from itunes_scraper.table_parser import HTMLTableParser
if __name__ == '__main__':
    url = "https://itunes.apple.com/us/podcast/radiolab/id152249110?mt=2"
    hp = HTMLTableParser()
    table = hp.parse_url(url)[0][1] # Grabbing the table from the tuple
    table.head()