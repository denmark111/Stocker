# Stocker

Stocker is a real time stock news analyzer with AWS Comprehend integrated.  
It's purpose is to crawl stock info web pages and analyze various news article with machine learning.  

### Machine learning integration w/ AWS Comprehend

Machine learning text analyzer used in this project is AWS Comprehend.  
Crawled news article datas are feeded through AWS Comprehend API and then processed.  
Processed data can be received via JSON data format.  

### Visualization with JavaScript

Collected datas from the AWS Comprehend are trimmed and organized to be displayed.  
Data visualization is performed with Charts.js & D3.js which is popular open source JavaScript library.  

### Prerequisites

To run this application on your own, you need to meet requirements shown below.  

- `Python 3`  

Python 3 is required for web crawling.  

- `AWS Account`

AWS is required for AWS Comprehend service.  

- `Apache web server`

Required to actually run the application