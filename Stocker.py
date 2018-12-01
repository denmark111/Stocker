# Top application for running multiple crawlers

from AWS import aws_access
from Parsers.seeking_alpha_parser import getNewsArticle

if __name__ in '__main__':
    
    # AWS Comprehend API class
    comprehend = aws_access.awsAccess()
    
    # Seeking Alpha page
    seekingAlpha = getNewsArticle()

    # Start analistics with AWS Comprehend API
    