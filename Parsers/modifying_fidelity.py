from html.parser import HTMLParser
import urllib.request, urllib.error
import string
import re

datas = []
output = [] # use for sort URL date
result = [] # get article title URL in fidelity.com
temp_result = [] # use for sort URL

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
              
    for l in datas: 
        if 'target' in l and 'title' in l:  
            if l['target'] == '_top': 
                if l['href']!='https://www.fidelity.com/sector-investing/overview' : 
                   result.append(l['href'])
                   
                   #output.append(l['href'].strip('https://www.fidelity.com/news/article/compony-news' + 'https://www.fidelity.com/news/article/default' + 'https://www.fidelity.com/news/article/us-markets' + 'https://www.fidelity.com/news/article/investing-ideas' + 'https://www.fidelity.com/news/article/mergers-and-quisition' + 'https://www.fidelity.com/news/article/technology'))
                   output.append(l['href'].split('/')[6])
        
    datas.clear() 

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
        if tag != 'p' or tag != 'div':
            return

        # If start tag is 'p' or 'div', get attributes
        attr = dict(attrs)

        # See if 'id' is in attribute
        # !! This is website specific !!
        # www.nasdaq.com uses 
        # <div id="articleText"> <p>article</p> </div> or
        # <div id="articlebody"> <p>article</p> </div>
        # format to show articles.
        if 'class' in attr :

            # If attribute 'id' is either 'articleText' or 'articlebody'
            if attr['class'] == 'scl-news-article--description ng-binding' :
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
           if 'target' in l and 'title' in l:  
             if l['target'] == '_top':
                 # Top list always contains trash link 
                if l['href']!='https://www.fidelity.com/sector-investing/overview' : 
                   result.append(l['href'])
                   
                   #output.append(l['href'].strip('https://www.fidelity.com/news/article/compony-news' + 'https://www.fidelity.com/news/article/default' + 'https://www.fidelity.com/news/article/us-markets' + 'https://www.fidelity.com/news/article/investing-ideas' + 'https://www.fidelity.com/news/article/mergers-and-quisition' + 'https://www.fidelity.com/news/article/technology'))
                   output.append(l['href'].split('/')[6])

        # Clear datas list for later use
        datas.clear()

        # Return crawled links
        return None

    # This function is called by the user
    def extractArticle(self, url):

        self._getLinks(url)

        # temp_result = result       
        temp_result = result.copy()
        #sort url date
        output.sort()
        #sort url in chronological order ////////
        for i in range(0,len(result)) :
            result[i]=temp_result[int(output[i].split('=')[1])-1]

        #for i in range(0,len(result)):    
        #  print(result[i])
        #sort url in chronological order ////////

        for links in result:
            article = ''

            datas.clear()

            print(links)
            self._getParsed(links, True)

            for d in datas:
                article = article + d

            article = article.replace('\n', '')
            article = article.replace('\r', '')

            article = re.sub(' +', ' ', article)
            print(article)

            del article

if __name__ in "__main__": 
  
      stock_name = 'amzn' 
      pagenum = 0 
      stock_link1 = 'https://search.fidelity.com/search/getNewsSearchResults?question=' + stock_name + '&originatingpage=NSRP&NSRPpageSelected=' 
      stock_link2 =  '&navState=root%7Croot-' 
      stock_link3 = '-10%7C0&binningState=&sortBy=&sourceBoxState=&bundleName=news-bundle' 

      
      #result.reverse()
      #for i in range(0,len(result)):    
      #    print(result[i])
      #temp_result.clear()

      # Declare crawler object to use
      parser = getNewsArticle()

      # Iterator
      
      round_count = 10
      while pagenum < round_count:

        # Insert page number to the link
        target = stock_link1 + str(pagenum+1)+ stock_link2 + str(pagenum*10) + stock_link3 

        # Run crawler
        parser.extractArticle(target)
        pagenum = pagenum + 1