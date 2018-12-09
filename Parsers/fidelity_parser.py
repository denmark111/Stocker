#!/usr/bin/python3

from html.parser import HTMLParser
import urllib.request
import urllib.error
import string
import re
import time
import boto3
import json
import pymysql.cursors

datas = []  # Global variable for storing temporary parsed data
output = []  # Global varialbe for sorting URL date
result = []  # Global varialbe for getting URL in fidelity.com
articleTitle = []  # Global varialbe for storing article title
articleDate = []  # Global varialbe for storing article title
articleContent = []  # Global varialbe for storing article content

# Get href from each news list page


class AWSAccess():

    def __init__(self):
        self.comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

    def getSentimentResult(self, text):
        return self.comprehend.detect_sentiment(Text=text, LanguageCode='en')

    def getKeywordResult(self, text):
        return self.comprehend.detect_key_phrases(Text=text, LanguageCode='en')



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


class articleParser(HTMLParser):

    # Initialize HTMLParser and flags
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = False
        self.inArticleDiv = False
        self.inUselessDiv = False

    # Get start tags
    def handle_starttag(self, tag, attrs):

        # If start tag is neither 'div' nor 'script', skip to the next line
        if tag != 'div' and tag != 'script':
            return

        # If start tag is 'div' or 'script', get attributes
        attr = dict(attrs)

        # See if 'role' is in attribute
        # !! This is website specific !!
        # www.fidelity.com uses
        # <div role="main"> <script> article </script> </div>
        # format to show articles.
        if 'role' in attr:

            # If attribute 'role' is either 'main'
            if attr['role'] == 'main':
                self.inArticleDiv = True

            # If not, set useless flag to True
            # This filters out useless <div>...</div>s between article div
            else:
                self.inUselessDiv = True

        # Set flag to read sources
        self.recording = True

    # Get end tags
    def handle_endtag(self, tag):

        # If end tag is 'div', finish reading
        if tag == 'div' and self.recording:
            self.recording = False

        # If end tag is 'div' and is useless div, finish skipping
        elif tag == 'div' and self.inUselessDiv:
            self.inUselessDiv = False

        # If end tag is 'script' and is article div, finish searching for tag 'script'
        elif tag == 'script' and self.inArticleDiv:
            self.inArticleDiv = False

    # Read data wo/ any tags which is the actual article data needed
    def handle_data(self, data):
        if self.recording and self.inArticleDiv:
            if not self.inUselessDiv:
                datas.append(data)


class Fidelity():

    def __init__(self):

        # Currently not in use
        self.article = []
        self.link = ''

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

            # Time delay for crawler anti-block
            time.sleep(3)
        # Basic error handling
        except urllib.error.HTTPError as e:
            print(e, 'while fetching', url)
            return
        except urllib.error.HTTPError as h:
            print(h, 'while fetching', url)
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

        # Retrieve parsed data from the url
        self._getParsed(url)

        # Iterate each html line and get reference link
        # !! This is website specific !!
        for l in datas:
            if 'target' in l and 'title' in l:
                if l['target'] == '_top':
                    # Top list always contains trash link
                    if l['href'] != 'https://www.fidelity.com/sector-investing/overview':
                        result.append(l['href'])
                        # array, output store date sequence
                        output.append(l['href'].split('/')[6])
                        articleTitle.append(l['title'])

        # Clear datas list for later use
        datas.clear()

        # terminate this function
        return None

    # This function is called by the user
    def extractArticle(self, url):

        final_art = []

        for links in url:

            article = ''
            temp_article = ''

            datas.clear()

            self._getParsed(links, True)

            for d in datas:
                article = article + str(d)
            # Pasing the article gotten by crawler
            if '"text":' not in article:
                return

            if 'This story has been deleted by the news provider.' in article:
                article = '"text":>it is a unnecessary article.<'

            article = article.split('"text":')[1]
            article = article.replace('\r', ' ')
            article = article.replace('\n', ' ')
            article = article.replace('&quot;', ' ')
            article = article.replace('&amp;', ' ')
            temp = article.split('>')

            for i in temp:
                temp_article = temp_article + i.split('<')[0]

            article = temp_article

            article = re.sub('(END).*', ' ', article)
            article = re.sub(',"receivedTime".*', ' ', article)
            article = re.sub('","service".*', ' ', article)
            article = re.sub('\\n\\n.*', ' ', article)
            article = re.sub(';\s\d\d\d-\d\d\d-\d\d\d\d.*', ' ', article)
            article = re.sub('\\n\\n\\n\\n.*', ' ', article)
            article = re.sub('\(Reporting by.*', ' ', article)
            article = re.sub('\"', ' ', article)
            article = article.replace('\\n', '')

            article = re.sub(' +', ' ', article)
            articleContent.append(article)
            print(article)
            final_art.append(article)

            if len(articleContent) == len(result):
                return

            del article

        return final_art

