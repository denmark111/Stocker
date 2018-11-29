from html.parser import HTMLParser
import urllib.request, urllib.error
from queue import *

co_ar = LifoQueue() # collect article / stack / ☆☆☆☆☆☆☆☆

tmp_stk = LifoQueue() # article title buffer1/ stack
tmp_q = Queue() # article title buffer2 /queue

links = []
output = [] # get page in fidelity.com
result = [] # result in extract

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
                  result.append(l['href']) 
  
      del result[0] 
      links.clear() 
  
      return result 
 
if __name__ in "__main__": 
  
      stock_name = 'amzn' 
      pagenum = 0
      stock_link1 = 'https://search.fidelity.com/search/getNewsSearchResults?question=' + stock_name + '&originatingpage=NSRP&NSRPpageSelected='
      stock_link2 =  '&navState=root%7Croot-' 
      stock_link3 = '-10%7C0&binningState=&sortBy=&sourceBoxState=&bundleName=news-bundle' 

  
      for pagenum in range(0, 10): 
          target = stock_link1 + str(pagenum+1)+ stock_link2 + str(pagenum * 10) + stock_link3
            
          print(target) 
          
          output.append(extract(target))
          
          print(output[pagenum]) 