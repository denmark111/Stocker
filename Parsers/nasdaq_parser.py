# www.nasdaq.com
# Currently only for AAPL
# Search through all pages of news
# Get all href links of news

from html.parser import HTMLParser
import urllib.request, urllib.error

links = []


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return

        attr = dict(attrs)
        links.append(attr)


def extract(url):

    result = []

    try:
        f = urllib.request.urlopen(url)
        html = f.read()
        source = html.decode('utf8')
        f.close()
    except urllib.error.HTTPError as e:
        print(e, 'while fetching', url)
        return

    parser = MyHTMLParser()
    parser.links = []
    parser.feed(source)
    for l in links:
        if 'target' in l:
            if l['target'] == '_self':
                result.append(l['href'])

    del result[0]
    links.clear()

    return result


if __name__ in "__main__":

    stock_name = 'aapl'
    stock_link = 'https://www.nasdaq.com/symbol/' + stock_name + '/news-headlines?page='
    output = []

    for i in range(1, 10):
        target = stock_link + str(i)

        print(target)

        output.append(extract(target))
        print(output[i - 1])