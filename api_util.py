import requests
import json
from ai_util import estimate_sentiment

class REST():
    def __init__(self, CREDS:dict):
        self.CREDS = CREDS

    def get_headlines(self, start:str, end:str, symbol:str):
        url = (f"https://data.alpaca.markets/v1beta1/news?start={start}&end={end}&sort=desc&symbols={symbol}&include_content=false")
        headers = {
            "accept": "application/json",
            "APCA-API-KEY-ID": self.CREDS['API_KEY'],
            "APCA-API-SECRET-KEY": self.CREDS['API_SECRET']
        }
        response = requests.get(url, headers=headers)
        res_json = response.json()

        headlines = []

        for n in res_json['news']:
            headlines.append(n["headline"])

        return headlines

# creds = open('CREDS.json')
# CREDS = json.load(creds)
# start = '2024-06-01T00:00:00Z'
# end = '2024-06-13T00:00:00Z'
# symbol = 'SPY'

# news = get_headlines(CREDS=CREDS, start=start, end=end, symbol=symbol)

# probability, sentiment = estimate_sentiment(news)

# print(probability)
# print(sentiment)

