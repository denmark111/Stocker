# Top application for running multiple crawlers

from AWS import aws_access
from Parsers.seeking_alpha_parser import getSeeking
from Parsers.nasdaq_parser import getNasdaq


if __name__ in '__main__':
    
    # AWS Comprehend API class
    comprehend = aws_access.awsAccess()
    
    # Nasdaq page
    nasdaq = getNasdaq()

    # Seeking Alpha page
    seekingAlpha = getSeeking()

    # Start analistics with AWS Comprehend API
    