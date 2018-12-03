# www.seekingalpha.com
# Currently only for AAPL
# Search through all pages of news
# Get all href links of news

from html.parser import HTMLParser
import urllib.request, urllib.error
import re
import boto3
import json

# Global variable for storing temporary parsed data
datas = []


# Get href from each news list page
class linkParser(HTMLParser):

    # Get start tag 'a' for href
    def handle_starttag(self, tag, attrs):

        # If not 'a' skip to the next page
        if tag != 'a':
            return

        # If 'a', get tag attributes 
        attr = dict(attrs)

        # Add it to the global datas list
        datas.append(attr)

# Get article data from the given link
class articleParser(HTMLParser):

    # Initialize HTMLParser and flags
    def __init__(self):
        HTMLParser.__init__(self)
        self.inArticleDiv = False
        self.inUselessDiv = False
        self.inScript = False

    # Get start tags
    def handle_starttag(self, tag, attrs):

        # If start tag is not 'div', skip to the next line
        if tag != 'div' and tag != 'script':
            return

        if tag == 'script':
            self.inScript = True

        # If start tag is 'div', get attributes
        attr = dict(attrs)

        # See if 'class' is in attribute
        # !! This is website specific !!
        # www.seekingalpha.com uses 
        # 
        # format to show articles.
        if 'class' in attr:

            # If attribute 'class' is either 'articleText'
            # set flag to True
            # Currently not working possible bug?
            if attr['class'] == 'artText':
                self.inArticleDiv = True

        # If not, set useless flag to True
        # This filters out useless <div>...</div>s between article div
        else:
            self.inUselessDiv = True

    # Get end tags
    def handle_endtag(self, tag):

        # If end tag is 'div' and is useless div, finish skipping
        if tag == 'div' and self.inUselessDiv:
            self.inUselessDiv = False

        # If end tag is 'div' and is article div, finish searching for tag 'p'
        elif tag == 'div' and self.inArticleDiv:
            self.inArticleDiv = False

        elif tag == 'script' and self.inScript:
            self.inScript = False

    # Read data wo/ any tags which is the actual article data needed
    def handle_data(self, data):
        if self.inArticleDiv:
            if not self.inUselessDiv:
                if not self.inScript:
                    datas.append(data)


# Define crawler class
# This class handles every parsing and crawling of a given news page link
class Seeking():

    def __init__(self):
        
        self.result = []
        self.link = ''

    # This is internal function
    # Retrieve parsed data from the given link
    # Parameters:
    # url => link to parse
    # isArticle => False if getting 'href's from news list,
    # True if getting article data from the news page.
    def _getParsed(self, url, isArticle=False):

        try:
            # Create opener for fake user-agent
            opener = urllib.request.build_opener()

            # Add fake user-agent
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]

            # Insert user-agent to opener
            urllib.request.install_opener(opener)

            # Open url with urllib module
            f = urllib.request.urlopen(url)
            
            # Read byte data
            html = f.read()

            # Decode with 'utf-8' character set
            source = html.decode('utf8')
            f.close()
        # Basic error handling
        except urllib.error.HTTPError as e:
            print(e, 'while fetching', url)
            return

        # For crawling for links, use linkParser class
        if not isArticle:
            parser = linkParser()
        
        # For crawling article data, use articleParser class
        else:
            parser = articleParser()

        # Feed data to the parser
        parser.feed(source)

    # This is internal function
    def _getLinks(self, url):

        # Temporary list for keeping multiple links
        result = []

        # Retrieve parsed data from the url
        self._getParsed(url)

        # Iterate each html line and get reference link
        # !! This is website specific !!
        for l in datas:
            if 'target' in l:
                if l['target'] == '_blank':
                    result.append('https://economictimes.indiatimes.com' + l['href'])

        # Top list always contains trash link
        # !! This is website specific !!
        del result[0]

        # Clear datas list for later use
        datas.clear()

        # Return crawled links
        return result

    # This function is called by the user
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
            # print(article)
            self.result.append(article)

            del article

    def getResult(self):
        return self.result


if __name__ in "__main__":

    # Define stock name - Due to change later
    stock_name = 'apple'

    # Number of pages to iterate
    round_count = 10

    # Actual link for the news
    stock_link = 'https://economictimes.indiatimes.com/topics_all.cms?type=article&query=' + stock_name + '&curpg='

    # Declare crawler object to use
    parser = Seeking()

    # Iterator
    i = 1

    while i < round_count:

        # Insert page number to the link
        target = stock_link + str(i)

        # Run crawler
        parser.extractArticle(target)
