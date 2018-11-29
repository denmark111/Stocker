
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
          if 'target' in l and 'title' in l: 
              if l['target'] == '_top': 
                  result.append(l['href']) 
  
      del result[0] 
      links.clear() 
  
      return result 
 
if __name__ in "__main__": 
  
      stock_name = 'amzn' 
      pagenum=0
      stock_link1 = 'https://search.fidelity.com/search/getNewsSearchResults?question=' + stock_name + '&originatingpage=NSRP&NSRPpageSelected=2&navState=root%7Croot-' 
      stock_link2 = '-10%7C0&binningState=&sortBy=&sourceBoxState=&bundleName=news-bundle' 
      output = [] 
  
      for pagenum in range(0, 10): 
          target = stock_link1 + str(pagenum * 10) + stock_link2
            
          print(target) 
  
          output.append(extract(target)) 
          print(output[pagenum - 1]) 
