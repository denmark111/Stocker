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

    sample = 'But negotiators here ran into serious trouble when Saudi Arabia, the US, Russia and Kuwait objected to the conference "welcoming" the document. Instead they wanted to support a much more lukewarm phrase, that the conference would "take note" of the report. Saudi Arabia had fought until the last minute in Korea to limit the conclusions of the document. Eventually they gave in. But it now seems that they have brought their objections to Poland. The dispute dragged on as huddles of negotiators met in corners of the plenary session here, trying to agree a compromise wording.'

    result = []
    words_string = ''

    aws = AWSAccess()

    result.append(aws.getKeywordResult(sample))

    for elem in result:
        for words in elem['KeyPhrases']:
            words_string += (words['Text'] + ' ')
        print(words_string)
        words_string = ''