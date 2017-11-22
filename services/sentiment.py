import logging
import pprint
import requests

class Sentiment(object):
    def __init__(self, url: str):
        self.url = url
        

    def create_payload(self, text: str) -> dict:
        payload = {'text': text}
        return payload

    def analyze(self, text: str) -> dict:
        payload = self.create_payload(text)
        r = requests.post(self.url, data=payload)
        
        if r.status_code == 200:
            sentiment = r.json()
            return sentiment
    
        return {}
        # throw
