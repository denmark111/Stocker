# www.nasdaq.com
# Currently only for AAPL
# Search through pre-defined pages of news
# Get all href links of news and extract news article

from html.parser import HTMLParser
import urllib.request, urllib.error
import re

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
        self.recording = False
        self.inArticleDiv = False
        self.inUselessDiv = False

    # Get start tags
    def handle_starttag(self, tag, attrs):

        # If start tag is neither 'p' nor 'div', skip to the next line
        if tag != 'p' and tag != 'div':
            return

        # If start tag is 'p' or 'div', get attributes
        attr = dict(attrs)

        # See if 'id' is in attribute
        # !! This is website specific !!
        # www.nasdaq.com uses 
        # <div id="articleText"> <p>article</p> </div> or
        # <div id="articlebody"> <p>article</p> </div>
        # format to show articles.
        if 'id' in attr:

            # If attribute 'id' is either 'articleText' or 'articlebody'
            # set flag to True
            # Currently not working possible bug?
            if attr['id'] == 'articleText' or attr['id'] == 'articlebody':
                self.inArticleDiv = True

        # If not, set useless flag to True
        # This filters out useless <div>...</div>s between article div
        else:
            self.inUselessDiv = True

        # Set flag to read sources
        self.recording = True

    # Get end tags
    def handle_endtag(self, tag):

        # If end tag is 'p', finish reading
        if tag == 'p' and self.recording:
            self.recording = False

        # If end tag is 'div' and is useless div, finish skipping
        elif tag == 'div' and self.inUselessDiv:
            self.inUselessDiv = False

        # If end tag is 'div' and is article div, finish searching for tag 'p'
        elif tag == 'div' and self.inArticleDiv:
            self.inArticleDiv = False

    # Read data wo/ any tags which is the actual article data needed
    def handle_data(self, data):
        if self.recording and self.inArticleDiv:
            if not self.inUselessDiv:
                datas.append(data)


# Define crawler class
# This class handles every parsing and crawling of a given news page link
class getNewsArticle():

    def __init__(self):

        # Currently not in use
        self.article = []

    # This is internal function
    # Retrieve parsed data from the given link
    # Parameters:
    # url => link to parse
    # isArticle => False if getting 'href's from news list,
    # True if getting article data from the news page.
    def _getParsed(self, url, isArticle=False):

        try:
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
                if l['target'] == '_self':
                    result.append(l['href'])

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
            print(article)

            del article


# Main function calls crawler
if __name__ in "__main__":

    # Define stock name - Due to change later
    stock_name = 'aapl'

    # Number of pages to iterate
    round_count = 10

    # Actual link for the news
    stock_link = 'https://www.nasdaq.com/symbol/' + stock_name + '/news-headlines?page='
    
    # Declare crawler object to use
    parser = getNewsArticle()

    # Iterator
    i = 1

    while i < round_count:

        # Insert page number to the link
        target = stock_link + str(i)

        # Run crawler
        parser.extractArticle(target)