# www.nasdaq.com
# Currently only for AAPL
# Search through all pages of news
# Get all href links of news

from html.parser import HTMLParser
import urllib.request, urllib.error
import re

datas = []


class linkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return

        attr = dict(attrs)
        datas.append(attr)


class articleParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = False
        self.inArticleDiv = False
        self.inUselessDiv = False

    def handle_starttag(self, tag, attrs):

        if tag != 'p' and tag != 'div':
            return

        attr = dict(attrs)

        if 'id' in attr:
            if attr['id'] == 'articleText' or attr['id'] == 'articlebody':
                self.inArticleDiv = True
            else:
                self.inUselessDiv = True

        self.recording = True

    def handle_endtag(self, tag):
        if tag == 'p' and self.recording:
            self.recording = False
        elif tag == 'div' and self.inUselessDiv:
            self.inUselessDiv = False
        elif tag == 'div' and self.inArticleDiv:
            self.inArticleDiv = False

    def handle_data(self, data):
        if self.recording and self.inArticleDiv:
            if not self.inUselessDiv:
                datas.append(data)


class getNewsArticle():

    def __init__(self):

        self.article = []

    def _getParsed(self, url, isArticle=False):

        try:
            f = urllib.request.urlopen(url)
            html = f.read()
            source = html.decode('utf8')
            f.close()
        except urllib.error.HTTPError as e:
            print(e, 'while fetching', url)
            return

        if not isArticle:
            parser = linkParser()
        else:
            parser = articleParser()
        parser.feed(source)

    def _getLinks(self, url):

        result = []

        self._getParsed(url)

        for l in datas:
            if 'target' in l:
                if l['target'] == '_self':
                    result.append(l['href'])

        del result[0]
        datas.clear()

        return result

    def extractArticle(self, url):

        page = self._getLinks(url)

        for links in page:
            article = ''

            datas.clear()

            print(links)
            self._getParsed(links, True)

            for d in datas:
                article += d

            article = article.replace('\n', '')
            article = article.replace('\r', '')

            article = re.sub(' +', ' ', article)
            print(article)

            del article


if __name__ in "__main__":

    stock_name = 'aapl'
    round_count = 10
    stock_link = 'https://www.nasdaq.com/symbol/' + stock_name + '/news-headlines?page='
    parser = getNewsArticle()

    output = []
    i = 1

    while i < round_count:
        target = stock_link + str(i)
        parser.extractArticle(target)