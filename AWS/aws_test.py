import boto3
import json

class AWSAccess():

    def __init__(self):
        self.comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

    def getSentimentResult(self, text):
        return self.comprehend.detect_sentiment(Text=text, LanguageCode='en')

    def getKeywordResult(self, text):
        return self.comprehend.detect_key_phrases(Text=text, LanguageCode='en')


if __name__ in '__main__':

    sample = 'Dec 6 (Reuters) - Walgreens Boots Alliance (WBA) said onThursday it would partner with FedEx Corp (FDX) to launch anext-day delivery service for prescription drugs nationwide,giving it a leg up as Amazon (AMZN) threatens to shake-up the sector.In the race to make inroads in the on-demand drug deliveryspace, Walgreens move could potentially put it head-to-headwith Amazon.com Inc (AMZN), which earlier this year said itwould buy online pharmacy PillPack.Amazons (AMZN) entry in the market would rattle.'

    result = []
    words_string = ''

    aws = AWSAccess()

    result.append(aws.getKeywordResult(sample))

    # print(json.dumps(aws.getKeywordResult(sample)))
    print(json.dumps(aws.getSentimentResult(sample)))

    # for elem in result:
    #     for words in elem['KeyPhrases']:
    #         words_string += (words['Text'] + ' ')
    #     print(words_string)
    #     words_string = ''