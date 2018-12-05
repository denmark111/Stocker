# Top application for running multiple crawlers

from AWS.aws_access import AWSAccess
from Parsers.seeking_alpha_parser import Seeking
from Parsers.nasdaq_parser import Nasdaq
#from Parsers.fidelity_parser import Fidelity
import time


def runCrawler(parser, url, pageCount):

    #if parser == fidelity : 
        #url = url + str(pageCount+1)+'&navState=root%7Croot-' + str(pageCount*10) + '-10%7C0&binningState=&sortBy=&sourceBoxState=&bundleName=news-bundle'

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

    print("result : {}".format(result))

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
    nasdaq = Nasdaq()
    stock_name = 'aapl'
    stock_link = 'https://www.nasdaq.com/symbol/' + stock_name + '/news-headlines?page='
    runCrawler(nasdaq, stock_link, pageCount)

    # Seeking Alpha page
    # seeking = Seeking()
    stock_name = 'apple'
    stock_link = 'https://economictimes.indiatimes.com/topics_all.cms?type=article&query=' + stock_name + '&curpg='
    # runCrawler(seeking, stock_link, pageCount)

    # Fidelity page
    # fidelity = Fidelity()
    # stock_name = 'appl'
    # stock_link = 'https://search.fidelity.com/search/getNewsSearchResults?question=' + stock_name + '&originatingpage=NSRP&NSRPpageSelected=' 
    # runCrawler(fidelity, stock_link, pageCount)