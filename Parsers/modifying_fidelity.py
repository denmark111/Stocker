from html.parser import HTMLParser
import urllib.request, urllib.error
from queue import *
import string
import re
from operator import itemgetter
import operator

links = []
output = [] # get article title URL in fidelity.com
result = [] # result in extract
temp_result = []
temp_output = [] # result in extract
ab ={}
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

#def sorturl(a,b):
    #ab=[a,b]
    #i=0
    #for x in a:
    #    ab[x] = b[i]
    #    i+=1   
    #sortedz = sorted(ab.items(),key=operator.itemgetter(1))

    #return print(sortedz.key)
if __name__ in "__main__": 
  
      stock_name = 'amzn' 
      pagenum = 0 
      stock_link1 = 'https://search.fidelity.com/search/getNewsSearchResults?question=' + stock_name + '&originatingpage=NSRP&NSRPpageSelected=' 
      stock_link2 =  '&navState=root%7Croot-' 
      stock_link3 = '-10%7C0&binningState=&sortBy=&sourceBoxState=&bundleName=news-bundle' 

  
      for pagenum in range(0, 10): 
          target = stock_link1 + str(pagenum+1)+ stock_link2 + str(pagenum*10) + stock_link3 
            
          extract(target) 
      #for i in range(0,len(output))
            
          
      output.sort()
      temp_result = result.copy()
      for x,i in output[x][1],range(0,len(temp_output)):
          temp_result[i] 

      #for i in range(0,100):
          #temp_result[i] = result[i].split('/')
      #result.sorted(result,key=temp_result{6})
      #print(re.match("2018....",result[3].split('/')[6]))

      #for i in range(0,100):
      sorturl(result,output)
      #print(sorturl(result,output).items(0))      
      
     # for i in range(0,100):    
      #    print(output[i])