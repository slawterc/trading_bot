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

