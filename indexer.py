from bs4 import BeautifulSoup

base_path = './corpus'

class Indexer:
    def __init__(self, mainUrl, index):
        self.mainUrl = mainUrl
        self.index = index
        self.index_site()

    def getHTMLdocument(self, url):
        with open('{}/{}'.format(base_path, url), encoding='ISO-8859-1') as fp:
            return BeautifulSoup(fp, 'html.parser')

    def index_site(self):
        id = 1
        site_index = self.getHTMLdocument(self.mainUrl)
        self.index.index_document({
            'id': id,
            'text': site_index.get_text()
        })

        for item in site_index.select('a'):
            id += 1
            item_link = item.get('href') if item else None
            try:
                content = self.getHTMLdocument(item_link)

                self.index.index_document({
                    'id': id,
                    'text': content.get_text(),
                })
            except FileNotFoundError:
                continue
        return self.index

