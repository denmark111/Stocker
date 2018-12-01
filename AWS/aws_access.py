import boto3
import json

class awsAccess():

    def __init__(self):
        self.comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

    def getResult(self, text):
        return json.dumps(self.comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4)
