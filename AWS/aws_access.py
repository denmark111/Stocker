import boto3
import json

class AWSAccess():

    def __init__(self):
        self.comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

    def getSentimentResult(self, text):
        return json.dumps(self.comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4)

    def getKeywordResult(self, text):
        return json.dumps(self.comprehend.detect_key_phrases(Text=text, LanguageCode='en'), sort_keys=True, indent=4)
