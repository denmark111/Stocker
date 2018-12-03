# Top application for running multiple crawlers

from AWS.aws_access import AWSAccess
from Parsers.seeking_alpha_parser import Seeking
from Parsers.nasdaq_parser import Nasdaq


def runCrawler(parser, url, pageCount):

    # Iterator
    i = 2

    # Begin crawling
    while i < pageCount:
                 
        # Insert page number to the link
        target = url + str(i)

        # Run crawler
        parser.extractArticle(target)

    # Get news result
    result = parser.getResult()

    _printResult(result)


def _printResult(article):

    # AWS Comprehend API class
    comprehend = AWSAccess()

    # Start analistics with AWS Comprehend API
    for elem in article:
        print("in for")
        print(comprehend.getResult(elem))


if __name__ in '__main__':
    
    # Page count to read from the webpage
    pageCount = 3

    # Nasdaq page
    # nasdaq = Nasdaq()
    stock_name = 'aapl'
    stock_link = 'https://www.nasdaq.com/symbol/' + stock_name + '/news-headlines?page='
    # runCrawler(nasdaq, stock_link, pageCount)

    # Seeking Alpha page
    seeking = Seeking()
    stock_name = 'apple'
    stock_link = 'https://economictimes.indiatimes.com/topics_all.cms?type=article&query=' + stock_name + '&curpg='
    runCrawler(seeking, stock_link, pageCount)
