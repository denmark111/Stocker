# www.seekingalpha.com
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
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
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
            if l['target'] == '_blank':
                result.append('https://economictimes.indiatimes.com' + l['href'])

    links.clear()

    return result


if __name__ in "__main__":

    stock_name = 'aapl'
    stock_link = 'https://economictimes.indiatimes.com/topics_all.cms?type=article&query=' + stock_name + '&curpg='
    output = []
    i = 1

    while True:
        target = stock_link + str(i)
        output.append(extract(target))

        if not output[i - 1]:
            break
        else:
            print(output[i - 1])
            i += 1
