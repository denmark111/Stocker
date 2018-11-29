# Stocker

Stocker is a real time stock news analyzer with AWS Comprehend integrated.  
It's purpose is to crawl stock info web pages and analyze various news article with machine learning.  

### Supported stock news website

1. [www.nasdaq.com](https://www.nasdaq.com)  

2. [www.seekingalpha.com](https://www.seekingalpha.com)

3. [www.fidelity.com](https://www.fidelity.com)

4. TBD

### Machine learning integration w/ AWS Comprehend

Machine learning text analyzer used in this project is AWS Comprehend.  
Crawled news article datas are feeded through AWS Comprehend API and then processed.  
Processed data can be received via JSON data format.  

AWS Comprehend could be used with AWS Translate to provide wide variety of language support.  

### Visualization with JavaScript

Collected datas from the AWS Comprehend are trimmed and organized to be displayed.  
Data visualization is performed with Charts.js & D3.js which is popular open source JavaScript library.  

### Prerequisites

To run this application on your own, you need to meet requirements shown below.  

- **Python 3**  

    Python 3 is required for web crawling.  
    built-in `html.Parser` library is used to parse html code.

- **AWS Account**

    AWS is required for AWS Comprehend service.  
    To learn more about AWS Comprehend, visit [here](https://aws.amazon.com/ko/comprehend/)  
    AWS is integrated as API in each crawler.

- **Apache web server**

    Required to actually run the application.  

### Installation

1. TBD