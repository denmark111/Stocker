from html.parser import HTMLParser
import urllib.request, urllib.error
from queue import *
import string
import re
from operator import itemgetter
import operator

links = []
output = [] # use for sort URL date
result = [] # get article title URL in fidelity.com
temp_result = [] # use for sort URL

class MyHTMLParser(HTMLParser): 
  
    def handle_starttag(self, tag, attrs): 
        if tag != 'a': 
            return 
  
        attr = dict(attrs) 
        links.append(attr)
        
def extract(url): 

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
        if 'target' in l and 'title' in l:  
            if l['target'] == '_top': 
                if l['href']!='https://www.fidelity.com/sector-investing/overview' : 
                   result.append(l['href']) 
                   #output.append(l['href'].strip('https://www.fidelity.com/news/article/compony-news' + 'https://www.fidelity.com/news/article/default' + 'https://www.fidelity.com/news/article/us-markets' + 'https://www.fidelity.com/news/article/investing-ideas' + 'https://www.fidelity.com/news/article/mergers-and-quisition' + 'https://www.fidelity.com/news/article/technology'))
                   output.append(l['href'].split('/')[6])

    links.clear() 

    return None 

if __name__ in "__main__": 
  
      stock_name = 'amzn' 
      pagenum = 0 
      stock_link1 = 'https://search.fidelity.com/search/getNewsSearchResults?question=' + stock_name + '&originatingpage=NSRP&NSRPpageSelected=' 
      stock_link2 =  '&navState=root%7Croot-' 
      stock_link3 = '-10%7C0&binningState=&sortBy=&sourceBoxState=&bundleName=news-bundle' 

  
      for pagenum in range(0, 10): 
          target = stock_link1 + str(pagenum+1)+ stock_link2 + str(pagenum*10) + stock_link3 
            
          extract(target) 
      # temp_result = result       
      temp_result = result.copy()
      #sort url date
      output.sort()
      #sort url in chronological order 
      for i in range(0,len(output)) :
          result[i]=temp_result[int(output[i].split('=')[1])-1]
          
      for i in range(0,100):    
          print(result[i])