# Re-extract clean data


def get_article_info():
    # Get num of index, each content
    for i, x in enumerate(articleContent, 0):
        # If parsed article is unnecessary, it is deleted in each list
        if 'it is a unnecessary article.' in x:
            del articleContent[i]
            del output[i]
            del articleTitle[i]
            del articleDate[i]
            del result[i]

def getAwsResult(stock_name):
    aws = AWSAccess()

    sentiment = []
    keywords = []
    keyword_trimmed = []
    words_string = ''

    for elem in articleContent:
        sentiment.append(aws.getSentimentResult(elem))
        keywords.append(aws.getKeywordResult(elem))

    for elem in keywords:
        
        for words in elem['KeyPhrases']:
            words_string += (words['Text'] + ' ')
        
        keyword_trimmed.append(words_string)
        print(words_string)
        words_string = ''

    # Join Database
    conn = pymysql.connect( 
        host='210.117.181.240', 
        user='home_user',
        password='qaz1234', 
        db='STOCKER', 
        charset='utf8mb4',
        autocommit=True)
    # Declare cursor for use query  
    cursor=conn.cursor()
    # Insert article datas into the table
    sql = 'INSERT INTO fidelity (stockName, articleTime, keyWords, positiveRate, negativeRate, mixedRate, neutralRate) VALUES (%s, %s, %s, %s, %s, %s, %s)'

    for i in range(len(articleContent)):
        cursor.execute(sql,(stock_name, articleDate[i], keyword_trimmed[i],
            sentiment[i]['SentimentScore']['Positive'],
            sentiment[i]['SentimentScore']['Negative'],
            sentiment[i]['SentimentScore']['Mixed'],
            sentiment[i]['SentimentScore']['Neutral']))

    conn.close()

if __name__ in "__main__":

    stock_name = input()
    stock_link1 = 'https://search.fidelity.com/search/getNewsSearchResults?question=' + \
        stock_name + '&originatingpage=NSRP&NSRPpageSelected='
    stock_link2 = '&navState=root%7Croot-'
    stock_link3 = '-10%7C0&binningState=&sortBy=&sourceBoxState=&bundleName=news-bundle'

    # Use for sort URL
    temp_result = []
    # Use for sort article title
    temp_article = []

    # Declare crawler object to use
    parser = Fidelity()

    # Declare AWS access object
    aws = AWSAccess()

    target = []
    for pagenum in range(0, 1):
        target.append(stock_link1 + str(pagenum+1) +
                      stock_link2 + str(pagenum*10) + stock_link3)
        parser._getLinks(target[pagenum])
    # Insert page number to the link
    temp_result = result.copy()
    # Copy article titile for sorting
    temp_article = articleTitle.copy()

    # sort url, title in chronological order ////////
    output.sort()
    for i in output:
        articleDate.append(i[0:8])

    for i in range(0, len(output)):
        result[i] = temp_result[int(output[i].split('=')[1])-1]
        articleTitle[i] = temp_article[int(output[i].split('=')[1])-1]
    # sort url, title in chronological order ////////

    # Run crawler
    while True:
        parser.extractArticle(result)
        if len(articleContent) == len(result):
            break
    # re-extract clean data
    get_article_info()

    getAwsResult(stock_name)